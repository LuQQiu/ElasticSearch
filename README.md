# ElasticSearch - a movie search website

## Project Outline
First, I crawled more than 200 pages movie data from IMDB webside using Python Scrapy and defined fields with mapping configuration.

After that, I established backend search engine that realized ngram partial matching, auto-suggest, structured query and aggregation in ElasticSearch.

Finally, A website was developed and designed with Flask and Node.js to display the movie information.

## How to Run
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
### Auto completion suggester
![autocomple](https://cloud.githubusercontent.com/assets/25273483/23535259/5015a626-ff8b-11e6-9ea0-367290cb8449.jpeg)
### Aggregation
![agg](https://cloud.githubusercontent.com/assets/25273483/23535260/50dd2ff2-ff8b-11e6-803c-91eba6832198.jpeg)
### Sort
![sort](https://cloud.githubusercontent.com/assets/25273483/23535261/5208e682-ff8b-11e6-97ce-3688f2966837.jpeg)
### Detailed webpage
![detailed](https://cloud.githubusercontent.com/assets/25273483/23535263/530d3bd2-ff8b-11e6-94df-718997470979.jpeg)
### More than 300 pages 
![300](https://cloud.githubusercontent.com/assets/25273483/23536331/274d3c2a-ff92-11e6-943a-48d17fb103ee.jpeg)

