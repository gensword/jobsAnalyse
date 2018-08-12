from Spiders import jobs_spider
import os
import time
import sys; sys.path.append(os.path.dirname(__file__)+'/../Spiders')
from Spiders import categories_spider
import subprocess

categories = categories_spider.Category().get_categories()
start_time = time.time()
while categories:
    jobs = categories[:4]
    jobs_spider.Spider().get_profession_jobs(jobs)
    categories = categories[4:]
print('used ' + str(time.time() - start_time) + ' secs')
#subprocess.call('sh retry.sh', shell=True)
#exit()
