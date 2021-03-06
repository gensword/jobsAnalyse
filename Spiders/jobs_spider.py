import gevent
from gevent import monkey; monkey.patch_all()
from multiprocessing import Process
from urllib.parse import quote
import requests
import random
import json
import os
import time
import pymysql
import sys; sys.path.append(os.path.dirname(__file__)+'/../Db')
from Db import db
import redis


class Spider:
    def __init__(self):
        self.base_url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        self.base_referer = 'https://www.lagou.com/jobs/list_'
        self.page_list = [i for i in range(1, 31)]
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50', ]

    def get_detail_page(self, profession, page):
        user_agent = self.user_agents[random.randint(0, 3)]
        header = {
            'Host': 'www.lagou.com',
            'Referer': self.base_referer + quote(profession, 'utf-8'),
            'User-Agent': user_agent,
            'Origin': 'https://www.lagou.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': '_ga=GA1.2.2051013043.1524817163; user_trace_token=20180427161919-aef3dce5-49f3-11e8-a6c9-525400f775ce; LGUID=20180427161919-aef3e21b-49f3-11e8-a6c9-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAACBHABBICE02E3F0CFCAA56443CB319CFC51967A; _gid=GA1.2.343886854.1531189425; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530839025,1530944945,1530944971,1531189425; LGSID=20180710102342-43a4c977-83e8-11e8-8271-525400f775ce; TG-TRACK-CODE=index_navigation; SEARCH_ID=0fe9fd431b494733a0c3d3523bb54b05; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531192361; LGRID=20180710111237-18e0b41f-83ef-11e8-993d-5254005c3644',
        }
        data = {'pn': page, 'kd': profession}
        print(profession + ' page ' + str(page) + ' start')
        try:
            response = requests.post(self.base_url, headers=header, data=data, timeout=10)
        except Exception as e:
            with open(os.path.dirname(__file__)+'/../Logs/failed_fetch_page', 'a') as f:
                f.write(profession + ' page ' + str(page) + ' failed' + '\n')
            r = redis.Redis(host='localhost', port=6379)
            r.lpush('failed_jobs', profession + ' ' + str(page) + ' ' + '0')
            return
        self.clear_data(response.content, profession)
        print(profession + ' page ' + str(page) + ' finished')

    def get_all_pages(self, profession, page_list):
        jobs = [gevent.spawn(self.get_detail_page, profession, page) for page in page_list]
        gevent.joinall(jobs)

    def clear_data(self, page, profession):
        results = json.loads(page.decode('utf-8'))['content']['positionResult']['result']
        for result in results:
            job = []
            job.extend(
                [result['positionId'], result['positionName'], profession, result['createTime'], result['salary'],
                 result['workYear'], result['education'], result['city']])
            try:
                db.insert(job)
            except pymysql.err.IntegrityError as e:
                with open(os.path.dirname(__file__)+'/../Logs/duplicate_data', 'a') as f:
                    f.write(str(result['positionId']) + '\n')

    def get_profession_jobs(self, profession_list):
        process_list = []
        for profession in profession_list:
            p = Process(target=self.get_all_pages, args=(profession, self.page_list))
            p.start()
            process_list.append(p)
        for p in process_list:
            p.join()





if __name__ == '__main__':
    start_time = time.time()
    professions = ['Python', 'PHP', 'Java', 'Go', 'Ruby', 'c#', 'c', '数据挖掘']
    spider = Spider()
    spider.get_profession_jobs(professions)
    end_time = time.time()
    print('All finished')
    print('Used ' + str(end_time - start_time) + ' seconds')
