from forward_trial import *
def load(rel):
    return json.loads((ROOT/rel).read_text(encoding="utf-8"))

# Same synthetic materials, fresh project, preserving the original failing report.
command("18-first-use-recheck",CHECK,"register","--project",ROOT/"fixed-first-use","--spec",ROOT/"spec.json")
fresh=load("fixed-first-use/edu_output/project/check.json")
write("reports/09-fixed-first-use.json",fresh)
shutil.copy2(ROOT/"fixed-first-use/edu_output/project/check.md",ROOT/"reports/09-fixed-first-use.md")
write("reports/09-fix-comparison.json",{
 "before_dependencies":len([x for x in load("reports/01-first-use-check.json")["findings"] if x.get("dependency_id")]),
 "after_dependencies":len([x for x in fresh["findings"] if x.get("dependency_id")]),
 "after_ids":[x["dependency_id"] for x in fresh["findings"] if x.get("dependency_id")]})

# Valid structured ledger baseline, unrelated update, and genuine claim expansion.
spec=load("spec.json")
ledger={"references":[{"id":"SYN-01","title":"虚构访谈研究","identity_verified":True}],
 "claims":[{"block_id":"citation-SYN-01","reference_id":"SYN-01","status":"supported",
            "reason":"访谈原文支持学生自述理解作业要求，不支持课程完成率变化"}]}
write("citation-probes/ledger.json",ledger)
claimpath=ROOT/"citation-probes/discussion.md"
shutil.copy2(ROOT/"materials/discussion.md",claimpath)
next(x for x in spec["files"] if x["id"]=="ledger")["path"]=str(ROOT/"citation-probes/ledger.json")
next(x for x in spec["files"] if x["id"]=="md")["path"]=str(claimpath)
write("citation-probes/spec.json",spec)
command("19-citation-structured-register",CHECK,"register","--project",ROOT/"citation-probes/project","--spec",ROOT/"citation-probes/spec.json")
write("reports/10-citation-baseline.json",load("citation-probes/project/edu_output/project/check.json"))
ledger["claims"].append({"block_id":"unrelated","reference_id":"SYN-OTHER","status":"pending","reason":"其他研究尚未阅读"})
write("citation-probes/ledger.json",ledger)
command("20-citation-unrelated-ledger",CHECK,"check","--project",ROOT/"citation-probes/project")
write("reports/11-citation-unrelated.json",load("citation-probes/project/edu_output/project/check.json"))
claimpath.write_text(claimpath.read_text(encoding="utf-8").replace(
 "同伴反馈帮助受访学生解释作业要求。[SYN-01]",
 "同伴反馈帮助受访学生解释作业要求，并显著提高了课程完成率。[SYN-01]"),encoding="utf-8")
command("21-citation-expanded-valid-ledger",CHECK,"check","--project",ROOT/"citation-probes/project")
write("reports/12-citation-expansion.json",load("citation-probes/project/edu_output/project/check.json"))

# A mixed paragraph is a natural precision boundary: one known, one unresolved
# completion rate. The request intentionally tries both; the tool says it rejects
# ambiguous locations and should not allow the unresolved edit.
spec0=load("spec.json")
mixed={"files":[deepcopy(next(x for x in spec0["files"] if x["id"]=="new")),
 {"id":"md","path":str(ROOT/"mixed-probe/discussion.md"),"role":"一个已确认值与一个待作者判断值共处的段落"}],
 "facts":[],"dependencies":[],"citations":[]}
(ROOT/"mixed-probe").mkdir(exist_ok=True)
before="正式试验干预组课程完成率70.0%；某子组课程完成率70.0%，分母和组别待确认。"
(ROOT/"mixed-probe/discussion.md").write_text(before+"\n",encoding="utf-8")
known=deepcopy(next(x for x in spec0["facts"] if x["id"]=="treated-rate"))
known["occurrences"]=[deepcopy(next(x for x in known["occurrences"] if x["file"]=="md"))]
known["occurrences"][0]["locator"]="line:1"
unknown=deepcopy(next(x for x in spec0["facts"] if x["id"]=="unknown-subgroup"))
unknown["sources"][0]["locator"]="line:1"
unknown["sources"][0]["pattern"]=r"某子组课程完成率(?P<value>[\d.]+)%"
mixed["facts"]=[known,unknown]
write("mixed-probe/spec.json",mixed)
command("22-mixed-paragraph-register",CHECK,"register","--project",ROOT/"mixed-probe/project","--spec",ROOT/"mixed-probe/spec.json")
mr=load("mixed-probe/project/edu_output/project/check.json")
write("reports/13-mixed-location-before.json",mr)
req={"authorization":"同步修改已确定的旧内容，保留原件；歧义不要替我决定。",
 "report_fingerprint":mr["input_fingerprint"],
 "edits":[{"file":"md","output":str(ROOT/"mixed-probe/unsafe-attempt.md"),"replacements":[{
 "locator":"line:1","before":before,"old":before,"new":before.replace("70.0%","65.0%"),
 "reason":"测试内部误把同段未决子组一并同步时，工具所承诺的歧义阻断是否生效"}]}]}
write("mixed-probe/request.json",req)
r=command("23-mixed-paragraph-sync",CHECK,"sync","--project",ROOT/"mixed-probe/project","--request",ROOT/"mixed-probe/request.json")
write("reports/14-mixed-location-result.json",{"returncode":r.returncode,
 "output_exists":(ROOT/"mixed-probe/unsafe-attempt.md").exists(),
 "output":(ROOT/"mixed-probe/unsafe-attempt.md").read_text(encoding="utf-8") if (ROOT/"mixed-probe/unsafe-attempt.md").exists() else None,
 "expected":"拒绝替作者决定未决子组的值","request":str(ROOT/"mixed-probe/request.json")})
print("Mixed paragraph returncode:",r.returncode)
