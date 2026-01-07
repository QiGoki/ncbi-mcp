# NCBI E-utilities API 完整总结

本文档基于 NCBI E-utilities 官方文档，对每个工具的**简介、参数、URL 示例、返回示例**进行系统梳理，方便开发者快速调用。

## 通用参数说明

所有 E-utility 请求建议携带以下参数，用于合规和身份标识：



| 参数        | 说明          | 要求                  |
| --------- | ----------- | ------------------- |
| `tool`    | 调用工具 / 应用名称 | 字符串，无空格             |
| `email`   | 用户邮箱        | 有效邮箱，无空格            |
| `api_key` | API 密钥      | 单 IP 每秒请求超 3 次时建议携带 |

## 1. EInfo

### 简介

用于获取**所有有效 Entrez 数据库列表**，或**单个数据库的统计信息**（包括索引字段、可用链接名）。

### 参数



| 类型 | 参数        | 说明        | 必填 | 取值                                              |
| -- | --------- | --------- | -- | ----------------------------------------------- |
| 可选 | `db`      | 目标数据库     | 否  | 有效 Entrez 数据库名（如 `pubmed` `protein`）            |
| 可选 | `version` | 指定 XML 版本 | 否  | `2.0`（返回含 `<IsTruncatable>` `<IsRangeable>` 字段） |
| 可选 | `retmode` | 返回格式      | 否  | `xml`（默认）、`json`                                |

### URL 示例



1. 获取所有数据库列表



```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi
```



1. 获取 Protein 数据库的 2.0 版本统计信息



```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?db=protein\&version=2.0
```

### 返回示例（XML 格式，简化版）



```
\<?xml version="1.0" encoding="UTF-8" ?>

\<!DOCTYPE eInfoResult PUBLIC "-//NLM//DTD eInfoResult, 11 May 2002//EN" "https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20020511/eInfoResult.dtd">

\<eInfoResult>

&#x20; \<DbList>

&#x20;   \<DbName>pubmed\</DbName>

&#x20;   \<DbName>protein\</DbName>

&#x20;   \<DbName>nucleotide\</DbName>

&#x20; \</DbList>

\</eInfoResult>
```

## 2. ESearch

### 简介

根据文本查询词获取匹配的 UID 列表，支持将结果存入 History 服务器，或合并 / 筛选 History 中的 UID 集合。

### 参数



| 类型   | 参数                | 说明               | 必填 | 取值                                          |
| ---- | ----------------- | ---------------- | -- | ------------------------------------------- |
| 必填   | `db`              | 目标数据库            | 是  | 有效 Entrez 数据库名，默认 `pubmed`                  |
| 必填   | `term`            | 检索词              | 是  | URL 编码的检索式（如 `asthma[title]`）               |
| 历史相关 | `usehistory`      | 是否存入 History 服务器 | 否  | `y`（是）、`n`（否）                               |
| 历史相关 | `WebEnv`          | 历史环境字符串          | 否  | 来自前序 ESearch/EPost/ELink 的返回值               |
| 历史相关 | `query_key`       | 历史查询键            | 否  | 整数，需配合 `WebEnv` 使用                          |
| 检索控制 | `retstart`        | 结果起始位置           | 否  | 整数，默认 0                                     |
| 检索控制 | `retmax`          | 返回结果数量           | 否  | 整数，默认 20，最大 10000                           |
| 检索控制 | `rettype`         | 返回类型             | 否  | `uilist`（默认，返回 UID 列表）、`count`（仅返回计数）       |
| 检索控制 | `retmode`         | 返回格式             | 否  | `xml`（默认）、`json`                            |
| 检索控制 | `sort`            | 排序方式             | 否  | 因数据库而异，如 PubMed 支持 `pub_date` `relevance`   |
| 检索控制 | `field`           | 限定检索字段           | 否  | 如 `title` `author`                          |
| 日期过滤 | `datetype`        | 日期类型             | 否  | `mdat`（修改日期）、`pdat`（发表日期）、`edat`（Entrez 日期） |
| 日期过滤 | `reldate`         | 最近 N 天           | 否  | 整数，配合 `datetype` 使用                         |
| 日期过滤 | `mindate/maxdate` | 日期范围             | 否  | 格式 `YYYY/MM/DD` `YYYY` `YYYY/MM`            |

### URL 示例



1. 检索 PubMed 中近 60 天与 cancer 相关的文献，返回前 100 条并存入 History



```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed\&term=cancer\&reldate=60\&datetype=edat\&retmax=100\&usehistory=y
```



1. 检索 PNAS 期刊第 97 卷的文献，从第 7 条开始返回 6 条



