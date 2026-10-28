"""方案A：缺第2题、但第1题完成度>=20的，保底60分（保留保底前分数）。用法: python3 -I apply_floor.py 成绩.json"""
import json,sys
p=sys.argv[1]; d=json.load(open(p,encoding='utf8')); n=0
for x in d:
    m=x['明细']
    if x['分数']>0 and m['第2题']['完成度']==0 and m['第1题']['完成度']>=20 and x['分数']<60:
        x['保底前分数']=x['分数']; x['分数']=60; n+=1
json.dump(d,open(p,'w',encoding='utf8'),ensure_ascii=False,indent=2)
print('保底人数',n)
