"""Refresh cached GitHub Profile Trophy cards; keep the last image on failure."""
import urllib.request
from pathlib import Path

USER='MendezPro'
ROOT=Path(__file__).resolve().parents[1]

def refresh_trophies():
    # Community mirror documented by ryo-ma/github-profile-trophy. No token is sent.
    url='https://trophy.ryglcloud.net/?username='+USER+'&theme=tokyonight&no-frame=true&no-bg=true&column=4&row=1&margin-w=18&title=Commits,PullRequest,Followers,Repositories'
    try:
        from xml.etree import ElementTree as ET
        req=urllib.request.Request(url,headers={'User-Agent':'MendezPro-profile'})
        with urllib.request.urlopen(req,timeout=30) as response:
            data=response.read(2_000_000)
        data=('\n'.join(line.rstrip() for line in data.decode('utf-8').splitlines()).rstrip()+'\n').encode('utf-8')
        document=ET.fromstring(data)
        if document.tag!='{http://www.w3.org/2000/svg}svg':
            raise ValueError('Response is not an SVG')
        content=' '.join(document.itertext())
        for label in ('Commits','PullRequest','Followers','Repositories'):
            if label not in content: raise ValueError('Missing trophy category')
        if any(el.tag.rsplit('}',1)[-1] in ('script','foreignObject','image','a','use') or any(key.rsplit('}',1)[-1].lower().startswith('on') for key in el.attrib) for el in document.iter()):
            raise ValueError('Unexpected active or external content')
        import re
        def external(value):
            value=re.sub(r'url\(#[A-Za-z0-9_-]+\)','',value,flags=re.I).lower()
            return 'url(' in value or 'javascript:' in value or '@import' in value
        if any(external(val) for el in document.iter() for val in el.attrib.values()) or any(external(el.text or '') for el in document.iter() if el.tag.endswith('style')):
            raise ValueError('Unexpected linked content')
        target=ROOT/'assets/trophies.svg'
        temp=target.with_suffix('.tmp')
        temp.write_bytes(data)
        temp.replace(target)
        print('Updated cached trophy cards.')
    except Exception as error:
        # Keep the last valid image if the volunteer service is unavailable.
        print('Trophy refresh unavailable; keeping previous image: '+type(error).__name__)

if __name__=='__main__': refresh_trophies()
