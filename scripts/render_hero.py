"""Render a looping mathematical 4D tesseract; requires Pillow. Run from any cwd."""
from pathlib import Path
import itertools, math
from PIL import Image, ImageDraw, ImageFilter

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
VERTICES=list(itertools.product((-1,1),repeat=4))
EDGES=[(a,b) for a in range(16) for b in range(a+1,16) if sum(VERTICES[a][j]!=VERTICES[b][j] for j in range(4))==1]

def turn(v,a,b,angle):
    c,s=math.cos(angle),math.sin(angle)
    v[a],v[b]=c*v[a]-s*v[b],s*v[a]+c*v[b]

def geometry(t):
    result=[]
    for raw in VERTICES:
        v=list(raw)
        turn(v,0,3,t+0.32)
        turn(v,1,2,t+0.52)
        turn(v,0,1,0.3)
        k=3.8/(3.8-v[3])
        p=[v[i]*k for i in range(3)]
        turn(p,0,2,0.45)
        turn(p,1,2,0.30)
        f=5.5/(5.5-p[2])
        result.append((930+p[0]*56*f,190+p[1]*56*f,p[2],v[3]))
    return result

def main():
    base=Image.open(ASSETS/'hero-base.png').convert('RGB')
    frames=[]
    for frame in range(96):
        points=geometry(frame*math.tau/96)
        overlay=Image.new('RGBA',(560*2,350*2))
        d=ImageDraw.Draw(overlay)
        for a,b in sorted(EDGES,key=lambda edge:points[edge[0]][2]+points[edge[1]][2]):
            pa,pb=points[a],points[b]
            hue=((pa[3]+pb[3])/2+1.6)/3.2
            hue=max(0,min(1,hue))
            color=tuple(int(x+(y-x)*hue) for x,y in zip((110,231,216),(169,155,255)))
            alpha=int(125+100*min(1,max(0,(pa[2]+pb[2]+4)/8)))
            d.line(((pa[0]-640)*2,(pa[1]-25)*2,(pb[0]-640)*2,(pb[1]-25)*2),fill=color+(alpha,),width=4)
        for x,y,z,w in points:
            x,y=(x-640)*2,(y-25)*2
            d.ellipse((x-3,y-3,x+3,y+3),fill=(200,235,245,210))
        glow=overlay.filter(ImageFilter.GaussianBlur(6))
        glow.alpha_composite(overlay)
        glow=glow.resize((560,350),Image.Resampling.LANCZOS)
        im=base.copy()
        im.paste(glow,(640,25),glow)
        frames.append(im)
    # A common palette keeps all static header text stable between frames.
    palette=frames[0].quantize(colors=192)
    quantized=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    quantized[0].save(ASSETS/'hero.gif',save_all=True,append_images=quantized[1:],duration=50,loop=0,optimize=True,disposal=1)
    frames[0].save(ASSETS/'hero-still.png')
    first=geometry(0)
    lines=''.join(f'<line x1="{first[a][0]:.3f}" y1="{first[a][1]:.3f}" x2="{first[b][0]:.3f}" y2="{first[b][1]:.3f}" stroke="'+('#6EE7D8' if first[a][3]+first[b][3]<0 else '#A99BFF')+'" stroke-width="1.5"/>' for a,b in EDGES)
    source=(ASSETS/'hero-base.svg').read_text(encoding='utf-8')
    (ASSETS/'hero.svg').write_text(source.replace('</svg>',lines+'</svg>'),encoding='utf-8')
    print('Animated 16 vertices / 32 edges / 96 frames; seamless 4.8-second loop.')

if __name__=='__main__': main()
