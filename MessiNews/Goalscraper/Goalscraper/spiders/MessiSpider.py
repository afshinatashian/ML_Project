import scrapy
from datetime import date, datetime


date_check = "01/01/2019"
date_time_check_obj = datetime.strptime(date_check, '%d/%m/%Y')
class messispider(scrapy.Spider):
    name = 'messi'
    start_urls = ['https://www.goal.com/en/player/lionel-messi/1/c5ryhn04g9goikd0blmh83aol']

    def parse(self, response):
        for link in response.css('.card a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_news)
        
        next_page = 'https://www.goal.com/' + response.css('a.btn.btn--older.needsclick').attrib['href']
        date = response.css('time::text')[-1].get()
        
        date_time_obj = datetime.strptime(date.strip(), '%d/%m/%Y')
        if next_page is not None:
            if date_time_obj >= date_time_check_obj:
                yield response.follow(next_page,callback=self.parse)
    
    def parse_news(self, response):
        yield {
            'Title': response.css('.article_title__Kfsaf::text').get(),
            'Summary': response.css('.article_teaser__1OofW::text').get(),
            'Content': response.css('p::text').getall(),
            'Author_Name': response.css('.article_authorPageLink__6nbzB::text').get(),
            'Time': response.css('.time::text').get()
        }
        
        
        