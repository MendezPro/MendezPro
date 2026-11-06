"""Refresh the profile SVG using only public GitHub API data; no dependencies."""
import os, json, html, urllib.request
from pathlib import Path
from datetime import datetime, timezone

USER = 'MendezPro'
ROOT = Path(__file__).resolve().parents[1]

def api(path):
    headers = {'User-Agent': 'MendezPro-profile', 'Accept': 'application/vnd.github+json'}
    if os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    with urllib.request.urlopen(urllib.request.Request('https://api.github.com/' + path, headers=headers),timeout=30) as r:
        return json.load(r)

def txt(x,y,t,size=16,c='#E6EDF3',w=400):
    return f'<text x="{x}" y="{y}" fill="{c}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{w}">{html.escape(str(t))}</text>'

def box(x,y,w,h,stroke='#28313D'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="13" fill="#151C25" stroke="{stroke}"/>'

def main():
    user=api('users/'+USER)
    repos=[]
    page=1
    while True:
        batch=api(f'users/{USER}/repos?type=owner&per_page=100&page={page}')
        repos.extend(batch)
        if len(batch)<100: break
        page+=1
    own=[r for r in repos if not r['fork']]
    languages=set()
    for repo in own:
        languages.update(api('repos/'+USER+'/'+repo['name']+'/languages'))
    stars=sum(r['stargazers_count'] for r in own)
    followers=user['followers']
    n=len(own)
    body=txt(36,43,'03 / GITHUB PULSE',13,'#7F8EA3',600)
    body+=txt(860,43,datetime.now(timezone.utc).strftime('ACTUALIZADO · %d %b %Y · UTC'),12,'#7F8EA3')
    for i,(v,label) in enumerate([(n,'REPOS PROPIOS PÚBLICOS'),(followers,'SEGUIDORES'),(len(languages),'LENGUAJES EN REPOS'),(stars,'ESTRELLAS RECIBIDAS')]):
        x=30+i*293
        body+=box(x,66,263,118)+txt(x+22,124,v,42,'#6EE7D8' if i%2==0 else '#C4B9FF',600)+txt(x+22,158,label,11,'#A7B3C4',600)
    body=body.replace('03 / GITHUB PULSE','GITHUB / PUBLIC ACTIVITY')
    body+=txt(36,218,'Datos públicos · repositorios y estrellas sin forks · lenguajes detectados en código, no niveles de dominio',12,'#7F8EA3')
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="244" viewBox="0 0 1200 244" role="img"><rect width="1200" height="244" rx="22" fill="#0D1117"/><rect x="1" y="1" width="1198" height="242" rx="21" fill="none" stroke="#28313D"/>{body}</svg>'
    out=ROOT/'assets/github-pulse.svg'
    out.parent.mkdir(exist_ok=True)
    temporary=out.with_suffix('.tmp')
    temporary.write_text(svg,encoding='utf-8')
    temporary.replace(out)
    print('Updated public profile statistics.')
    refresh_trophies()

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

if __name__=='__main__': main()
