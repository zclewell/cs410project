import math
import sys
import time

import metapy
import pytoml

from math import log, pi, e

class PL2Ranker(metapy.index.RankingFunction):
    """
    Create a new ranking function in Python that can be used in MeTA.
    """
    def __init__(self, some_param=1.0):
        self.param = some_param
        # You *must* call the base class constructor here!
        super(PL2Ranker, self).__init__()

    def score_one(self, sd):
        """
        You need to override this function to return a score for a single term.
        For fields available in the score_data sd object,
        @see https://meta-toolkit.org/doxygen/structmeta_1_1index_1_1score__data.html
        """
        tfn = sd.doc_term_count * log(1 + self.param * (sd.avg_dl / sd.doc_size), 2)
        if tfn <= 0:
            return 0

        lmb = sd.num_docs / sd.corpus_term_count
        if lmb < 1:
            return 0

        return sd.query_term_weight * (tfn * log(tfn * lmb,2) 
               + log(e, 2)*(1/lmb - tfn) + 0.5 * log(2 * pi * tfn, 2))/(tfn + 1)

def load_ranker():
    """
    Use this function to return the Ranker object to evaluate.

    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index. You can ignore this, unless
    you need to load a ForwardIndex for some reason...
    """
    return PL2Ranker(10)

def get_results(cfg_file, query_file):
    idx = metapy.index.make_inverted_index(cfg_file)
    ranker = load_ranker(cfg)
    query = metapy.index.Document()
    top_k = 10

    results = []
    with open(query_path, 'r') as query_file:
        queries = query_file.readlines()

    for line in tqdm(queries):
        query.content(line.strip())
        result.append(ranker.score(idx, query, top_k))
    return results

def main():
    print(get_results('config.toml', '../data/queries.txt'))

if __name__ == '__main__':
    main()
