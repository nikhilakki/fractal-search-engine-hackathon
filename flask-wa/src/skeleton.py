# This is a skeleton template!

# Our main function!
def main():
    # 1. Recieve Query Json
    query, asinId = getQuery() # To do

    # 2. Prep Query
    tokenized_query = preprocess(query) # query is now processed and tokenized # Ankan

    # 3. Check if asinID is present in QA dataframe
    val = checkForAsinID(asinId)

    # 4. Based on val, do something!
    if val == 0:
        presentInBoth(asinId)
    elif val == 1:
        notPresentInQA(asinId)
    elif val == 2:
        notPresentInRV(asinId)
    else:
        notPresentInBoth()

def checkForAsinID(asinId):
    # check if asinId is present in QA, 0 if True else 1
    x = 0 if len(qa[qa['asin'] == asinId]) != 0 else 1
    # check if asinId is present in RV, 0 if True else 2
    y = 0 if len(rv[rv['asin'] == asinId]) != 0 else 2

    # return the sum
    Sum = x + y
    # such that:
    # 0 = Present in both
    # 1 = NOT present in QA but Present in RV
    # 2 = Present in QA but NOT present in RV
    # 3 = NOT present in both
    return Sum


def presentInBoth(tokenized_query,asinId):
    qdf = qa[qa['asin'] == asinId]
    rdf = rv[rv['asin'] == asinId]

    # Relevant Answer:
    tokenizedQA = qa['tokenized_questions']
    bmq = BM25(tokenizedQA)
    tfq = bmq.get_term_frequencies(tokenized_query)
    idfq = bmq.get_idf_for_query(tokenized_query)
    qdf['bm25scores'] = bmq.get_bm25_scores(tokenized_query,tfq,idfq)
    qdf = qdf.sort_values(by='bm25scores',axis=1)
    answer_json = qdf[['answer','answer_sentiment']].iloc[0:1].to_json(orient='records')

    # Relevant Reviews:
    tokenizedRV = rv['tokenized_rv']
    bmr = BM25(tokenizedRV)
    tfr = bmr.get_term_frequencies(tokenized_query)
    idfr = bmr.get_idf_for_query(tokenized_query)
    rdf['bm25scores'] = bmr.get_bm25_scores(tokenized_query,tfr,idfr)
    rdf = rdf.sort_values(by='bm25scores',axis=1)
    review_json = rdf[['reviewText','review_sentiment']].iloc[0:5].to_json(orient='records')

    return answer_json + review_json


def notPresentInQA(tokenized_query,asinId):
    rdf = rv[rv['asin'] == asinId]

    # Relevant Answer: None! Since the product does not have any answers
    answer_json = [{'answer':None,'answer_sentiment':None}]

    # Relevant Reviews:
    tokenizedRV = rv['tokenized_rv']
    bmr = BM25(tokenizedRV)
    tfr = bmr.get_term_frequencies(tokenized_query)
    idfr = bmr.get_idf_for_query(tokenized_query)
    rdf['bm25scores'] = bmr.get_bm25_scores(tokenized_query,tfr,idfr)
    rdf = rdf.sort_values(by='bm25scores',axis=1)
    review_json = rdf[['reviewText','review_sentiment']].iloc[0:5].to_json(orient='records')

    return answer_json + review_json


def notPresentInRV(tokenized_query,asinId):
    qdf = qa[qa['asin'] == asinId]

    # Relevant Answer:
    tokenizedQA = qa['tokenized_questions']
    bmq = BM25(tokenizedQA)
    tfq = bmq.get_term_frequencies(tokenized_query)
    idfq = bmq.get_idf_for_query(tokenized_query)
    qdf['bm25scores'] = bmq.get_bm25_scores(tokenized_query,tfq,idfq)
    qdf = qdf.sort_values(by='bm25scores',axis=1)
    answer_json = qdf[['answer','answer_sentiment']].iloc[0:1].to_json(orient='records')

    # Relevant Reviews: None! Since the product has no reviews
    review_json = [{'reviewText':None,'review_sentiment':None}]

    return answer_json + review_json


def notPresentInBoth():
    # Product ID neither has answers nor reviews
    answer_json = [{'answer':None,'answer_sentiment':None}]
    review_json = [{'reviewText':None,'review_sentiment':None}]
    return answer_json + review_json
