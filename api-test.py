from typing import Optional, Dict, Union, List
from urllib.parse import urlencode

import requests
import pprint

# 通用配置
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
# 通用参数（建议必传，合规性）
API_KEY = "5e729756bb8301944a10d4a421bdee67d608"
EMAIL = "654051206@qq.com"
TOOL = "mcp"

COMMON_PARAMS = {
    "tool": TOOL,  # 替换为你的应用名
    "email": EMAIL,  # 替换为你的邮箱
    "api_key": API_KEY,  # 单IP每秒>3次请求时添加
}

def einfo(
    db: Optional[str] = None,
    retmode: str = "xml"
) -> Dict:
    """
    获取Entrez数据库列表或单个数据库的统计信息
    :param db: 目标数据库（如pubmed/protein），None则返回所有数据库
    :param version: XML版本（2.0返回扩展字段）
    :param retmode: 返回格式（xml/json）
    :return: 解析后的字典结果
    """
    params = COMMON_PARAMS.copy()
    if db:
        params["db"] = db
    params["retmode"] = retmode.lower()

    url = f"{BASE_URL}einfo.fcgi?{urlencode(params)}"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json() if retmode == "json" else resp.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"EInfo请求失败: {str(e)}")


def esearch(
    db: str = "pubmed",
    term: str = "",
    retstart: int = 0,
    retmax: int = 20,
    rettype: str = "uilist",
    retmode: str = "xml",
    sort: Optional[str] = None,
    field: Optional[str] = None,
    datetype: Optional[str] = None,
    reldate: Optional[int] = None,
    mindate: Optional[str] = None,
    maxdate: Optional[str] = None
) -> Dict:
    """
        文本检索获取UID列表，支持History服务器存储
        :param db: 目标数据库（必填）
        :param term: 检索词（URL编码前的字符串，必填）
        :param retstart: 结果起始位置
        :param retmax: 返回结果数量（最大10000）
        :param rettype: 返回类型（uilist/count）
        :param retmode: 返回格式（xml/json）
        :param sort: 排序方式（如pub_date/relevance）
        :param field: 限定检索字段（如title/author）
        :param datetype: 日期类型（mdat/pdat/edat）
        :param reldate: 最近N天（配合datetype）
        :param mindate/maxdate: 日期范围（YYYY/MM/DD等）
        :return: 解析后的字典结果
        """
    # 校验必填参数
    if not term:
        raise ValueError("ESearch必填参数term不能为空")

    params = COMMON_PARAMS.copy()
    params.update({
        "db": db,
        "term": term,
        "retstart": retstart,
        "retmax": min(retmax, 10000),  # 限制最大值
        "rettype": rettype,
        "retmode": retmode.lower()
    })
    # 可选参数
    if sort:
        params["sort"] = sort
    if field:
        params["field"] = field
    if datetype:
        params["datetype"] = datetype
    if reldate:
        params["reldate"] = reldate
    if mindate:
        params["mindate"] = mindate
    if maxdate:
        params["maxdate"] = maxdate

    url = f"{BASE_URL}esearch.fcgi?{urlencode(params)}"

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json() if retmode == "json" else resp.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"ESearch请求失败: {str(e)}")


def esummary(
        ids: Union[str, List[str], List[int]],
        db: str = "pubmed",
        retstart: int = 1,
        retmax: int = 20,
        retmode: str = "xml",
        version: Optional[str] = "2.0"
) -> Dict:
    """
    获取UID对应的文档摘要（DocSum）
    :param db: 目标数据库
    :param ids: UID列表
    :param retstart: 结果起始位置
    :param retmax: 返回结果数量（最大10000）
    :param retmode: 返回格式（xml/json）
    :param version: XML版本（2.0返回详细DocSum）
    :return: 解析后的字典结果
    """
    # 校验输入（二选一）
    if not ids :
        raise ValueError("ESummary必须传入ids")

    params = COMMON_PARAMS.copy()
    params.update({
        "db": db,
        "retstart": retstart,
        "retmax": min(retmax, 10000),
        "retmode": retmode.lower()
    })
    if isinstance(ids, (list, tuple)):
        ids = ",".join(map(str, ids))
    params["id"] = ids
    if version:
        params["version"] = version

    url = f"{BASE_URL}esummary.fcgi?{urlencode(params)}"
    print(url)
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json() if retmode == "json" else resp.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"ESummary请求失败: {str(e)}")


def efetch(

        ids: Optional[Union[str, List[str], List[int]]],
        db: str = "pubmed",
        retmode: str = "xml",
        rettype: Optional[str] = "abstract",
        retstart: int = 0,
        retmax: int = 20,
        strand: Optional[int] = None,
        seq_start: Optional[int] = None,
        seq_stop: Optional[int] = None,
        complexity: Optional[int] = None
) -> Union[str, Dict]:
    """
    获取UID对应的完整格式化记录（核心工具）
    :param db: 目标数据库
    :param ids: UID列表
    :param retmode: 返回格式（xml/text/html/fasta等）
    :param rettype: 返回类型（如abstract/medline/fasta）
    :param retstart: 结果起始位置
    :param retmax: 返回结果数量（最大10000）
    :param strand: DNA链方向（1/2，序列专属）
    :param seq_start/seq_stop: 序列起止位置（序列专属）
    :param complexity: 数据复杂度（0-4，序列专属）
    :return: 原始文本（如FASTA）或解析后的字典
    """
    if not ids:
        raise ValueError("EFetch必须传入ids")

    params = COMMON_PARAMS.copy()
    params.update({
        "db": db,
        "retstart": retstart,
        "retmax": min(retmax, 10000),
        "retmode": retmode.lower()
    })
    if isinstance(ids, (list, tuple)):
        ids = ",".join(map(str, ids))
    params["id"] = ids
    if rettype:
        params["rettype"] = rettype
    # 序列专属参数
    if strand:
        params["strand"] = strand
    if seq_start:
        params["seq_start"] = seq_start
    if seq_stop:
        params["seq_stop"] = seq_stop
    if complexity is not None:
        params["complexity"] = complexity

    url = f"{BASE_URL}efetch.fcgi?{urlencode(params)}"
    print(url)
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        # 非结构化格式（如fasta/text）返回原始文本，结构化返回解析结果
        if retmode in ["json", "xml"]:
            return resp.json() if retmode == "json" else resp.text
        return resp.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"EFetch请求失败: {str(e)}")


if __name__ == "__main__":
    term = " USP39 AND (heart OR cardiac)"
    # db = einfo(retmode="json")["einforesult"]["dblist"]
    # print("DB:",db)

    idList = esearch(term=term,retmax=5,retmode="json")["esearchresult"]["idlist"]
    print("IDS:",idList)

    # summary = esummary(ids=idList,retmode="json")
    # pprint.pprint(summary)
    #
    # fetch = efetch(ids=idList)
    # pprint.pprint(fetch)
