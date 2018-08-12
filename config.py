import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Lagou_job_analysis'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:xiyanghui99@localhost/jobsAnalyse'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'xiyanghui99'
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
