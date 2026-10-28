#!/usr/bin/env python3
"""提取学生报告里的答案图，并为每人拼一张总览图 sheet.png。
用法: python3 -I extract.py <仓库根目录> <输出目录> <学号1> <学号2> ...
文件夹命名为 "<学号>-<姓名>"。支持 docx；.doc 先用 soffice 转 docx。
平台导出的 .doc(XML) 里可能嵌 base64 图片(如只交了这种文件的学生)，用 extract_b64.py 处理。
需要 pandoc、soffice、Pillow。"""
import sys,os,subprocess,hashlib,glob,shutil,re
from PIL import Image, ImageDraw
root,out=sys.argv[1],sys.argv[2]; ids=sys.argv[3:]
# 题目文档自带的图(md5前8位)，运行时按实际题目文档补充
TPL=set(os.environ.get('TPL_HASHES','').split(','))
for sid in ids:
    d=glob.glob(f'{root}/{sid}-*')[0]
    files=[f for f in os.listdir(d) if not f.startswith(('软件学院','.'))]
    o=f'{out}/{sid}'; os.makedirs(o,exist_ok=True)
    print('==',os.path.basename(d),files)
    docx=[f for f in files if f.endswith('.docx')]; doc=[f for f in files if f.endswith('.doc')]
    if docx: src=f'{d}/{docx[0]}'
    elif doc:
        shutil.copy(f'{d}/{doc[0]}',f'{o}/a.doc')
        subprocess.run(['soffice','--headless','--convert-to','docx','--outdir',o,f'{o}/a.doc'],capture_output=True); src=f'{o}/a.docx'
    else: print('  NO REPORT'); continue
    if not os.path.exists(src): print('  CONVERT FAILED'); continue
    r=subprocess.run(['pandoc',src,'-t','markdown',f'--extract-media={o}/m'],capture_output=True,text=True)
    subprocess.run(['pandoc',src,'-t','plain','-o',f'{o}/t.txt'],capture_output=True)
    own=[]
    for p in re.findall(r'\(([^)\s]*media/[^)\s{]*)',r.stdout):
        q=p if os.path.exists(p) else f'{o}/m/{p}'
        if not os.path.exists(q): continue
        h=hashlib.md5(open(q,'rb').read()).hexdigest()[:8]
        if h in TPL: continue
        try: im=Image.open(q); im.load()
        except Exception: continue
        if im.size[0]<200 and im.size[1]<200: continue   # 校徽等小图
        own.append((q,im))
    print('  own images:',[(os.path.basename(q),im.size) for q,im in own])
    if not own: continue
    cols=2 if len(own)>1 else 1; rows=(len(own)+cols-1)//cols; W=1000; cells=[]
    for q,im in own:
        im=im.convert('RGB'); im=im.resize((W,int(im.size[1]*W/im.size[0])))
        if im.size[1]>760: im=im.resize((int(W*760/im.size[1]),760))
        cells.append(im)
    H=max(c.size[1] for c in cells)+30
    sheet=Image.new('RGB',(W*cols,H*rows),'white'); dr=ImageDraw.Draw(sheet)
    for k,c in enumerate(cells):
        x=(k%cols)*W; y=(k//cols)*H
        dr.text((x+5,y+5),f'#{k+1} {os.path.basename(own[k][0])}',fill='red'); sheet.paste(c,(x,y+25))
    sheet.save(f'{o}/sheet.png')
