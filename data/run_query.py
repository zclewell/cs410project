import math
import sys

import metapy
import pytoml
from tqdm import *
import csv
from subprocess import call

from math import log, pi, e

class OurRanker(metapy.index.RankingFunction):

    def __init__(self, some_param=1.0):
        self.param = some_param
        super(OurRanker, self).__init__()

    def score_one(self, sd):
        tfn = sd.doc_term_count * log(1 + self.param * (sd.avg_dl / sd.doc_size), 2)
        if tfn <= 0:
            return 0

        lmb = sd.num_docs / sd.corpus_term_count
        if lmb < 1:
            return 0

        return sd.query_term_weight * (tfn * log(tfn * lmb,2) 
               + log(e, 2)*(1/lmb - tfn) + 0.5 * log(2 * pi * tfn, 2))/(tfn + 1)

def my_tokenizer(doc):
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    tok = metapy.analyzers.LowercaseFilter(tok)
    tok = metapy.analyzers.ListFilter(tok, "stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)
    tok = metapy.analyzers.Porter2Filter(tok)

    ana = metapy.analyzers.NGramWordAnalyzer(1, tok)
    unigrams = ana.analyze(doc)

    tok.set_content(doc.content())
    tokens = []
    for token, count in unigrams.items():
        tokens.append(token)
    return tokens

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: {} type result_num query".format(sys.argv[0]))
        sys.exit(1)
    type_req = sys.argv[1]
    cfg = ''
    url_refine_term = ''
    if type_req == 'profile':
        cfg = './profile_config.toml'
        url_refine_term = 'edu/directory/'
    elif type_req == 'news':
        cfg = './news_config.toml'
        url_refine_term = 'edu/news/'
    elif type_req == 'courses':
        cfg = './courses_config.toml'
        url_refine_term = 'edu/courses/'
    elif type_req == 'all':
        cfg = './entire_config.toml'
    else:
        print('Invalid search type')
        sys.exit(1)
    idx = metapy.index.make_inverted_index(cfg)
    ranker = OurRanker()


    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)
    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    top_k = 0
    try:
        top_k = int(sys.argv[2])
    except ValueError:
        print('Number of results must be an integer')

    user_query = sys.argv[3]
    query = metapy.index.Document()
    with open('data.csv','rb') as f:
        reader = csv.reader(f)
        urls = [row[0] for index, row in enumerate(reader) if url_refine_term in str(unicode(row[0], errors='ignore'))]
    print(user_query)
    query.content(user_query.strip())
    results = ranker.score(idx, query, top_k)
    for curr in results:
        print('\t'+urls[curr[0]]+' ('+str(curr[1])+')')
    print('\n')
    # call(['rm','-r','./idx'])

