import pymysql

db = pymysql.connect(host='localhost',
                   port=3306,
                   user='root',
                   passwd='123456',
                   database='邮件分类',
                   charset='utf8')

cur = db.cursor()

sql1 = '''create table user(
            email varchar(50),
            password varchar (50)
            )
            '''

sql2='''create table email(
                id int primary key auto_increment,
                title varchar (20),
                export_email_id int ,
                export_email varchar (80),
                import_email_id int ,
                import_email varchar (80),
                email_address varchar (80)
        )
        '''

cur.execute(sql1)
cur.execute(sql2)

db.commit()
cur.close()
db.close()


class style:
    def insert_user(self,email,password):
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='123456',
                             database='邮件分类',
                             charset='utf8')
        cur = db.cursor()
        sql = "insert into user (email,password ) values ('%s','%s');" % (email, password)
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()

    def insert_email(self,title,export_email_id,export_email,import_email_id,import_email,email_address):
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='123456',
                             database='邮件分类',
                             charset='utf8')
        cur = db.cursor()
        sql = "insert into email (title,export_email_id,export_email,import_email_id,import_email,email_address) \
                                           values (%s,%s,%s,%s,%s,%s);"
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()

    def select_user(self):
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='123456',
                             database='邮件分类',
                             charset='utf8')
        cur=db.cursor()
        sql = "select * from user ;"
        cur.execute(sql)
        db.commit()
        all_row = cur.fetchall()
        cur.close()
        db.close()
        return all_row

    def select_user_list(self):
        temp_list = []
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='123456',
                             database='邮件分类',
                             charset='utf8')
        cur = db.cursor()
        sql = "select * from user ;"
        cur.execute(sql)
        db.commit()
        all_row = cur.fetchall()
        for i in all_row:
            temp_list.append(list(i))
        cur.close()
        db.close()
        return temp_list

    def select_email(self):
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='123456',
                             database='邮件分类',
                             charset='utf8')
        cur = db.cursor()
        sql = "select * from email;"
        cur.execute(sql)
        db.commit()
        all_row = cur.fetchall()
        cur.close()
        db.close()
        return all_row

    def select_email_list(self):
        temp_list=[]
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='123456',
                             database='邮件分类',
                             charset='utf8')
        cur = db.cursor()
        sql = "select * from email;"
        cur.execute(sql)
        db.commit()
        all_row = cur.fetchall()
        for i in all_row:
            temp_list.append(list(i))
        cur.close()
        db.close()
        return temp_list

