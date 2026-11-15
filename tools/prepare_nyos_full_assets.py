"""Verified archival assets and a public-domain geographic locator."""
import json
import urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'projects/lake-nyos/film'
(P/'assets/photos').mkdir(parents=True,exist_ok=True)
data=P/'assets/data';data.mkdir(parents=True,exist_ok=True)
def get(url,path):
    if not path.exists():
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'DocumentaryResearch/1.0'}),timeout=60) as r:
            path.write_bytes(r.read())
    print(path.name,flush=True)
get('https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson',data/'natural-earth-countries.geojson')
get('https://svs.gsfc.nasa.gov/vis/a000000/a002300/a002348/nyos.jpg',P/'assets/photos/P03_NASA_Landsat_2001.jpg')
spec=json.loads((P/'photos.json').read_text())
if not any(x['id']=='P03' for x in spec['photos']):
    spec['photos'].append({'id':'P03','what':'Landsat-7 image of Lake Nyos, 5 February 2001',
        'file':'P03_NASA_Landsat_2001.jpg','kind':'photo',
        'source':'https://svs.gsfc.nasa.gov/2348/',
        'credit':'NASA/Goddard Space Flight Center Scientific Visualization Studio',
        'license':'Public domain (NASA imagery; no third-party copyright credit on the asset record)',
        'license_url':'https://www.nasa.gov/nasa-brand-center/images-and-media/',
        'license_ok':True,'date':'2001-02-05'})
(P/'photos.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
