import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Lagou_job_analysis'
    SQLALCHEMY_DATABASE_URI = 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MYSQL_USER = 
    MYSQL_PASSWORD = 
    REDIS_HOST = 
    REDIS_PORT = 
