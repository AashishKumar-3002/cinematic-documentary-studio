"""Durable native cinematic-film export; resume validated 4-second sections after interruptions."""
import concurrent.futures
import argparse
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
from studio_runtime import find_tool

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.agents/skills/cinematic-film/scripts'))
from render import make,encoder_args

P=ROOT/'projects/lake-nyos/film'
OUT=P/'out';CHECK=OUT/'checkpoints1080';CHECK.mkdir(parents=True,exist_ok=True)
FPS=30;SIZE='1920x1080';STEP=120

def run_job(job):
    idx,first,last=job
    f,r,_=make(P,SIZE)
    dest=CHECK/f'part{idx:04d}.mp4'
    proc=subprocess.Popen([find_tool('ffmpeg'),'-v','error','-y','-f','rawvideo',
        '-pix_fmt','rgb24','-s',SIZE,'-r',str(FPS),'-i','-',*encoder_args(1920,18),str(dest)],stdin=subprocess.PIPE)
    try:
        for n in range(first,last):proc.stdin.write(r.frame(n).tobytes())
        proc.stdin.close()
        if proc.wait()!=0:raise RuntimeError(f'encoder failed: {idx}')
    except BaseException:
        proc.kill();raise
    return idx,last-first

def frame_count(path):
    if not path.exists() or path.stat().st_size==0:return 0
    q=subprocess.run([find_tool('ffprobe'),'-v','error','-select_streams','v:0',
        '-show_entries','stream=nb_frames','-of','csv=p=0',str(path)],capture_output=True,text=True)
    try:return int(q.stdout.strip()) if q.returncode==0 else 0
    except ValueError:return 0

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workers',type=int,default=2,choices=range(1,9),help='Concurrent render workers; start with 2 on a new machine')
    args=parser.parse_args()
    start=time.time()
    timing=json.loads((P/'audio/timing.json').read_text())
    total=round(timing['total_duration']*FPS)
    jobs=[(i,a,min(total,a+STEP)) for i,a in enumerate(range(0,total,STEP))]
    done={i for i,a,b in jobs if frame_count(CHECK/f'part{i:04d}.mp4')==b-a}
    def status(state):
        count=sum(b-a for i,a,b in jobs if i in done)
        obj={'state':state,'completed_sections':len(done),'total_sections':len(jobs),
             'completed_frames':count,'total_frames':total,'percent':round(100*count/total,1),
             'elapsed_this_run_seconds':round(time.time()-start),'pid':os.getpid(),
             'output':'lake-nyos-full-v1-1080p.mp4'}
        temp=OUT/'render-progress.tmp';temp.write_text(json.dumps(obj,indent=2));temp.replace(OUT/'render-progress.json')
        print(json.dumps(obj),flush=True)
    status('rendering')
    remaining=[j for j in jobs if j[0] not in done]
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures=[pool.submit(run_job,j) for j in remaining]
        for future in concurrent.futures.as_completed(futures):
            i,count=future.result();done.add(i);status('rendering')
    status('muxing')
    listing=CHECK/'concat.txt'
    listing.write_text(''.join(f"file '{(CHECK/f'part{i:04d}.mp4').as_posix()}'\n" for i,_,_ in jobs))
    dest=OUT/'lake-nyos-full-v1-1080p.mp4'
    subprocess.run([find_tool('ffmpeg'),'-y','-v','error','-f','concat','-safe','0','-i',str(listing),
        '-i',str(P/'audio/mix.m4a'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k',
        '-shortest','-movflags','+faststart',str(dest)],check=True)
    subprocess.run([find_tool('ffmpeg'),'-v','error','-i',str(dest),'-f','null','-'],check=True)
    status('complete; decoded without errors')

if __name__=='__main__':main()
