from PIL import Image, ImageDraw, ImageFont
import os
OUT=os.path.dirname(os.path.abspath(__file__))
def font(sz):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()
F16, F20, F24 = font(16), font(20), font(24)
BLUE=(0,114,186); DARK=(15,23,42); GRAY=(203,213,225); LGRAY=(148,163,184); LBLUE=(224,242,254); RED=(220,38,38)

def save(im,nm):
    p=os.path.join(OUT,nm); im.save(p); print(nm, os.path.getsize(p))

# S2 branch: 1 spec -> 3 clients
im=Image.new("RGB",(640,440),"white"); d=ImageDraw.Draw(im)
d.rectangle([30,180,150,260],fill=BLUE,outline=BLUE)
d.text((48,212),"SPEC",fill="white",font=F20)
for i,(y,lb) in enumerate([(60,"Client A"),(180,"Client B"),(300,"Client C")]):
    d.rectangle([380,y,600,y+80],fill="white",outline=BLUE,width=3)
    d.text((400,y+28),lb,fill=DARK,font=F20)
    d.line([150,220,270,220+i*0 if False else 220],fill=BLUE,width=3)
    d.line([150,220,380,y+40],fill=BLUE,width=3)
d.text((30,390),"one spec -> three implementations",fill=LGRAY,font=F16)
save(im,"fig_s2_branch.png")

# S3 venn: two 2/3 circles overlap
im=Image.new("RGB",(640,440),"white"); d=ImageDraw.Draw(im)
d.ellipse([90,70,370,350],outline=BLUE,width=4)
d.ellipse([270,70,550,350],outline=BLUE,width=4)
# overlap highlight: small ellipse approx
d.ellipse([230,130,410,290],fill=LBLUE,outline=None)
d.text((150,200),"2/3",fill=BLUE,font=F24)
d.text((450,200),"2/3",fill=BLUE,font=F24)
d.text((252,190),"overlap",fill=DARK,font=F20)
d.text((252,218),"= slash",fill=RED,font=F20)
d.text((120,390),"two quorums always overlap (2/3+2/3>100%)",fill=LGRAY,font=F16)
save(im,"fig_s3_venn.png")

# S5 arrow: assumption -> conclusion
im=Image.new("RGB",(640,440),"white"); d=ImageDraw.Draw(im)
d.rectangle([30,150,270,290],fill=LBLUE,outline=BLUE,width=3)
d.text((55,185),"ASSUMPTION",fill=DARK,font=F20)
d.text((55,220),"= premises",fill=DARK,font=F16)
d.text((55,245)," (args list)",fill=LGRAY,font=F16)
d.rectangle([370,150,610,290],fill="white",outline=DARK,width=3)
d.text((395,185),"CONCLUSION",fill=DARK,font=F20)
d.text((395,220),"safety",fill=DARK,font=F16)
d.polygon([(270,220),(370,200),(370,240)],fill=BLUE)
d.line([270,220,370,220],fill=BLUE,width=4)
d.text((150,330),"deterministic extraction, no LLM",fill=LGRAY,font=F16)
save(im,"fig_s5_arrow.png")

# S7 grid: 57 cells, 48 gray 9 white, note E=0
im=Image.new("RGB",(640,440),"white"); d=ImageDraw.Draw(im)
cols,rows=19,3; cw,ch=28,60; ox,oy=54,60
for i in range(57):
    c,r=i%cols,i//cols
    x0,y0=ox+c*cw,oy+r*ch
    fill=(148,163,184) if i<48 else "white"
    d.rectangle([x0,y0,x0+cw-4,y0+ch-8],fill=fill,outline=DARK,width=1)
d.text((54,270),"48 gray = non-E (unanimous) / 9 white = split",fill=DARK,font=F16)
d.text((54,300),"unanimous E = 0",fill=RED,font=F20)
d.text((54,340),"57 premises, 48 (84.2%) non-E",fill=LGRAY,font=F16)
save(im,"fig_s7_grid.png")
