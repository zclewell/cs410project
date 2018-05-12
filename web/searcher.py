import json
import time
import csv
import metapy
import operator
from query import OurRanker

class Searcher:
    def __init__(self, cfg):
        """
        Create/load a MeTA inverted index based on the provided config file and
        set default filter option to All
        """
        self.idx = metapy.index.make_inverted_index(cfg)
        self.url_refine_term = ''
        self.default_filter = 'All'
      
    # Main search called by search_server.py which given query returns results 

    def search(self, request):
        """
        Accept a JSON request and run the provided query with our ranker.
        """
        type_req = request['filter']
        print(type_req)
        cfg = ''
        url_refine_term = ''
        if type_req == 'Profiles':
            cfg = '../data/profile_config.toml'
            url_refine_term = 'edu/directory/'
            self.idx = metapy.index.make_inverted_index(cfg)
            self.url_refine_term = url_refine_term
        elif type_req == 'News':
            cfg = '../data/news_config.toml'
            url_refine_term = 'edu/news'
            self.idx = metapy.index.make_inverted_index(cfg)
            self.url_refine_term = url_refine_term
        elif type_req == 'Courses':
            cfg = '../data/entire_config.toml'
            #url_refine_term = 'edu/courses'
            self.idx = metapy.index.make_inverted_index(cfg)
            self.url_refine_term = url_refine_term
        elif type_req == 'All':
            cfg = '../data/entire_config.toml'
            self.idx = metapy.index.make_inverted_index(cfg)
            self.url_refine_term = url_refine_term
        else:
            print('Invalid search type')
            sys.exit(1)

        user_query = request['query']
        ranker = OurRanker()


        results = {}
        query = metapy.index.Document()
        query.content(user_query.strip())    
        response = {'query': request['query'], 'results': []} 
        
        results = ranker.score(self.idx, query)

        #generate array of docs based on config
        with open('../data/data.csv','rb') as f:
            reader = csv.reader(f)
            urls = [row[0] for index, row in enumerate(reader) if url_refine_term in str(unicode(row[0], errors='ignore'))]

        #generate urls corresponding to doc ids returned by ranker
        for res in results:
            if not (type_req == 'Courses' and not ("courses" in urls[res[0]])): 
                response['results'].append({
                    'score': float(res[1]),
                    'name': str(urls[res[0]]),
                    'path': self.idx.doc_path(res[0])
                })
            #print(urls[res[0]])
        return json.dumps(response, indent=2)

