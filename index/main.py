import math
import sys
import time

import metapy
import pytoml
from tqdm import *
import csv

from math import log, pi, e

class PL2Ranker(metapy.index.RankingFunction):

    def __init__(self, some_param=1.0):
        self.param = some_param
        super(PL2Ranker, self).__init__()

    def score_one(self, sd):
        tfn = sd.doc_term_count * log(1 + self.param * (sd.avg_dl / sd.doc_size), 2)
        if tfn <= 0:
            return 0

        lmb = sd.num_docs / sd.corpus_term_count
        if lmb < 1:
            return 0

        return sd.query_term_weight * (tfn * log(tfn * lmb,2) 
               + log(e, 2)*(1/lmb - tfn) + 0.5 * log(2 * pi * tfn, 2))/(tfn + 1)

def load_ranker():
    return PL2Ranker()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)
    cfg = sys.argv[1]
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    ranker = load_ranker()
    # ev = metapy.index.IREval(cfg)
    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)
    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)
    start_time = time.time()
    top_k = 10
    query_path = query_cfg.get('query-path', 'queries.txt')
    query_start = query_cfg.get('query-id-start', 0)
    query = metapy.index.Document()
    print('Running queries')
    with open(query_path) as query_file:
        with open('../data.csv','rb') as f:
            reader = csv.reader(f)
            for query_num, line in enumerate(query_file):
                print(line)
                query.content(line.strip())
                results = ranker.score(idx, query, top_k)
                print(results)
                doc_ids = []
                interestingrows = []
                for curr in results:
                    if curr[0] != 1:
                        interestingrows += [row for idx, row in enumerate(reader) if idx == curr[0]]
                        # doc_ids.append(curr[0])
                for curr in interestingrows:
                    print('\t'+curr[0])
                print('\n')
