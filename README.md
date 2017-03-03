# ElasticSearch - a movie search website

## Project Outline
First, I crawled more than 200 pages movie data from IMDB webside using Python Scrapy and defined fields with mapping configuration.

After that, I established backend search engine that realized ngram partial matching, auto-suggest, structured query and aggregation in ElasticSearch.

Finally, A website was developed and designed with Flask and Node.js to display the movie information.

## How to run
starting to crawl data from IMDB website
```
scrapy crawl imdb_spider
```

Setting up Flask application
```
export FLASK_APP=webmovie.py
```
```
flask run
```
Now, you can open your movie website in the browser
```
localhost:5000
```

## Final Webpage


