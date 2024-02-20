import pymysql

from utils.log_util import logger
from utils.read import read_ini

data = read_ini()['mysql']

DB_CONF = {
    "host": data["HOST"],
    "port": int(data["PORT"]),
    "user": data["USER"],
    "password": data["PASSWD"],
    "db": data["DB"]
}


class MysqlDb:
    def __init__(self):
        # mysql链接
        self.conn = pymysql.connect(**DB_CONF, autocommit=True)
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 查询一条数据
    def select_db_one(self, sql):
        logger.info(f"执行sql：{sql}")
        self.cur.execute(query=sql)
        # 获取数据
        result = self.cur.fetchone()
        logger.info(f"sql执行结果{result}")
        return result

    # 查询所有数据
    def select_db_all(self, sql):
        logger.info(f"执行sql：{sql}")
        self.cur.execute(query=sql)
        # 获取数据
        result = self.cur.fetchall()
        logger.info(f"sql执行结果{result}")
        return result

    # 执行sql,不用获取数据库返回，但需要提交，比如update、delete
    def execute_sql(self, sql):
        try:
            logger.info(f"执行sql：{sql}")
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            logger.info(f"执行sql出错：{sql}")

    # 释放资源
    def __del__(self):
        self.cur.close()
        self.conn.close()


db = MysqlDb()

if __name__ == '__main__':
    db = MysqlDb()
    sql = "select code from users_verifycode where mobile = '13800001111' order by id limit 1;"
    print(db.select_db_one(sql)['code'])