```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed\&term=PNAS\[ta]+AND+97\[vi]\&retstart=6\&retmax=6\&tool=biomed3
```

### 返回示例（XML 格式，简化版）



```
\<?xml version="1.0" encoding="UTF-8" ?>

\<!DOCTYPE eSearchResult PUBLIC "-//NLM//DTD eSearchResult, 21 May 2002//EN" "https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20020521/eSearchResult.dtd">

\<eSearchResult>

&#x20; \<Count>12345\</Count>

&#x20; \<RetMax>100\</RetMax>

&#x20; \<RetStart>0\</RetStart>

&#x20; \<IdList>

&#x20;   \<Id>37567890\</Id>

&#x20;   \<Id>37567891\</Id>

&#x20; \</IdList>

&#x20; \<QueryKey>1\</QueryKey>

&#x20; \<WebEnv>NCID\_1\_23456\_7890\_123.45.67.890\_9001\</WebEnv>

\</eSearchResult>
```

## 3. EPost

### 简介

将 UID 列表上传到 Entrez History 服务器，或追加到已有的 Web 环境中，生成可用于后续工具的 `query_key` 和 `WebEnv`。

### 参数



| 类型 | 参数       | 说明         | 必填 | 取值                                          |
| -- | -------- | ---------- | -- | ------------------------------------------- |
| 必填 | `db`     | 目标数据库      | 是  | 有效 Entrez 数据库名，默认 `pubmed`                  |
| 必填 | `id`     | UID 列表     | 是  | 单个 UID 或逗号分隔的 UID 列表（如 `19393038,30242208`） |
| 可选 | `WebEnv` | 已有的历史环境字符串 | 否  | 来自前序 ESearch/EPost/ELink 的返回值               |

### URL 示例

向 PubMed 上传 2 个 PMID 并生成新的 Web 环境



```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi?db=pubmed\&id=11237011,12466850
```

### 返回示例（XML 格式，简化版）



```
\<?xml version="1.0" encoding="UTF-8" ?>

\<!DOCTYPE ePostResult PUBLIC "-//NLM//DTD ePostResult, 21 May 2002//EN" "https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20020521/ePostResult.dtd">

\<ePostResult>

&#x20; \<QueryKey>1\</QueryKey>

&#x20; \<WebEnv>NCID\_1\_98765\_4321\_98.76.54.321\_9001\</WebEnv>

\</ePostResult>
```

## 4. ESummary

### 简介

根据 UID 列表或 History 服务器中的 UID 集合，返回**文档摘要（DocSum）**，包含记录的核心元数据。

### 参数



| 类型         | 参数          | 说明        | 必填               | 取值                         |
| ---------- | ----------- | --------- | ---------------- | -------------------------- |
| 必填         | `db`        | 目标数据库     | 是                | 有效 Entrez 数据库名，默认 `pubmed` |
| UID 输入     | `id`        | UID 列表    | 否（与 History 二选一） | 单个 UID 或逗号分隔的 UID 列表       |
| History 输入 | `query_key` | 历史查询键     | 否（与 UID 二选一）     | 整数，需配合 `WebEnv`            |
| History 输入 | `WebEnv`    | 历史环境字符串   | 否（与 UID 二选一）     | 来自前序 ESearch/EPost/ELink   |
| 可选         | `retstart`  | 结果起始位置    | 否                | 整数，默认 1                    |
| 可选         | `retmax`    | 返回结果数量    | 否                | 整数，最大 10000                |
| 可选         | `retmode`   | 返回格式      | 否                | `xml`（默认）、`json`           |
| 可选         | `version`   | 指定 XML 版本 | 否                | `2.0`（返回数据库专属的详细 DocSum）   |

### URL 示例

获取 PubMed 中 2 个 PMID 的摘要



```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed\&id=11850928,11482001
```

### 返回示例（XML 格式，简化版）



```
\<?xml version="1.0" encoding="UTF-8" ?>

\<!DOCTYPE eSummaryResult PUBLIC "-//NLM//DTD eSummaryResult, 21 May 2002//EN" "https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20020521/eSummaryResult.dtd">

\<eSummaryResult>

&#x20; \<DocSum>

&#x20;   \<Id>11850928\</Id>

&#x20;   \<Item Name="Title" Type="String">A study on asthma treatment\</Item>

&#x20;   \<Item Name="AuthorList" Type="List">

&#x20;     \<Item Name="Author" Type="String">Smith J\</Item>

&#x20;   \</Item>

&#x20; \</DocSum>

\</eSummaryResult>
```

## 5. EFetch

### 简介

根据 UID 列表或 History 服务器中的集合，返回**格式化的完整记录**（如 PubMed 摘要、GenBank 序列、FASTA 序列等），是获取详细数据的核心工具。

