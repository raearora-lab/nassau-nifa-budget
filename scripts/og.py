from PIL import Image, ImageDraw, ImageFont, ImageFilter
G="/usr/share/fonts/truetype/sand-box/google/"
def fr(sz):
    f=ImageFont.truetype(G+"Fraunces/Fraunces-VariableFont_SOFT,WONK,opsz,wght.ttf",sz)
    try: f.set_variation_by_axes([144,900,0,0])
    except Exception:
        try: f.set_variation_by_name("Black")
        except Exception: pass
    return f
mono=ImageFont.truetype(G+"IBM Plex Mono/IBMPlexMono-Bold.ttf",22)
W,H=1200,630
glow=Image.new("RGB",(W,H),"#000"); g=ImageDraw.Draw(glow)
img=Image.new("RGB",(W,H),"#000"); d=ImageDraw.Draw(img)
def both(fn):
    fn(g); fn(d)
L,P,T,B="#c8ff00","#ff2d6a","#00ffd0","#7eb0ff"
items=[(lambda c:c.text((60,52),"WHO RUNS NY · NASSAU VS NIFA",font=mono,fill=T)),
(lambda c:c.text((60,100),"Nassau County",font=fr(92),fill=L)),
(lambda c:c.text((60,200),"Budget vs NIFA",font=fr(92),fill=L)),
(lambda c:c.text((60,345),"$755.3M",font=fr(70),fill=L)),
(lambda c:c.text((440,345),"$145.5M",font=fr(70),fill=P)),
(lambda c:c.text((820,345),"Nov 19",font=fr(70),fill=B))]
for f in items: both(f)
glow=glow.filter(ImageFilter.GaussianBlur(14))
img=Image.blend(img,glow,0.0); 
from PIL import ImageChops
img=ImageChops.add(img,glow.point(lambda v:int(v*0.7)))
d=ImageDraw.Draw(img)
for x,t in ((60,"LEVY, FROZEN FY22–FY27"),(440,"NIFA FY27 RISK, HIGH"),(820,"NIFA VOTE ON FY27 PLAN")):
    d.text((x,440),t,font=mono,fill="#8a8a94")
d.text((60,540),"FY2017–FY2027 · NIFA's 7 recommendations · every NIFA figure · updated Nov 14, 2026",font=ImageFont.truetype(G+"IBM Plex Mono/IBMPlexMono-Medium.ttf",20),fill="#f4f4f0")
d.ellipse((1110,60,1126,76),fill=P)
img.save("public/og.png",optimize=True); print("ok")
