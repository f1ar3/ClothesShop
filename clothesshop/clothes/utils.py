from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery

from .models import Products, ProductSizes


def q_search(query):

    vector = SearchVector('brand', 'name', 'description')
    query = SearchQuery(query)

    return Products.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')

def get_product_sizes(product):
    return ProductSizes.objects.filter(product=product)

