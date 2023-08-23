import requests
import difflib
import sys

HOST = "https://www.selectree.calpoly.edu"
SEARCH_MULTI_PATH = "/api/tree/search-by-name-multiresult/"
MAX_TREES = 10000
 
def searchByNameMultiResultWebRequest(searchTerm, activePage, resultsPerPage, host, search_multi_path):
                URL = host + search_multi_path
                params = dict()
                params["searchTerm"] = searchTerm
                params["activePage"] = activePage
                params["resultsPerPage"] = resultsPerPage
                res =requests.get(URL, params=params).json()
                return res
 
def testNameUnformatted(searchTerm):
    match = False
    query = searchByNameMultiResultWebRequest(searchTerm, 1, MAX_TREES, HOST, SEARCH_MULTI_PATH)
    seq_ratio = 0
    top_result = ""
    for tree in query['pageResults']:
        tree_string = tree['name_unformatted'].rstrip().replace("<em>", "").replace("</em>", "")
        seq = difflib.SequenceMatcher(None, tree_string, searchTerm)
        seq_ratio_tmp = seq.ratio() * 100
        if (seq_ratio_tmp > seq_ratio):
            seq_ratio = seq_ratio_tmp
            top_result = tree_string
        if tree_string == searchTerm:
            match = True
            print(f'{searchTerm} found in selectree database!')
            break
    if not match:
        print(f'{searchTerm} not found in selectree database!, best result is {top_result} with {seq_ratio} sequence ratio')
 
def main():
    if len(sys.argv) < 2:
        print("Usage: python driver.py <test_name_1> <test_name_2> ...")
        return

    for arg in sys.argv[1:]:
        testNameUnformatted(arg)

if __name__ == "__main__":
    main()