### 参数



| 类型         | 参数                   | 说明      | 必填               | 取值                                                              |
| ---------- | -------------------- | ------- | ---------------- | --------------------------------------------------------------- |
| 必填         | `db`                 | 目标数据库   | 是                | 有效 Entrez 数据库名，默认 `pubmed`                                      |
| UID 输入     | `id`                 | UID 列表  | 否（与 History 二选一） | 单个 UID 或逗号分隔的 UID 列表                                            |
| History 输入 | `query_key`          | 历史查询键   | 否（与 UID 二选一）     | 整数，需配合 `WebEnv`                                                 |
| History 输入 | `WebEnv`             | 历史环境字符串 | 否（与 UID 二选一）     | 来自前序 ESearch/EPost/ELink                                        |
| 格式控制       | `retmode`            | 返回格式    | 否                | 因数据库而异，如 `xml` `text` `html` `fasta`                            |
| 格式控制       | `rettype`            | 返回类型    | 否                | 因数据库而异，如 PubMed 支持 `abstract` `medline`；Protein 支持 `gp` `fasta` |
| 可选         | `retstart`           | 结果起始位置  | 否                | 整数，默认 0                                                         |
| 可选         | `retmax`             | 返回结果数量  | 否                | 整数，最大 10000                                                     |
| 序列专属       | `strand`             | DNA 链方向 | 否                | `1`（正链）、`2`（负链）                                                 |
| 序列专属       | `seq_start/seq_stop` | 序列起止位置  | 否                | 整数，从 1 开始计数                                                     |
| 序列专属       | `complexity`         | 数据复杂度   | 否                | 0-4（0 = 完整数据，1 = 生物序列，依此类推）                                     |

### URL 示例



1. 获取 PubMed 中 2 个 PMID 的文本摘要



```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed\&id=17284678,9997\&retmode=text\&rettype=abstract
```



1. 获取核酸序列 GI=21614549 的前 100 个碱基的 FASTA 格式



```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore\&id=21614549\&strand=1\&seq\_start=1\&seq\_stop=100\&rettype=fasta\&retmode=text
```

### 返回示例（FASTA 格式）



```
\>gi|21614549|ref|NM\_000518.4| Homo sapiens TP53 (tumor protein p53), mRNA

ATGAGCCCAGCTCCTCCCCGCGCGCCGCTCGGGCGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCG

GCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGCGGC
```

## 6. ELink

### 简介

实现**数据库间 / 数据库内的 UID 关联**，例如从 Protein 链接到 Gene、从 PubMed 文献链接到相关文献；支持将结果存入 History 服务器，或查询 LinkOut 外部链接。

### 参数



| 类型         | 参数          | 说明            | 必填               | 取值                                                                       |
| ---------- | ----------- | ------------- | ---------------- | ------------------------------------------------------------------------ |
| 必填         | `db`        | 目标数据库（链接终点）   | 是                | 有效 Entrez 数据库名，默认 `pubmed`                                               |
| 必填         | `dbfrom`    | 源数据库（链接起点）    | 是                | 有效 Entrez 数据库名，默认 `pubmed`                                               |
| 必填         | `cmd`       | 命令模式          | 是                | `neighbor`（默认，返回关联 UID）、`neighbor_history`（存入 History）、`acheck`（查询可用链接）等 |
| UID 输入     | `id`        | 源 UID 列表      | 否（与 History 二选一） | 单个 UID 或逗号分隔的 UID 列表                                                     |
| History 输入 | `query_key` | 历史查询键         | 否（与 UID 二选一）     | 整数，需配合 `WebEnv`                                                          |
| History 输入 | `WebEnv`    | 历史环境字符串       | 否（与 UID 二选一）     | 来自前序 ESearch/EPost/ELink                                                 |
| 可选         | `retmode`   | 返回格式          | 否                | `xml`（默认）、`json`                                                         |
| 可选         | `linkname`  | 指定链接类型        | 否                | 格式 `dbfrom_db_subset`（如 `gene_snp_genegenotype`）                         |
| 可选         | `term`      | 过滤关联 UID 的检索词 | 否                | URL 编码的检索式，仅 `db=dbfrom` 时有效                                             |

### URL 示例



1. 从 Protein 数据库的 2 个 GI 链接到 Gene 数据库



```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=protein\&db=gene\&id=15718680,157427902
```



1. 查询 PubMed 文献 PMID=20210808 的相关文献并返回相似度评分



```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed\&db=pubmed\&id=20210808\&cmd=neighbor\_score
```

### 返回示例（XML 格式，简化版）



