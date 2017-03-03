# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from elasticsearch_dsl.document import DocType
from elasticsearch_dsl.field import Text, Date, Keyword, Integer, String, Completion, Float
from elasticsearch_dsl.analysis import token_filter, analyzer
from elasticsearch_dsl import Index
from elasticsearch import Elasticsearch


es=Elasticsearch(['localhost'],http_auth=('elastic', 'changeme'),port=9200)

ngram_filter = token_filter('ngram_filter',
                            type='nGram',
                            min_gram=1,
                            max_gram=20)

ngram_analyzer = analyzer('ngram_analyzer',
                          type='custom',
                          tokenizer='whitespace',
                          filter=[
                              'lowercase',
                              'asciifolding',
                              ngram_filter
                          ])


class ImdbspiderPipeline(object):
    def __init__(self):
        movies = Index('imdb', using=es)
        movies.doc_type(Movie)
        movies.delete(ignore=404)
        movies.create()
    
    # insert data into ElasticSearch
    def process_item(self, item, spider):
        movie = Movie()
        movie.title = item['title']
        movie.summary = item['summary']
        movie.datePublished = item['datePublished']
        movie.genres = item['genres']
        movie.creators = item['creators']
        movie.casts = item['casts']
        movie.time = item['time']
        movie.rating = item['rating']
        movie.countries = item['country']
        movie.languages = item['languages']
        movie.poster = item['poster']
        movie.plot_keywords = item['plot_keywords']
        movie.suggest = [item['title']] + item['casts'] + item['creators']
        movie.save(using=es)
        return item


# define data mapping and analyzer
class Movie(DocType):
    title = Text(fields={'raw':{'type': 'keyword'}})
    summary = Text()
    datePublished = Date()
    creators = Keyword(multi=True)
    genres = Keyword(multi=True)
    casts = Keyword(multi=True)
    time = Integer()
    countries = Keyword(multi=True)
    plot_keywords = Keyword(multi=True)
    languages = Keyword(multi=True)
    rating = Float()
    poster = Keyword()
    suggest = Completion(analyzer=ngram_analyzer,
                         search_analyzer=analyzer('standard'))
    class Meta:
        index = 'imdb'
