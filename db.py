import pymysql
import logging
logging.basicConfig(level=logging.DEBUG)
conn = pymysql.connect(host='localhost',port=3306,db='邮件分类', user='root', password='123456',charset='utf8')
def insert(sql, values):
    with conn.cursor() as cs:
        cs.execute(sql, values)
        conn.commit()
        logging.info(f'插入操作 {sql}，参数值 {values}')
def update(sql):
    insert(sql)
    logging.info(f'更新操作 {sql}')
def delete(sql):
    insert(sql)
    logging.info(f'删除操作 {sql}')
def select(sql):
    result = []
    with conn.cursor() as cs:
        cs.execute(sql)
        result = cs.fetchall()
        logging.debug(f'查询操作 {sql} 结果如下\n{result}')
        return result

