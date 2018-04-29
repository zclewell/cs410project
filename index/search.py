import math
import sys
import time
import metapy
import pytoml
class PL2Ranker(metapy.index.RankingFunction):
    """
    Create a new ranking function in Python that can be used in MeTA.
    """
    def __init__(self, some_param=0.6):
        self.param = some_param
        # You *must* call the base class constructor here!
        super(PL2Ranker, self).__init__()
    def score_one(self, sd):
        my_lambda = sd.num_docs/sd.corpus_term_count
        my_tfn = sd.doc_term_count * math.log(1.0 + (self.param * sd.avg_dl / sd.doc_size), 2)
        if my_lambda < 1 or my_tfn <= 0:
            return 0.0
        numerator = my_tfn * math.log(my_tfn * my_lambda, 2) 
        numerator += math.log(math.e,2) * (1.0/my_lambda - my_tfn) 
        numerator += 0.5*math.log(2.0*math.pi*my_tfn,2)
        denominator = my_tfn + 1.0
        return sd.query_term_weight*numerator/denominator
        
def load_ranker(cfg_file):
    return PL2Ranker()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)
    cfg = sys.argv[1]
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    ranker = load_ranker(cfg)
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
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = ranker.score(idx, query, 1)
            print(results[0][0])
            # avg_p = ev.avg_p(results, query_start + query_num, top_k)
            # print("Query {} average precision: {}".format(query_num + 1, avg_p))
    # print("Mean average precision: {}".format(ev.map()))
    # print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))