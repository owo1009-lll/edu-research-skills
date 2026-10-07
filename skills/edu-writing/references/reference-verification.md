# 引用核验

核验记录（ledger）由助理根据实际读过的来源在内部整理；用户只提供普通的论文和笔记，不需要了解这个格式。

## 1. 核实文献身份

- 通过出版社页面、DOI 注册机构或权威数据库确认。
- DOI 必须与预期的题名、作者、年份、刊名一致；DOI 有效但指向别的文献，算不匹配。
- 没有 DOI 的文献，需要实际读过的权威记录和稳定网址。中文文献在知网等数据库的核实由用户完成或提供条目。

运行：

```
python <本skill>/scripts/verify_references.py --ledger <ledger.json> --output <新的核验文件夹>
```

脚本记录 DOI 元数据、核查日期、阅读版本和更正声明状态。Crossref 在线查询失败会被记录；可以另行提供实际访问过的一手记录（权威网址、阅读者、位置、保存的证据路径及哈希、元数据），脚本按该记录核对字段。脚本只核对字段，不判断解读是否正确；在线查询不可用时不得标为成功。以前保存的注册记录保留其日期和范围；当前再向出版社核对是另一次独立操作。

## 2. ledger 格式

```
references=[{
  id, doi（可选）,
  expected: {title, year, venue, first_author},
  reading: {status: full_text|source_excerpt|abstract|secondary_citation, version, path, source_sha256},
  notice_check: {status, scope, checked_utc, required_reference_ids（可选）},
  primary_record（可选）: {provider, url, checked_utc, locator, reader, evidence_path, evidence_sha256, metadata}
}]
claims=[{block_id, reference_id, status: supported, locator, support, reader, claim_type（可选）}]
```

一手记录的 metadata 包括：doi 或 null、title、authors=[{family, given} 或 {name}]、year、registered_years、venue、volume/issue/pages、稳定 url。

## 3. 核实论断支撑

- 每条重要的事实、解释或数值论断，都实际读相关段落，写明它为什么支撑这条论断。
- 记录 PDF 页码或印刷页码、章节或段落、保存的行号；区分测得的发现、作者的解释和本文的推论。
- DOI 只解决身份，不解决论断是否有依据。
- 区分两种情况：论断明显没有依据或张冠李戴——改正；必要的来源暂时无法获取——记下具体的检索和阅读缺口。
- 修改原稿时，来源暂时读不到，也保留原有的有限定的理论论证和引文，继续追查来源；不要因为获取不全就删掉整段论证或换成套话。这些段落在外部来源记录中明确标为待查，不在 ledger 或打包流程里标为已核验；打包脚本不接受时，改用普通 Word 修订稿交付。
- 没有依据的新论断删去或收窄。
- ledger 中 `status=supported` 表示阅读者完成了有限范围的来源判断，不表示脚本验证了语义。
- 直接引语必须逐字准确，并写明说话人。只读过摘要的文献，不能支撑关于具体方法细节的论断。

## 4. 更正与撤稿

- 查看能访问到的出版社更正、更新链接和注册的更新与关联字段；已知更正作为证据的一部分，打包脚本可以要求列出其文献编号。
- 在查过的来源里没有看到声明，不等于保证没有撤稿。
- 未解决的日期、版本和获取缺口写进简短的待补说明；不承诺零错误。

## 5. 打包时的检查

正文中的 `[@id]` 按核验过的元数据转成可读引用和参考文献表（英文 APA 著者-出版年，中文 GB/T 7714 顺序编码）。打包脚本检查：正文与参考文献表（包括图表注释和表格单元格）是否一一对应、重复的编号或 DOI、已知更正的编号、来源支撑记录、同一作者同一年份的区分。这些机械检查不能替代实际阅读和全文评阅。
