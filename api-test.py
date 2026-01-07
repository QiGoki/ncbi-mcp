import requests
import pprint

BASE_URl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
APIS = {
    "einfo": "einfo.fcgi",
    "search": "esearch.fcgi",
}
API_KEY = "5e729756bb8301944a10d4a421bdee67d608"

EMAIL = "654051206@qq.com"
TOOL = "mcp"


def connect_to_ncbi(term, db="pubmed"):
    params = {
        # "tool": TOOL,
        # "email": EMAIL,
        "api_key": API_KEY,
        "retmode": "json",  # return data as json
        "db": db,
        "term": term
    }

    re = requests.get(BASE_URl + APIS["search"], params=params)
    return re.json()


if __name__ == "__main__":
    term = "USP39"
    ncbi = connect_to_ncbi(term)
    pprint.pprint(ncbi, indent=2)
