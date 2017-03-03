import scrapy
import time
import random
import logging

class Imdbspider(scrapy.Spider):
    name = 'imdb_spider'

    start_urls = [
        'http://www.imdb.com/search/title?release_date=1980-01-01,2018-01-01&title_type=feature&user_rating=5.0,10'
        ]
    imdbhome = 'http://www.imdb.com'
    
    # obtain the movie hrefs and next page's href
    def parse(self,response):
        logging.basicConfig()
        logger = logging.getLogger('imdb')
        logger.setLevel(logging.INFO)
        i = 1
        movie_hrefs = [self.imdbhome + ele for ele in response.selector.xpath('//h3[@class="lister-item-header"]/a/@href').extract()]
        next_page = response.selector.xpath('//a[@class="lister-page-next next-page"]/@href').extract()
        for movie in movie_hrefs:
            yield scrapy.Request(movie,callback=self.parse_movie)
            # sleep random 2 to 4 seconds
            time.sleep (random.randint(1,3))
        if next_page:
            logger.info('this is the %f pages' %i)
            i = i+1
            logger.info('%s' %next_page)
            yield scrapy.Request('http://www.imdb.com/search/title' + next_page[0],callback=self.parse)

    # obtain the needed data from a movie page and sent to ElasticSearch
    def parse_movie(self, response):
        title = response.selector.xpath('//h1[@itemprop="name"]/text()').extract_first()
        datePublished = response.selector.xpath('//meta[@itemprop="datePublished"]/@content').extract_first()
        summary = response.selector.xpath('//div[@class="summary_text"]/text()').extract_first()
        genres = response.xpath("//span[@itemprop='genre']/text()").extract()
        creators = response.xpath("//span[@itemprop='creator']//span[@itemprop='name']/text()").extract()
        casts = response.xpath("//td[@itemprop='actor']//span[@itemprop='name']/text()").extract()
        time = response.xpath("//time[@datetime]/text()").extract()[-1]
        plot_keywords = response.xpath("//div[@itemprop='keywords']//span[@itemprop='keywords']/text()").extract()
        rating = response.xpath("//div[@class='ratingValue']//span[@itemprop='ratingValue']/text()").extract_first()
        country = response.xpath("//div[h4[text() = 'Country:']]/a/text()").extract()
        language = response.xpath("//div[h4[text() = 'Language:']]/a/text()").extract()
        poster = response.xpath('//div[@class="poster"]//img/@src').extract_first()
        yield {'title': title,
               'datePublished': datePublished,
               'summary': self.normalize_string(summary),
               'genres': genres,
               'creators': creators,
               'casts': casts,
               'time': self.normalize_integer(time),
               'plot_keywords': plot_keywords,
               'rating': self.normalized_float(rating),
               'country': country,
               'languages': language,
               'poster': poster}




    def normalized_float(self,num):
        return float(num)

    def normalize_string(self,s):
        return s.strip()


    def normalize_integer(self,num):
        return int(filter(lambda x: x.isdigit(), num))
