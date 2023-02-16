# pip install spacy requests parsel

# to install ML model:
# py -m spacy download ru_core_news_lg

# to start:
# py text_scraper.py

from requests import get
from parsel import Selector
import quote_finder

rss_feed = get('https://www.kommersant.ru/RSS/main.xml')
rss_xml = Selector(text=rss_feed.text, type='xml')

for item in rss_xml.xpath('//item'):
    pub_date = item.xpath('pubDate/text()').get()
    link = item.xpath('link/text()').get()
    content_response = get(link)
    if content_response.status_code == 200:
        page_node = Selector(text=content_response.text, type='html')
        texts = page_node.css('p.doc__text').xpath('text()').getall()
        content = ' '.join(texts)
        result_list = quote_finder.get_quotes_and_author(content)
        with open('result.txt', 'a+', encoding='utf-8') as f:
            f.write(f'{pub_date}\n{link}\n')
            for l in result_list:
                f.write(l)
    else:
        print(f'Got error {content_response.status_code} on page {link}')
