from forward_trial import *

def load(rel):
    return json.loads((ROOT/rel).read_text(encoding="utf-8"))

spec=load("scope.json")
new=load("materials/result-current.json")
new["phase2"]["sensitivity"]="RR=1.020000; 95%CI=[1.000400,1.039984]"
write("materials/result-current.json",new)
md=ROOT/"materials/discussion.md"
md.write_text(md.read_text(encoding="utf-8")+"加权敏感性分析RR=1.02; 95%CI=[1.00,1.04]。\n",encoding="utf-8")
inv={x["id"]:read_document(x["path"]) for x in spec["files"]}
write("inventory-before.json",inv)
write("original-hashes.json",{x["id"]:hashfile(x["path"]) for x in spec["files"]})
counter=0
def b(file,locator,pattern=None,**more):
    global counter
    counter+=1
    assert any(x["locator"]==locator for x in inv[file]["units"]), (file,locator)
    v={"id":f"binding-{counter}","file":file,"locator":locator,
       "reason":"实际阅读该位置上下文，按阶段、样本、模型、单位和结局确认对应"}
    if pattern:v["pattern"]=pattern
    v.update(more)
    return v

def ident(stat,sample="正式试验全部240名随机分组学生",model="描述统计",unc="不适用",unit="人数"):
    return dict(outcome="8周课程完成",comparison="干预组相对对照组" if "RR" in stat else "不适用",
        timepoint="第8周",sample=sample,statistic=stat,unit=unit,model=model,
        adjustments="基线协变量" if model=="基线协变量调整" else "不适用",
        analysis="敏感性" if model=="加权" else "主分析",uncertainty=unc)

def fact(id,source,occ,identity,authority=True):
    v={"id":id,"identity":identity,"mapping_reason":"依据合成研究两阶段设计与当前材料明确标签逐处确认",
       "sources":[source],"occurrences":occ}
    if authority:v["authority"]={"source":source["id"],"kind":"user_confirmed","reason":"本次请求明确指定 result-current.json 中同一分析记录；不凭文件时间或显著性选择"}
    spec["facts"].append(v)

rate_scale={"scale":.01,"conversion_reason":"同一组、同一正式试验、同一8周完成率，百分数除以100得到比例","display_decimals":1}
for phase,key,value,label,docpattern,pptloc,pptpattern,mdpattern in [
 ("phase1","n",48,"pilot-total",r"先导阶段纳入(?P<value>48)人","ppt:1:sample/body/0:text",r"先导阶段 n=(?P<value>\d+)",None),
 ("phase1","survey_n",42,"pilot-survey",r"其中(?P<value>\d+)人完成问卷","ppt:1:sample/body/0:text",r"问卷 n=(?P<value>\d+)",r"先导阶段问卷有效样本为(?P<value>\d+)人"),
 ("phase2","n",240,"formal-total",r"正式试验纳入(?P<value>\d+)人","ppt:1:sample/body/1:text",r"正式试验 n=(?P<value>\d+)",None),
 ("phase2","survey_n",196,"formal-survey",r"问卷有效样本为(?P<value>\d+)人","ppt:1:sample/body/1:text",r"问卷 n=(?P<value>\d+)",r"正式试验问卷有效样本为(?P<value>\d+)人")]:
    occ=[b("doc","docx:p:1",docpattern),b("ppt",pptloc,pptpattern)]
    if mdpattern:occ.append(b("md","line:5",mdpattern))
    fact(label,b("new",f"json:/{phase}/{key}"),occ,ident("n",sample=("先导阶段" if phase=="phase1" else "正式试验")+("问卷有效样本" if key=="survey_n" else "全部样本")))
fact("treated-rate",b("new","json:/phase2/rate_treated",guards=[
 {"locator":"json:/phase2/outcome","equals":"8周课程完成"},{"locator":"json:/phase2/sample","equals":"正式试验全部随机分组学生"}]),[
 b("doc","docx:p:2",r"干预组(?P<value>[\d.]+)%",**rate_scale),
 b("csv","csv:2:6",guards=[{"locator":"csv:2:2","equals":"全部240人"},{"locator":"csv:2:5","equals":"干预组完成率"}],**rate_scale),
 b("md","line:2",r"干预组课程完成率(?P<value>[\d.]+)%",**rate_scale),
 b("ppt","ppt:2:completion/body/0:text",r"干预组(?P<value>[\d.]+)%",**rate_scale),
 b("ppt","ppt:2:completion/visual/chart:series:0:value:0",guards=[
 {"locator":"ppt:2:completion/visual/chart:category:0","equals":"干预组"},
 {"locator":"ppt:2:completion/visual/chart:axis:title","equals":"%"}],**rate_scale),
 b("ppt","ppt:2:notes",r"干预组(?P<value>[\d.]+)%",**rate_scale),
 b("plan","json:/slides/1/body/0",r"干预组(?P<value>[\d.]+)%",**rate_scale),
 b("plan","json:/slides/1/visual/series/0/values/0",**rate_scale),
 b("plan","json:/slides/1/notes",r"干预组(?P<value>[\d.]+)%",**rate_scale)],ident("完成比例",unit="比例"))
