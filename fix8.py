import json
d=json.load(open('data-1023.json'))
p=[x for x in d['products'] if x['id']=='imp-yw-xxa8'][0]
f=p['fields']

# 1. 费率表（官方PDF逐档核对）
tab={'50-55':(168,260,318,990),'56-60':(238,288,378,1088),'61-65':(288,356,428,1186),
     '66-75':(318,378,468,1268),'76-80':(368,488,'598(仅限续保)',None)}
rates=[]
for g,(a,b,c,dd) in tab.items():
    lo,hi=g.split('-')
    plans=[('计划一',a),('计划二',b),('计划三',c),('计划四',dd)]
    for name,v in plans:
        if v is None: continue
        r={'min':int(lo),'max':int(hi),'plan':name,'premium':v}
        if isinstance(v,str): r['note']='仅限续保'
        rates.append(r)
p['rates']=rates
p['ratesSource']='官方费率表PDF（2026-10-29 逐档录入）'

# 2. sumInsured
f['sumInsured']=('意外身故/伤残：计划一2万 / 计划二10万 / 计划三、四20万；意外医疗：四计划统一10万（不限社保）；'
 '交通叠加（计划二以上）：计划二飞机/轨道/轮船各10万+客运及非营运机动车5万，计划三/四各20万+10万；'
 '猝死慰问金1000元（计划二以上）；骨折金：2000/3000/3000/5000元；救护车：0/1000/1500/1500元；'
 '异地亲属探望：0/3000/3000/5000元')

# 3. 修正住院津贴：官方须知为常规单次≤15天、ICU单次≤30天（不叠加）
f['hospitalAllow']=[
 '住院津贴0免赔天数：计划一 50元/天 / 计划二三四 100元/天；常规住院单次≤15天，年度累计180天',
 'ICU津贴：100/200/200/300元每天（计划一至四），单次≤30天、累计180天；与常规住院津贴不叠加'
]

# 4. 追加核验note
f['note'].append('[条款核验] 计划一免责条款明确「猝死」不赔——猝死慰问金仅计划二以上附加；且计划一医疗未走社保只报70%（计划二以上80%）')
f['note'].append('[条款核验] 计划三投保地区受限：仅限北上广深杭等指定城市名单（与计划一/二/四全国可投不同）；持孝心安5/6号有效保单可连续投保')
f['note'].append('[条款核验] 异地亲属探望需连续住院超过3天、异地需跨市级行政区，报销住宿/餐饮/交通但不含返程')
f['note'].append('[条款核验] 计划四普通部0免赔，特需部另算：年限额1万、每次免赔200、赔60%；意外身故报案需36小时内')
f['updatedAt']=20261029

json.dump(d,open('data-1023.json','w'),ensure_ascii=False,indent=1)
# 回读断言
d2=json.load(open('data-1023.json'))
p2=[x for x in d2['products'] if x['id']=='imp-yw-xxa8'][0]
print('rates档数:',len(p2['rates']),'| 76-80计划三note:',[r.get('note') for r in p2['rates'] if r['min']==76 and r['plan']=='计划三'])
print('note条数:',len(p2['fields']['note']))
print('sumInsured前40:',p2['fields']['sumInsured'][:40])
