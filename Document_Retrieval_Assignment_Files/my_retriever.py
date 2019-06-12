import math

class Retrieve:
    # Create new Retrieve object storing index and termWeighting scheme
    def __init__(self,index, termWeighting):
        self.index = index
        self.termWeighting = termWeighting

        #Retrieve list of document ids
        self.docIds = set([docId for term in self.index.keys() for docId in self.index[term].keys()])
        self.doc_d2 = {}

        #compute sum(d^2) for term weighting schemes
        if self.termWeighting == "binary":
            for term in self.index.keys():
                for docId in self.index[term].keys():
                    if docId in self.doc_d2:
                        self.doc_d2[docId] += 1
                    else:
                        self.doc_d2[docId] = 1

        elif self.termWeighting == "tf":
            for term in self.index.keys():
                for doc_id, count in self.index[term].items():
                    if doc_id in self.doc_d2:
                        self.doc_d2[doc_id] += count**2
                    else:
                        self.doc_d2[doc_id] = count**2

        elif self.termWeighting == "tfidf":
            #Compute IDF values for every term
            self.idf_w = {term:math.log(len(self.docIds)/len(self.index[term])) for term in self.index.keys()}
            for term in self.index.keys():
                for doc_id, count in self.index[term].items():
                    if doc_id in self.doc_d2:
                        self.doc_d2[doc_id] +=  (count*self.idf_w[term])**2
                    else:
                        self.doc_d2[doc_id] = (count*self.idf_w[term])**2


    # Method performing retrieval for specified query
    def forQuery(self, query):

        #Document IDs
        result_docIds = {}

        #Retrieve document ids for query type that is binary
        if self.termWeighting == "binary":
            
            q2 = len(query)
        
            for term in query.keys(): 
                if term not in self.index: continue
                for docId in self.index[term].keys():    
                    if docId in result_docIds:
                        result_docIds[docId] += 1
                    else:
                        result_docIds[docId] = 1
            result_docIds = {key:(value/(math.sqrt(q2)*math.sqrt(self.doc_d2[key]))) for key, value in result_docIds.items()}
            result_docIds = sorted(result_docIds, key=lambda x: result_docIds[x], reverse=True)
            return result_docIds[:11]


        #Term frequency
        elif self.termWeighting == "tf":

            q2 = sum([value**2 for term, value in query.items()])

            for term, tf_count in query.items():
                if term not in self.index: continue
                for doc, count in self.index[term].items():
                    q_d = tf_count * self.index[term][doc]
                    if doc in result_docIds:
                        result_docIds[doc] += (q_d)
                    else:
                        result_docIds[doc] = (q_d)

            result_docIds = {key:(value/math.sqrt(self.doc_d2[key])) for key, value in result_docIds.items()}
            result_docIds = sorted(result_docIds, key=lambda x: result_docIds[x], reverse=True)
            return result_docIds[:11]

        #Term frequency - inverse document frequency
        elif self.termWeighting == "tfidf":
    
            q2 = sum([(count * self.idf_w[term])**2 for term, count in query.items() if term in self.index])

            for term, tf_count in query.items():
                if term not in self.index: continue
                for docId, count in self.index[term].items():
                    q_d = (tf_count*self.idf_w[term]) * (count*self.idf_w[term])
                    if docId in result_docIds:
                        result_docIds[docId] += (q_d)
                    else:
                        result_docIds[docId] = (q_d)
            result_docIds = {key:(value/(math.sqrt(q2) * math.sqrt(self.doc_d2[key]))) for key, value in result_docIds.items()}
            result_docIds = sorted(result_docIds, key=lambda x: result_docIds[x], reverse=True)
            
            return result_docIds[:11]