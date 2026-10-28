#!/usr/bin/env python3
"""平台导出的 .doc 其实是 WordML(XML)，学生答案可能以 base64 嵌在里面。
用法: python3 -I extract_b64.py <某个.doc> <输出目录>"""
import re,base64,sys,os
t=open(sys.argv[1],encoding='utf-8-sig',errors='ignore').read(); os.makedirs(sys.argv[2],exist_ok=True)
for i,m in enumerate(re.finditer(r'(/9j/[A-Za-z0-9+/=\s]+|iVBORw0KGgo[A-Za-z0-9+/=\s]+)',t)):
    s=re.sub(r'\s','',m.group(1)); b=base64.b64decode(s+'='*(-len(s)%4))
    p=f'{sys.argv[2]}/img{i}.'+('jpg' if b[:2]==b'\xff\xd8' else 'png'); open(p,'wb').write(b); print(p,len(b))
