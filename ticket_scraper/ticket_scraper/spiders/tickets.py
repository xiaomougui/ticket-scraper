import scrapy
import json
import requests
from scrapy import Spider
from ticket_scraper.settings import REDIS_SETTINGS
from scrapy.utils.project import get_project_settings
# from ticket_scraper.items import TicketScraperItem

# 判断参数是否传入
def rtes(data):
    scrapyd_url = 'http://localhost:5000/'
    url = f'{scrapyd_url}/test'
    data1 = {
        'name': 'test',
        'data':data
    }
    print(data1)
    requests.post(url, data=json.dumps(data1))

# 配置 Scrapy 爬虫信息
class TicketsSpider(scrapy.Spider):
    name = "tickets"

    def __init__(self, keyword="",cty="",ctl="",currPage=1,singleChar="", tn="",tsg="",sctl="",order=1,*args,**kwargs):
        print(keyword,cty,ctl,currPage,789)
        data = {
            'keyword': keyword,
            'cty': cty,
            'ctl': ctl,
            'currPage': currPage,
            'singleChar': singleChar,
            'tn': tn,
            'tsg': tsg,
            'sctl': sctl,
            'order': order,
        }
        rtes(data)
        super(TicketsSpider, self).__init__(*args, **kwargs)

        self.datach =data

    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     spider = super(TicketsSpider, cls).from_crawler(crawler, *args, **kwargs)
    #     spider.category = kwargs.get('datach')
    #     rtes(spider.category)

    def start_requests(self):
        url = 'https://search.damai.cn/searchajax.html'

        # params = {
        #     'keyword': "",
        #     'cty': "上海",
        #     'ctl': "音乐会",
        #     'currPage': "2",
        #     'singleChar': "",
        #     'tn': "",
        #     'sctl': "",
        #     'tsg': "0",
        #     'order': "1",
        # }
        headers = {
            'referer':'https://search.damai.cn/search.htm?spm=a2oeg.home.category.ditem_0.591b23e1bWz0BM&ctl=%E6%BC%94%E5%94%B1%E4%BC%9A&order=1&cty=%E5%8C%97%E4%BA%AC',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        }
        yield scrapy.FormRequest(
            url,
            headers=headers,
            formdata=self.datach,
            method='get',
            callback=self.parse
        )

    def parse(self, response):
        all_data = json.loads(response.text)
        ticket_data=all_data['pageData']['resultData']
        # print(ticket_data)
        if ticket_data:
            for data in ticket_data:
                yield {
                    'name': data['name'],
                    'date' :data['showtime'],
                    'actors':data['actors'],
                    'location':data['cityname'],
                    'location_details': data['venue'],
                    'price':data['price_str'],
                    'lowPrice': data['price'],
                    'highPrice': data['pricehigh'],
                    'categoryName': data['categoryname']
                }
