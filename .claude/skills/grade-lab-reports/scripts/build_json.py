#!/usr/bin/env python3
"""由逐人逐题打分记录生成成绩 JSON，并统一处理抄袭封顶。
用法: python3 -I build_json.py <scores.json> <输出成绩.json>
scores.json: [{"姓名","学号","题分":[[完成,正确],...],"报告":n,"评语":"...","封顶":70(可选)}]
"""
import json,sys,collections
cfg=json.load(open(sys.argv[1],encoding='utf8'))
CAP=cfg.get('分值',{'完成度':[15,15,15,15],'正确性':[6,6,10,8],'报告':10})
out=[]
for e in cfg['学生']:
    q=e['题分']
    for k,(a,b) in enumerate(q):
        assert a<=CAP['完成度'][k] and b<=CAP['正确性'][k],(e['姓名'],k+1)
    assert e['报告']<=CAP['报告'],e['姓名']
    raw=sum(a+b for a,b in q)+e['报告']; s=min(raw,e['封顶']) if e.get('封顶') else raw
    d={f'第{k+1}题':{'完成度':a,'正确性':b} for k,(a,b) in enumerate(q)}; d['报告']=e['报告']
    r={'姓名':e['姓名'],'学号':e['学号'],'分数':s,'明细':d,'评语':e['评语']}
    if e.get('封顶') and raw>e['封顶']: r['封顶前分数']=raw
    out.append(r)
json.dump(out,open(sys.argv[2],'w',encoding='utf8'),ensure_ascii=False,indent=2)
sc=sorted(x['分数'] for x in out)
print(len(sc),'人 平均',round(sum(sc)/len(sc),1),'中位',sc[len(sc)//2],'区间',collections.Counter(min(x//10*10,90) for x in sc))
