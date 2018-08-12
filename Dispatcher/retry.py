import redis
from urllib.parse import quote
import requests
import json
from Db import db
import pymysql

r = redis.Redis(host='localhost', port=6379)
while r.llen('failed_jobs'):
    failed_job = r.rpop('failed_jobs').decode('utf8')
    profession, page, retry_nums = tuple(failed_job.split(' '))
    if int(retry_nums) >= 3:
        continue
    else:
        try:
            header = {
                'Host': 'www.lagou.com',
                'Referer': 'https://www.lagou.com/jobs/list_' + quote(profession, 'utf-8'),
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
                'Origin': 'https://www.lagou.com',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': '_ga=GA1.2.2051013043.1524817163; user_trace_token=20180427161919-aef3dce5-49f3-11e8-a6c9-525400f775ce; LGUID=20180427161919-aef3e21b-49f3-11e8-a6c9-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAACBHABBICE02E3F0CFCAA56443CB319CFC51967A; _gid=GA1.2.343886854.1531189425; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530839025,1530944945,1530944971,1531189425; LGSID=20180710102342-43a4c977-83e8-11e8-8271-525400f775ce; TG-TRACK-CODE=index_navigation; SEARCH_ID=0fe9fd431b494733a0c3d3523bb54b05; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531192361; LGRID=20180710111237-18e0b41f-83ef-11e8-993d-5254005c3644',
            }
            data = {'pn': page, 'kd': profession}
            response = requests.post('https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false', headers=header, data=data, timeout=10)
            results = json.loads(response.content.decode('utf-8'))['content']['positionResult']['result']
            for result in results:
                job = []
                job.extend(
                    [result['positionId'], result['positionName'], profession, result['createTime'], result['salary'],
                     result['workYear'], result['education'], result['city']])
                try:
                    db.insert(job)
                except pymysql.err.IntegrityError as e:
                    break

        except Exception as e:
            r.lpush(profession+' ' + page + ' ' + str(int(retry_nums)+1))

