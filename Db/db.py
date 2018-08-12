import pymysql.cursors


def insert(job):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `jobs` (`id`, `job_name`, `job_category`, `publish_date`, `money`," \
                  "`experience`, `education`, `city`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (job[0], job[1], job[2], job[3], job[4], job[5], job[6], job[7]))
        connection.commit()
    finally:
        connection.close()

def select(search_keys, search_values):
    connection = get_connection()

    results = {}
    try:
        with connection.cursor() as cursor:
            # Read a single record
            new_search_key = []
            for key in search_keys:
                new_search_key.append('`' + key + '`' + '=%s')
            seach_str = ' and '.join(new_search_key)
            sql = "SELECT * FROM `jobs` WHERE " + seach_str
            cursor.execute(sql, tuple(search_values))
            results = cursor.fetchall()
    finally:
        return results


def get_connection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='xiyanghui99',
                                 db='job_anlyse',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


if __name__ == '__main__':
    print(len(select(['education', 'city'], ['本科', '上海'])))