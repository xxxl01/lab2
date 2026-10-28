#!/usr/bin/env python3
"""全班图片查重: 逐张比对, 输出两两相同图片数。
用法: python3 -I similarity.py <输出目录1> [<输出目录2> ...]   (即 extract.py 的输出目录, 每人在 <目录>/<学号>/m 下)
结果只是线索: 版式相同的截图(同样的Visio窗口)会有误报, 必须人工并排看图确认;
手机重新拍屏的同一张图可能漏检, 需人工补充。"""
import os,glob,hashlib,itertools,sys,collections
from PIL import Image,ImageFilter,ImageOps
import numpy as np
TPL=set(os.environ.get('TPL_HASHES','').split(','))
def feat(im):
    g=ImageOps.autocontrast(im.convert('L')).resize((128,128),Image.LANCZOS)
    a=255-np.asarray(g.filter(ImageFilter.GaussianBlur(2)),dtype=float); a=a-a.mean(); n=np.linalg.norm(a); return (a/n).flatten()
imgs=collections.defaultdict(list)
for base in sys.argv[1:]:
    for sid in sorted(os.listdir(base)):
        seen=set()
        for q in glob.glob(f'{base}/{sid}/m/**/*',recursive=True):
            if not os.path.isfile(q): continue
            try: im=Image.open(q); im.load()
            except Exception: continue
            if im.size[0]<250 or im.size[1]<250: continue
            h=hashlib.md5(open(q,'rb').read()).hexdigest()[:8]
            if h in TPL or h in seen: continue
            seen.add(h); imgs[sid].append((os.path.basename(q),feat(im),im.size,h))
for a,b in itertools.combinations(sorted(imgs),2):
    m=[]
    for i,(fa,va,sa,ha) in enumerate(imgs[a]):
        for j,(fb,vb,sb,hb) in enumerate(imgs[b]):
            ra,rb=sa[0]/sa[1],sb[0]/sb[1]
            c=float(va@vb)
            if abs(ra-rb)/max(ra,rb)<0.15 and c>=0.985: m.append((fa,fb,round(c,3),'同文件' if ha==hb else '相似'))
    if m: print(a,b,f'{len(m)}张/{len(imgs[a])}vs{len(imgs[b])}',m)
