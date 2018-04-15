import metapy
import csv


def my_tokenizer(doc):
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    tok = metapy.analyzers.LowercaseFilter(tok)
    tok = metapy.analyzers.ListFilter(tok, "data/stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)
    tok = metapy.analyzers.Porter2Filter(tok)

    ana = metapy.analyzers.NGramWordAnalyzer(1, tok)
    trigrams = ana.analyze(doc)

    tok.set_content(doc.content())
    tokens, counts = [], []
    for token, count in trigrams.items():
        counts.append(count)
        tokens.append(token)
    return tokens
    
if __name__ == '__main__':
    doc = metapy.index.Document()
    bypassedFirst = False
    with open('prepped.txt', 'a') as of:
            with open('data.csv','rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    if bypassedFirst:
                        combined = str(unicode(row[0], errors='ignore')) + ' ' + str(unicode(row[1], errors='ignore')) + ' ' + str(unicode(row[2], errors='ignore'))
                        combined = combined.replace('_',' ').replace('.',' ').replace('\\',' ').replace('|',' ')
                        doc.content(combined)
                        tokens = my_tokenizer(doc)
                        for token in tokens:
                                of.write(token)
                                of.write(' ')
                        of.write('\n')
                    else:
                        bypassedFirst = True


