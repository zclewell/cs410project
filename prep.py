import metapy
import csv
import sys

def my_tokenizer(doc):
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    tok = metapy.analyzers.LowercaseFilter(tok)
    tok = metapy.analyzers.ListFilter(tok, "data/stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)
    # tok = metapy.analyzers.Porter2Filter(tok)

    ana = metapy.analyzers.NGramWordAnalyzer(1, tok)
    unigrams = ana.analyze(doc)

    tok.set_content(doc.content())
    tokens = []
    for token, count in unigrams.items():
        tokens.append(token)
    return tokens
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: {} csv output (refine_term)".format(sys.argv[0]))
        sys.exit(1)
    doc = metapy.index.Document()
    refine_term = ''
    if len(sys.argv) == 4:
        refine_term = sys.argv[3]
    #first row of the csv has the column titles so we don't want to index this
    bypassedFirst = False 
    with open(sys.argv[2], 'a') as of:
            with open(sys.argv[1],'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    if bypassedFirst:
                        if refine_term in str(unicode(row[0], errors='ignore')):
                            print(row[0])
                            combined = str(unicode(row[0], errors='ignore')) + ' ' + str(unicode(row[1], errors='ignore')) + ' ' + str(unicode(row[2], errors='ignore'))
                            #strip some stopwords that the tokenizer will miss
                            combined = combined.replace('_',' ').replace('.',' ').replace('\\n',' ').replace('|',' ').replace('\\',' ')
                            #tokenize
                            doc.content(combined)
                            tokens = my_tokenizer(doc)
                            #ignore empty lines
                            if len(tokens):
                                #output all tokens for a given row into a single line in our output file
                                for token in tokens:
                                        of.write(token)
                                        of.write(' ')
                                of.write('\n')
                    else:
                        bypassedFirst = True