```
\<?xml version="1.0" encoding="UTF-8" ?>

\<!DOCTYPE eLinkResult PUBLIC "-//NLM//DTD eLinkResult, 21 May 2002//EN" "https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20020521/eLinkResult.dtd">

\<eLinkResult>

&#x20; \<LinkSet>

&#x20;   \<DbFrom>protein\</DbFrom>

&#x20;   \<IdList>

&#x20;     \<Id>15718680\</Id>

&#x20;   \</IdList>

&#x20;   \<LinkSetDb>

&#x20;     \<DbTo>gene\</DbTo>

&#x20;     \<Link>

&#x20;       \<Id>1234\</Id>

&#x20;     \</Link>

&#x20;   \</LinkSetDb>

&#x20; \</LinkSet>

\</eLinkResult>
```

## 7. EGQuery

### 简介

用**单个检索词查询所有 Entrez 数据库**，返回每个数据库的匹配记录数。

### 参数



| 类型 | 参数     | 说明  | 必填 | 取值                     |
| -- | ------ | --- | -- | ---------------------- |
| 必填 | `term` | 检索词 | 是  | URL 编码的检索式（如 `asthma`） |

### URL 示例

查询所有数据库中与 asthma 相关的记录数



```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/egquery.fcgi?term=asthma
```

### 返回示例（XML 格式，简化版）



```
\<?xml version="1.0" encoding="UTF-8" ?>

\<!DOCTYPE eGQueryResult PUBLIC "-//NLM//DTD eGQueryResult, 21 May 2002//EN" "https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20020521/eGQueryResult.dtd">

\<eGQueryResult>

&#x20; \<Result>

&#x20;   \<DbName>pubmed\</DbName>

&#x20;   \<Count>56789\</Count>

&#x20; \</Result>

&#x20; \<Result>

&#x20;   \<DbName>protein\</DbName>

&#x20;   \<Count>1234\</Count>

&#x20; \</Result>

\</eGQueryResult>
```

## 8. ESpell

### 简介

为指定数据库的检索词提供**拼写纠错建议**。

### 参数



| 类型 | 参数     | 说明      | 必填 | 取值                                  |
| -- | ------ | ------- | -- | ----------------------------------- |
| 必填 | `db`   | 目标数据库   | 是  | 有效 Entrez 数据库名，默认 `pubmed`          |
| 必填 | `term` | 待纠错的检索词 | 是  | URL 编码的检索式（如 `asthmaa+OR+alergies`） |

### URL 示例

纠正 PubMed 检索词 `asthmaa OR alergies` 的拼写



```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/espell.fcgi?db=pubmed\&term=asthmaa+OR+alergies
```

### 返回示例（XML 格式，简化版）



```
\<?xml version="1.0" encoding="UTF-8" ?>

\<!DOCTYPE eSpellResult PUBLIC "-//NLM//DTD eSpellResult, 21 May 2002//EN" "https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20020521/eSpellResult.dtd">

\<eSpellResult>

&#x20; \<CorrectedQuery>asthma OR allergies\</CorrectedQuery>

&#x20; \<SpelledQuery>asthmaa OR alergies\</SpelledQuery>

\</eSpellResult>
```

## 9. ECitMatch

### 简介

通过**引用信息字符串**批量检索对应的 PubMed ID（PMID）。

### 参数



| 类型 | 参数        | 说明      | 必填 | 取值           |
| -- | --------- | ------- | -- | ------------ |
| 必填 | `db`      | 目标数据库   | 是  | 仅支持 `pubmed` |
| 必填 | `rettype` | 返回格式    | 是  | 仅支持 `xml`    |
| 必填 | `bdata`   | 引用信息字符串 | 是  | 格式：\` 期刊名    |

### URL 示例

批量查询 2 条引用对应的 PMID



```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/ecitmatch.cgi?db=pubmed\&retmode=xml\&bdata=proc+natl+acad+sci+u+s+a|1991|88|3248|mann+bj|Art1|%0Dscience|1987|235|182|palmenberg+ac|Art2|
```

### 返回示例（XML 格式，简化版）



```
\<?xml version="1.0" encoding="UTF-8" ?>

\<!DOCTYPE CitMatchResult PUBLIC "-//NLM//DTD CitMatchResult, 21 May 2002//EN" "https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20020521/CitMatchResult.dtd">

\<CitMatchResult>

&#x20; \<Citation>

&#x20;   \<YourKey>Art1\</YourKey>

&#x20;   \<PMID>1906092\</PMID>

&#x20; \</Citation>

&#x20; \<Citation>

&#x20;   \<YourKey>Art2\</YourKey>

&#x20;   \<PMID>3024701\</PMID>

&#x20; \</Citation>

\</CitMatchResult>
```

> （注：文档部分内容可能由 AI 生成）