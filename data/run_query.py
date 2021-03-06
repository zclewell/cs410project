#Script that evaluates a given query on a .dat file generated by our prep function based on the supplied config

import math
import sys

import metapy
import csv

from math import log, pi, e

#implementation of a PL2 Ranker
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

#returns a list of results specified by args
def run(args):
    #if we didn't get enough arguments exit
    if len(args) != 4:
        print("Usage: {} type result_num query".format(sys.argv[0]))
        sys.exit(1)

    #load the correct config file based on the type requested
    type_req = args[1]
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

    #create index based on config
    idx = metapy.index.make_inverted_index(cfg)

    #create ranker
    ranker = OurRanker()

    #generate top_k based on user argument
    top_k = 0
    try:
        top_k = int(args[2])
    except ValueError:
        print('Number of results must be an integer')

    user_query = args[3]
    query = metapy.index.Document()
    query.content(user_query.strip())

    results = ranker.score(idx, query, top_k)

    print(user_query)

    #generate array of docs based on config
    with open('data.csv','rb') as f:
        reader = csv.reader(f)
        urls = [row[0] for index, row in enumerate(reader) if url_refine_term in str(unicode(row[0], errors='ignore'))]
    
    #generate urls corresponding to doc ids returned by ranker
    output = []
    for curr in results:
        print('\t'+urls[curr[0]]+' ('+str(curr[1])+')')
        output.append(urls[curr[0]])
    return output

#function for when we are run from the command line
if __name__ == '__main__':
    #pipe the command line arguments into our run function
    run(sys.argv)
