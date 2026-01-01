def retrieve_docs_with_scores(vector_store, query, k):
    return vector_store.similarity_search_with_score(query, k=k)
