from flask import Flask, jsonify
import json
import time
import requests
import pymysql
from flask import request
from scrapy.utils.project import get_project_settings


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/1'




# @app.route('/', methods=['POST'])
# def init():
#     return 1

def start_scrapy_spider(params):
    # 调用 Scrapyd API 启动 Scrapy Spider，并传递参数
    # 这里的示例代码仅供参考，具体实现可以根据 Scrapyd API 的实际情况进行调整

    scrapyd_url = 'http://localhost:6800/'
    data= {
        'project': 'ticket_scraper',
        'spider': 'tickets',
        'keyword':params['keyword'],
        'cty':params['cty'],
        'ctl':params['ctl'],
        'currPage':params['currPage'],
        'singleChar':params['singleChar'],
        'tn':params['tn'],
        'tsg':params['tsg'],
        'sctl':params['sctl'],
        'order':params['order'],
    }

    # 构建启动 Spider 的 API 请求
    url = f'{scrapyd_url}/schedule.json'

    response = requests.post(url, data=data)
    return response.json()


def fetch_data_from_db(data):
    # 构造 SQL 查询条件(动态)
    conditions = []
    params = []

    print(data)

    if data.get('keyword', '') != '':
        conditions.append("actors = %s")
        params.append(data['keyword'])
    if data.get('cty', '') != '':
        conditions.append("location = %s")
        params.append(data['cty'])
    if data.get('ctl', '') != '':
        conditions.append("categoryName = %s")
        params.append(data['ctl'])

    time.sleep(1)

    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='hrn77799.',
        database='ticket-data',
        cursorclass=pymysql.cursors.DictCursor
    )
    with conn.cursor() as cursor:
        # 构造动态 SQL 查询语句
        sql = "SELECT * FROM tickets"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY id DESC LIMIT 60"
        print(sql)

        cursor.execute(sql, tuple(params))
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(row)

    conn.close()
    return result


@app.route('/app', methods=['POST'])
def scrape_data():
    # 获取爬虫参数
    data = request.json
    # 启动 Scrapy 异步任务
    start_scrapy_spider(data)

    # 异步获取数据库数据
    result = fetch_data_from_db(data)


    print(result)

    return jsonify(result)

@app.route('/test', methods=['POST'])
def test():
    print(request)
    data1 = request.data
    print(data1.decode('utf-8'),123)
    return jsonify({'result': 'success'})

@app.route('/tags', methods=['POST'])
def tags():
    params = request.json
    headers = {
        'referer': 'https://search.damai.cn/search.htm?spm=a2oeg.home.category.ditem_0.591b23e1bWz0BM&ctl=%E6%BC%94%E5%94%B1%E4%BC%9A&order=1&cty=%E5%8C%97%E4%BA%AC',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }
    response=requests.get(url='https://search.damai.cn/searchajax.html', params=params, headers=headers)
    data= response.json()

    tags=data['pageData']['factMap']
    print(tags)

    return jsonify(tags)

# 设置响应头信息，允许特定域名跨域请求
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return "Sorry, the requested URL was not found on this server.", 404


if __name__ == '__main__':
    app.run(debug=False)
