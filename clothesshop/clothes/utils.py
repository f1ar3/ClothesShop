from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery

from .models import Products

def q_search(query):

    vector = SearchVector('brand', 'name', 'description')
    query = SearchQuery(query)

    return Products.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')

