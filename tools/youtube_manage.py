"""Project-local YouTube management. Only connect starts OAuth; writes require --apply."""
from __future__ import annotations
import argparse, copy, json, sys
from datetime import date, datetime, timezone
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

ROOT=Path(__file__).resolve().parents[1]
AUTH='https://www.googleapis.com/auth/'
PROFILES={
    'read':[AUTH+'youtube.readonly'],
    'upload':[AUTH+'youtube.readonly',AUTH+'youtube.upload'],
    'manage':[AUTH+'youtube.force-ssl'],
    'analytics':[AUTH+'youtube.readonly',AUTH+'yt-analytics.readonly'],
}
SNIPPET={'title','description','tags','categoryId','defaultLanguage','defaultAudioLanguage'}
STATUS={'privacyStatus','embeddable','license','publicStatsViewable','selfDeclaredMadeForKids','containsSyntheticMedia','publishAt'}

def emit(value): print(json.dumps(value,indent=2,ensure_ascii=False))
def load(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def token_path(profile): return ROOT/'credentials'/('youtube-'+profile+'.json')

def credentials(profile,connect=False):
    token=token_path(profile)
    if connect:
        secret=ROOT/'credentials/client_secret.json'
        if not secret.is_file(): raise ValueError('Save a Desktop OAuth client JSON to credentials/client_secret.json first. See the management skill setup reference.')
        creds=InstalledAppFlow.from_client_secrets_file(str(secret),PROFILES[profile]).run_local_server(port=0,access_type='offline',prompt='consent')
    else:
        if not token.is_file(): raise ValueError(f'Profile {profile!r} is not connected. Run connect --profile {profile} when ready to sign in.')
        creds=Credentials.from_authorized_user_file(str(token),PROFILES[profile])
        if not creds.has_scopes(PROFILES[profile]): raise ValueError('Token lacks required scopes. Reconnect this profile.')
        if creds.expired and creds.refresh_token: creds.refresh(Request())
        if not creds.valid: raise ValueError('Authorization expired or was revoked. Reconnect this profile.')
    token.parent.mkdir(parents=True,exist_ok=True)
    token.write_text(creds.to_json(),encoding='utf-8')
    return creds

def service(profile): return build('youtube','v3',credentials=credentials(profile),cache_discovery=False)
def one(request):
    items=request.execute().get('items',[])
    if not items: raise ValueError('Resource not found or not accessible to this account')
    return items[0]

def own_channel(yt,expected):
    channels=yt.channels().list(part='id,snippet',mine=True,maxResults=50).execute().get('items',[])
    if expected not in {c['id'] for c in channels}: raise ValueError('Expected channel does not match the authenticated account. Stop and reconnect the correct channel.')
    return next(c for c in channels if c['id']==expected)

def owned_video(yt,video_id,channel):
    video=one(yt.videos().list(part='snippet,status,processingDetails',id=video_id))
    if video['snippet']['channelId']!=channel: raise ValueError('Video belongs to a different channel')
    return video

def metadata_body(video,patch):
    unknown=set(patch)-SNIPPET
    if unknown: raise ValueError('Unsupported metadata fields: '+', '.join(sorted(unknown)))
    snippet={k:copy.deepcopy(v) for k,v in video['snippet'].items() if k in SNIPPET}
    snippet.update(patch)
    if not isinstance(snippet.get('title'),str) or not 1<=len(snippet['title'])<=100: raise ValueError('Title must contain 1..100 characters')
    if not isinstance(snippet.get('description',''),str) or len(snippet.get('description',''))>5000: raise ValueError('Description must be a string of at most 5000 characters')
    if not snippet.get('categoryId'): raise ValueError('categoryId is required')
    if 'tags' in snippet and (not isinstance(snippet['tags'],list) or any(not isinstance(x,str) for x in snippet['tags'])): raise ValueError('tags must be a list of strings')
    return {'id':video['id'],'snippet':snippet}

def visibility_body(video,privacy,publish_at=None):
    status={k:copy.deepcopy(v) for k,v in video['status'].items() if k in STATUS}
    status['privacyStatus']=privacy
    status.pop('publishAt',None)
    if publish_at:
        if privacy!='private': raise ValueError('Scheduling requires private visibility')
        when=datetime.fromisoformat(publish_at.replace('Z','+00:00'))
        if when.tzinfo is None or when<=datetime.now(timezone.utc): raise ValueError('Publish time must be in the future with an explicit timezone')
        status['publishAt']=when.astimezone(timezone.utc).isoformat().replace('+00:00','Z')
    return {'id':video['id'],'status':status}

def save_plan(action,channel,before,body):
    folder=ROOT/'output/youtube-management'
    folder.mkdir(parents=True,exist_ok=True)
    name=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'-'+action+'.json'
    path=folder/name
    path.write_text(json.dumps({'action':action,'channel':channel,'before':before,'request':body},indent=2,ensure_ascii=False),encoding='utf-8')
    return str(path)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('status',help='Local connection status; no Google request')
    c=sub.add_parser('connect',help='Explicitly start browser sign-in')
    c.add_argument('--profile',choices=PROFILES,default='read')
    for name in ['channel','videos','video','comments','playlists','analytics','metadata','visibility','thumbnail','captions','create-playlist','add-to-playlist']:
        c=sub.add_parser(name)
        c.add_argument('--channel',required=True,help='Expected channel ID, verified against authenticated account')
        if name in ['videos','playlists','comments']: c.add_argument('--page-token')
        if name in ['video','comments','metadata','visibility','thumbnail','captions','add-to-playlist']: c.add_argument('--video',required=True)
        if name=='analytics':
            c.add_argument('--start',required=True); c.add_argument('--end',required=True)
            c.add_argument('--report',choices=['daily','traffic','retention'],default='daily'); c.add_argument('--video')
        if name in ['metadata','create-playlist']: c.add_argument('--file',required=True,type=Path)
        if name=='visibility':
            c.add_argument('--privacy',choices=['private','unlisted','public'],required=True)
            c.add_argument('--publish-at',help='Future ISO timestamp with timezone; requires private visibility')
        if name in ['thumbnail','captions']: c.add_argument('--file',required=True,type=Path)
        if name=='captions': c.add_argument('--language',default='en'); c.add_argument('--name',default='English')
        if name=='add-to-playlist': c.add_argument('--playlist',required=True)
        if name in ['metadata','visibility','thumbnail','captions','create-playlist','add-to-playlist']: c.add_argument('--apply',action='store_true',help='Perform the reviewed change; default is a read-only plan')
    a=parser.parse_args()
    if a.command=='status':
        emit({'oauth_client_present':(ROOT/'credentials/client_secret.json').is_file(),'profiles':{p:{'token_present':token_path(p).is_file(),'scopes':s} for p,s in PROFILES.items()},'note':'Token presence does not prove live access.'}); return
    if a.command=='connect':
        creds=credentials(a.profile,True)
        emit({'profile':a.profile,'channels':build('youtube','v3',credentials=creds,cache_discovery=False).channels().list(part='id,snippet',mine=True).execute()}); return
    writes=a.command in ['metadata','visibility','thumbnail','captions','create-playlist','add-to-playlist']
    profile='analytics' if a.command=='analytics' else 'manage' if writes and a.apply else 'read'
    yt=service(profile)
    channel=own_channel(yt,a.channel)
    if a.command=='channel': emit(channel); return
    if a.command=='videos':
        details=one(yt.channels().list(part='contentDetails',id=a.channel))
        emit(yt.playlistItems().list(part='snippet,contentDetails',playlistId=details['contentDetails']['relatedPlaylists']['uploads'],maxResults=50,pageToken=a.page_token).execute()); return
    if a.command=='playlists': emit(yt.playlists().list(part='snippet,status,contentDetails',mine=True,maxResults=50,pageToken=a.page_token).execute()); return
    if a.command=='analytics':
        start=date.fromisoformat(a.start); end=date.fromisoformat(a.end)
        if start>end: raise ValueError('Start date is after end date')
        if a.report=='retention' and not a.video: raise ValueError('Retention requires --video')
        if a.video: owned_video(yt,a.video,a.channel)
        dims,metrics={'daily':('day','views,estimatedMinutesWatched,averageViewDuration'),'traffic':('insightTrafficSourceType','views,estimatedMinutesWatched'),'retention':('elapsedVideoTimeRatio','audienceWatchRatio,relativeRetentionPerformance')}[a.report]
        opts={'ids':'channel=='+a.channel,'startDate':a.start,'endDate':a.end,'dimensions':dims,'metrics':metrics}
        if a.video: opts['filters']='video=='+a.video
        analytics=build('youtubeAnalytics','v2',credentials=credentials('analytics'),cache_discovery=False)
        emit(analytics.reports().query(**opts).execute()); return
    video=owned_video(yt,a.video,a.channel) if hasattr(a,'video') else None
    if a.command=='video': emit(video); return
    if a.command=='comments': emit(yt.commentThreads().list(part='snippet,replies',videoId=a.video,maxResults=50,pageToken=a.page_token,textFormat='plainText').execute()); return
    before=video
    if a.command=='metadata': body=metadata_body(video,load(a.file))
    elif a.command=='visibility': body=visibility_body(video,a.privacy,a.publish_at)
    elif a.command in ['thumbnail','captions']:
        if not a.file.is_file(): raise ValueError('Media file does not exist')
        if a.command=='thumbnail':
            from PIL import Image
            with Image.open(a.file) as im:
                if im.format not in ('PNG','JPEG'): raise ValueError('Thumbnail must be PNG or JPEG')
            if a.file.stat().st_size>50*1024*1024: raise ValueError('Thumbnail exceeds the documented API upload limit')
            body={'videoId':a.video,'file':str(a.file.resolve())}
        else:
            if a.file.suffix.lower() not in ('.srt','.vtt'): raise ValueError('Use a time-coded SRT or VTT file')
            body={'snippet':{'videoId':a.video,'language':a.language,'name':a.name,'isDraft':False},'file':str(a.file.resolve())}
    elif a.command=='create-playlist':
        patch=load(a.file)
        if not isinstance(patch.get('title'),str) or not patch['title']: raise ValueError('Playlist title required')
        privacy=patch.get('privacyStatus','private')
        if privacy not in ('private','unlisted','public'): raise ValueError('Invalid playlist visibility')
        body={'snippet':{'title':patch['title'],'description':patch.get('description','')},'status':{'privacyStatus':privacy}}
    elif a.command=='add-to-playlist':
        before=one(yt.playlists().list(part='snippet,status',id=a.playlist))
        if before['snippet']['channelId']!=a.channel: raise ValueError('Playlist belongs to a different channel')
        existing=yt.playlistItems().list(part='id',playlistId=a.playlist,videoId=a.video,maxResults=1).execute()
        if existing.get('items'): emit({'already_present':True,'playlist':a.playlist,'video':a.video}); return
        body={'snippet':{'playlistId':a.playlist,'resourceId':{'kind':'youtube#video','videoId':a.video}}}
    plan=save_plan(a.command,a.channel,before,body)
    if not a.apply: emit({'dry_run':True,'plan':plan,'request':body}); return
    if a.command in ['metadata','visibility']:
        part='snippet' if a.command=='metadata' else 'status'
        result=yt.videos().update(part=part,body=body).execute()
        readback=owned_video(yt,a.video,a.channel)
        emit({'applied':True,'plan':plan,'result':result,'readback':readback}); return
    if a.command=='thumbnail':
        if video.get('processingDetails',{}).get('processingStatus')!='succeeded': raise ValueError('Wait until video processing succeeds before setting the thumbnail')
        result=yt.thumbnails().set(videoId=a.video,media_body=MediaFileUpload(str(a.file))).execute()
    elif a.command=='captions': result=yt.captions().insert(part='snippet',body={'snippet':body['snippet']},media_body=MediaFileUpload(str(a.file),mimetype='application/octet-stream')).execute()
    elif a.command=='create-playlist': result=yt.playlists().insert(part='snippet,status',body=body).execute()
    else: result=yt.playlistItems().insert(part='snippet',body=body).execute()
    emit({'applied':True,'plan':plan,'result':result,'note':'Verify media processing or playlist result before reporting completion.'})

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8',errors='replace')
    try: main()
    except Exception as exc:
        print(f'YouTube operation failed: {exc}',file=sys.stderr)
        raise SystemExit(1)
