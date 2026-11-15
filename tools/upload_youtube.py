"""Upload only when explicitly invoked; private visibility by default."""
from pathlib import Path
import argparse, json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from youtube_manage import credentials, own_channel, metadata_body

root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument('video',type=Path)
p.add_argument('--metadata',type=Path,required=True,help='JSON with title, description, tags, categoryId, madeForKids, containsSyntheticMedia')
p.add_argument('--channel',required=True,help='Expected channel ID; verified before upload')
p.add_argument('--privacy',choices=['private','unlisted','public'],default='private')
a=p.parse_args()
if not a.video.is_file(): p.error('Video file does not exist')
m=json.loads(a.metadata.read_text(encoding='utf-8'))
for key in ['title','description','madeForKids','containsSyntheticMedia']:
    if key not in m: p.error(f'Metadata must explicitly set {key}')
if not isinstance(m['madeForKids'],bool) or not isinstance(m['containsSyntheticMedia'],bool): p.error('Audience and synthetic-media fields must be JSON booleans')
creds=credentials('upload')
youtube=build('youtube','v3',credentials=creds,cache_discovery=False)
own_channel(youtube,a.channel)
body={'snippet':{'title':m['title'],'description':m['description'],'tags':m.get('tags',[]),'categoryId':str(m.get('categoryId','27'))},'status':{'privacyStatus':a.privacy,'selfDeclaredMadeForKids':bool(m['madeForKids']),'containsSyntheticMedia':bool(m['containsSyntheticMedia'])}}
metadata_body({'id':'pending-upload','snippet':body['snippet']},{})
request=youtube.videos().insert(part='snippet,status',body=body,media_body=MediaFileUpload(str(a.video),chunksize=8*1024*1024,resumable=True),notifySubscribers=False)
response=None
while response is None:
    progress,response=request.next_chunk(num_retries=3)
    if progress: print(f'{progress.progress()*100:.0f}%')
print('https://www.youtube.com/watch?v='+response['id'])
