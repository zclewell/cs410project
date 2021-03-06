import math
import sys
import time

import metapy
import pytoml
from tqdm import *
import csv

from math import log, pi, e

#our ranking function
class OurRanker(metapy.index.Ranker):
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

#function to run when ran from command line
if __name__ == '__main__':
    #accepts a config file to run multiple queries on
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)
    cfg = sys.argv[1]
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)

    ranker = OurRanker()

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)
    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    top_k = 10
    query_path = query_cfg.get('query-path', './data/queries.txt')
    query_start = query_cfg.get('query-id-start', 0)
    query = metapy.index.Document()
    print('Running queries')
    with open(query_path) as query_file:
        with open('../data/data.csv','rb') as f:
            reader = csv.reader(f)

            #generate list of URLs so we can return them to user
            urls = [row[0] for idxs, row in enumerate(reader)]

            for query_num, line in enumerate(query_file):
                print(line)
                query.content(line.strip())
                results = ranker.score(idx, query, top_k)
                for curr in results:
                    print('\t'+urls[curr[0]]+' ('+str(curr[0])+')')
                print('\n')