fact("control-rate",b("new","json:/phase2/rate_control"),[
 b("doc","docx:p:2",r"对照组(?P<value>[\d.]+)%",**rate_scale),
 b("csv","csv:3:6",**rate_scale),
 b("md","line:2",r"对照组为(?P<value>[\d.]+)%",**rate_scale),
 b("ppt","ppt:2:completion/visual/chart:series:0:value:1",**rate_scale)],ident("完成比例",unit="比例"))
rrpat=r"RR=(?P<value>[\d.]+); 95%CI=\[(?P<low>[\d.]+),(?P<high>[\d.]+)\]"
fact("primary-rr",b("new","json:/phase2/rr",rrpat,reference_values=[1],guards=[
 {"locator":"json:/phase2/model","equals":"未调整风险比"}]),[
 b("doc","docx:p:2",rrpat),b("doc","docx:p:9",rrpat,guards=[{"locator":"docx:p:8","equals":"未调整RR"}]),
 b("csv","csv:4:6",rrpat,guards=[{"locator":"csv:4:4","equals":"未调整风险比"}]),b("md","line:3",rrpat),
 b("ppt","ppt:3:effect/body/0:text",rrpat),b("plan","json:/slides/2/body/0",rrpat)],
 ident("RR",model="未调整风险比",unit="比值",unc="95%置信区间"))
fact("adjusted-rr",b("new","json:/phase2/adjusted",rrpat,reference_values=[1]),[
 b("doc","docx:p:12",rrpat,guards=[{"locator":"docx:p:11","equals":"调整RR"}]),
 b("csv","csv:5:6",rrpat,guards=[{"locator":"csv:5:4","equals":"基线协变量调整"}]),b("md","line:6",rrpat),
 b("ppt","ppt:3:effect/visual/table:cell:1:1",r"(?P<value>[\d.]+) \[(?P<low>[\d.]+),(?P<high>[\d.]+)\]",display_decimals=2)],
 ident("RR",model="基线协变量调整",unit="比值",unc="95%置信区间"))
fact("sensitivity-rr",b("new","json:/phase2/sensitivity",rrpat,reference_values=[1]),[
 b("md","line:10",rrpat,display_decimals=2)],ident("RR",model="加权",unit="比值",unc="95%置信区间"))
fact("unknown-subgroup",b("md","line:7",r"完成率(?P<value>[\d.]+)%"),[],
 ident("完成比例",sample="未决：分母和组别待作者确认",unit="%"),False)
for file,loc,id in [("doc","docx:p:3","abstract-interpretation"),("md","line:4","discussion-recommendation"),
 ("md","line:8","discussion-cautious"),("ppt","ppt:3:effect/message:text","ppt-headline"),
 ("ppt","ppt:3:notes","ppt-interpretation"),("plan","json:/slides/2/message","plan-headline"),
 ("plan","json:/slides/2/notes","plan-interpretation")]:
    spec["dependencies"].append({"id":id,"depends_on":["primary-rr"],"target":b(file,loc),
      "reason":"解释依赖未调整风险比及区间是否覆盖无效应参考值1"})
spec["citations"].append({"id":"citation-SYN-01","reference_id":"SYN-01","reader":"independent forward-testing reader",
 "claim":b("md","line:9"),"support":b("reading","line:2"),"source_file":"reading","ledger_file":"ledger"})
write("spec.json",spec)
r=command("01-register",CHECK,"register","--project",ROOT/"project","--spec",ROOT/"spec.json")
if r.returncode:raise RuntimeError(r.stderr)
report=load("project/edu_output/project/check.json")
write("reports/01-first-use-check.json",report)
shutil.copy2(ROOT/"project/edu_output/project/check.md",ROOT/"reports/01-first-use-check.md")
write("reports/01-check-only-hashes.json",{
 "unchanged":{x["id"]:hashfile(x["path"])==load("original-hashes.json")[x["id"]] for x in spec["files"]},
 "counts":{status:sum(x["status"]==status for x in report["findings"]) for status in ["stale","review","consistent","unchecked"]},
 "dependency_findings":[x for x in report["findings"] if "dependency_id" in x]})
print(json.dumps(load("reports/01-check-only-hashes.json"),ensure_ascii=True))
