import seaborn as sns
import re
import pandas as pd
from Db import db
import matplotlib.pyplot as plt
import matplotlib as mpl
from io import BytesIO
import base64


class Analysis:
    def __init__(self):
        self.conn = db.get_connection()

    def jobs_salary(self, jobs_list):
        jobs_str = ','.join(jobs_list)
        sql = 'SELECT * FROM jobs where job_category in' + '(' + jobs_str + ')'
        data = pd.read_sql(sql, con=self.conn)
        data['money'] = data['money'].map(self.get_average_money)
        # print(data['money'].head())
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['font.serif'] = ['SimHei']
        sns.set_style("ticks", {"font.sans-serif": ['SimHei', 'Droid Sans Fallback']})

        f, ax = plt.subplots(figsize=(7, 6))
        sns.boxplot(x="money", y="job_category", data=data,
                    whis="range", palette="vlag")
        sns.swarmplot(x="money", y="job_category", data=data,
                      size=2, color=".3", linewidth=0)

        ax.xaxis.grid(True)
        ax.set(ylabel="")
        sns.despine(trim=True, left=True)
        img = BytesIO()
        plt.savefig(img)
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue())
        return plot_url

    def jobs_experience(self, jobs_list):
        jobs_str = ','.join(jobs_list)
        sql = 'SELECT * FROM jobs where job_category in' + '(' + jobs_str + ')'
        data = pd.read_sql(sql, con=self.conn)
        data['money'] = data['money'].map(self.get_average_money)
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['font.serif'] = ['SimHei']
        sns.set_style("whitegrid", {"font.sans-serif": ['SimHei', 'Droid Sans Fallback']})
        sns.barplot(x="experience", y="money", hue="job_category", data=data)

    def jobs_city_percentage(self, jobs_list, cities_list):
        jobs_str = ','.join(jobs_list)
        cities_str = ','.join(cities_list)
        sql = 'SELECT city, job_category, count(*) as nums FROM jobs where job_category in' + '(' + jobs_str + \
              ') and city in ' + '(' + cities_str + \
              ')group by job_category, city'
        data = pd.read_sql(sql, con=self.conn)
        sql = 'SELECT job_category, count(*) as job_nums FROM jobs where job_category in' + '(' + jobs_str + ')group by job_category'
        job_nums = pd.read_sql(sql, con=self.conn)
        job_city_percentage = []
        for row, nums in enumerate(data['nums']):
            job_city_percentage.append(nums / job_nums['job_nums'][row // len(cities_list)])
        data.insert(0, 'percentage', job_city_percentage)
        for row in range(len(jobs_list)):
            percentage = 1 - sum(data['percentage'][row * len(cities_list):(row + 1) * len(cities_list)])
            nums = job_nums['job_nums'][row] - sum(data['nums'][row * len(cities_list):(row + 1) * len(cities_list)])
            new_row = {'percentage': percentage, 'city': '其他城市',
                       'job_category': data['job_category'][row * len(cities_list)], 'nums': nums}
            data = data.append(new_row, ignore_index=True)
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['font.serif'] = ['SimHei']
        sns.set_style("whitegrid", {"font.sans-serif": ['SimHei', 'Droid Sans Fallback']})
        sns.barplot(x="city", y="percentage", hue="job_category", data=data)

    def jobs_salary_education(self, jobs_list):
        jobs_str = ','.join(jobs_list)
        sql = 'SELECT education, job_category, money FROM jobs where job_category in' + '(' + jobs_str + ')'
        data = pd.read_sql(sql, con=self.conn)
        data['money'] = data['money'].map(self.get_average_money)
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['font.serif'] = ['SimHei']
        sns.set_style("whitegrid", {"font.sans-serif": ['SimHei', 'Droid Sans Fallback']})
        sns.barplot(x="education", y="money", hue="job_category", data=data)

    def jobs_salary_experience_line(self, jobs_list):
        jobs_str = ','.join(jobs_list)
        sql = 'SELECT experience, job_category, money FROM jobs where job_category in' \
              + '(' + jobs_str + ") and experience not in('不限')"
        data = pd.read_sql(sql, con=self.conn)
        data['money'] = data['money'].map(self.get_average_money)
        data['experience'] = data['experience'].map(self.handle_experience)
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['font.serif'] = ['SimHei']
        sns.set_style("whitegrid", {"font.sans-serif": ['SimHei', 'Droid Sans Fallback']})
        sns.lineplot(x="experience", y="money", hue="job_category", data=data)

    @staticmethod
    def handle_experience(experience):
        experience = re.findall(r'(\d+)', experience)
        if not experience:
            return 0
        elif len(experience) == 1:
            return int(experience[0])
        else:
            experience = (int(experience[1]) + int(experience[0])) / 2
            return experience

    @staticmethod
    def get_average_money(money):
        money = re.findall(r'(\d+)', money)
        if len(money) == 1:
            return float(money[0])
        money = (float(money[1]) + float(money[0])) / 2
        return money


if __name__ == '__main__':
    Analysis = Analysis()
    plot_url = Analysis.jobs_salary(["'PHP'", "'Java'", "'Python'"])
    print(plot_url)