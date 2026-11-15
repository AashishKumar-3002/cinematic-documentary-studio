"""Save a public source with URL and retrieval time for later fact checking."""
import argparse, json
from pathlib import Path
from datetime import datetime, timezone
from scrapling.fetchers import Fetcher
p=argparse.ArgumentParser()
p.add_argument('url')
p.add_argument('--output',type=Path,required=True)
a=p.parse_args()
if not a.url.startswith(('https://','http://')): p.error('Use an HTTP(S) URL')
page=Fetcher.get(a.url,timeout=30)
if page.status>=400: raise RuntimeError(f'HTTP {page.status}')
record={'url':a.url,'retrieved_at':datetime.now(timezone.utc).isoformat(),'status':page.status,'title':page.css('title::text').get(),'text':page.get_all_text(ignore_tags=('script','style'))}
a.output.parent.mkdir(parents=True,exist_ok=True)
a.output.write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf-8')
print(a.output)
