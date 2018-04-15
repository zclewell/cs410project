import metapy
import csv


def my_tokenizer(doc):
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    tok = metapy.analyzers.LowercaseFilter(tok)
    tok = metapy.analyzers.ListFilter(tok, "data/stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)
    tok = metapy.analyzers.Porter2Filter(tok)

    ana = metapy.analyzers.NGramWordAnalyzer(1, tok)
    unigrams = ana.analyze(doc)

    tok.set_content(doc.content())
    tokens = []
    for token, count in unigrams.items():
        tokens.append(token)
    return tokens
    
if __name__ == '__main__':
    doc = metapy.index.Document()
    bypassedFirst = False #first row of the csv has the column titles so we don't want to index this
    with open('prepped.txt', 'a') as of:
            with open('data.csv','rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    if bypassedFirst:
                        #combine all fields of the csv into one string
                        combined = str(unicode(row[0], errors='ignore')) + ' ' + str(unicode(row[1], errors='ignore')) + ' ' + str(unicode(row[2], errors='ignore'))

                        #strip some stopwords that the tokenizer will miss
                        combined = combined.replace('_',' ').replace('.',' ').replace('\\',' ').replace('|',' ')

                        #tokenize
                        doc.content(combined)
                        tokens = my_tokenizer(doc)

                        #output all tokens for a given row into a single line in our output file
                        for token in tokens:
                                of.write(token)
                                of.write(' ')
                        of.write('\n')
                    else:
                        bypassedFirst = True


