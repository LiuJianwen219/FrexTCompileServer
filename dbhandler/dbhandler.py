#!/usr/bin/env python
import config
from tornado import ioloop, gen
import pymysql


class DbHandler:
    def __init__(self, values):
        self.host = values["host"]
        self.user = values["user"]
        self.password = values["password"]
        self.db = values["db"]
        self.port = values["port"]
        self.connection = pymysql.connect(self.host, self.user, self.password, self.db)

    def select_submit_message(self, uid):
        cursor = self.connection.cursor()
        try:
            print("SELECT message FROM home_submitlist WHERE uid='%s'" % uid)
            result = cursor.execute("SELECT message FROM home_submitlist WHERE uid='%s'" % uid)
            print(result)
            self.connection.commit()
            return cursor.fetchone()
        except Exception as e:
            print(str(e))
            self.connection.rollback()
        finally:
            cursor.close()
        return None

    def update_submit_message(self, uid, message):
        cursor = self.connection.cursor()
        try:
            uid = ''.join(filter(str.isalnum, uid))
            print("message+", message)
            print(uid)
            cursor.execute("UPDATE home_submitlist SET message='%s' WHERE uid='%s'" % (message, uid))
            self.connection.commit()
        except:
            self.connection.rollback()
        finally:
            cursor.close()

    def update_submit_status(self, uid, status):
        cursor = self.connection.cursor()
        try:
            uid = ''.join(filter(str.isalnum, uid))
            print("status+", status)
            print(uid)
            print("UPDATE home_submitlist SET status='%s' WHERE uid='%s'" % (status, uid))
            cursor.execute("UPDATE home_submitlist SET status='%s' WHERE uid='%s'" % (status, uid))
            self.connection.commit()
        except:
            self.connection.rollback()
        finally:
            cursor.close()

    def select_online_compile_message(self, uid):
        cursor = self.connection.cursor()
        try:
            print("SELECT message FROM experiment_compilerecord WHERE uid='%s'" % uid)
            result = cursor.execute("SELECT message FROM experiment_compilerecord WHERE uid='%s'" % uid)
            print(result)

            self.connection.commit()
            return cursor.fetchone()
        except Exception as e:
            print(str(e))
            self.connection.rollback()
        finally:
            cursor.close()
        return None

    def update_online_compile_message(self, uid, message):
        cursor = self.connection.cursor()
        try:
            print("is ok?")
            uid = ''.join(filter(str.isalnum, uid))
            print("message+", message)
            print(uid)
            cursor.execute("UPDATE experiment_compilerecord SET message='%s' WHERE uid='%s'" % (message, uid))
            self.connection.commit()
        except:
            self.connection.rollback()
        finally:
            cursor.close()

    def update_online_compile_status(self, uid, status):
        cursor = self.connection.cursor()
        try:
            print("i am wrong")
            uid = ''.join(filter(str.isalnum, uid))
            print("status+", status)
            print(uid)
            cursor.execute("UPDATE experiment_compilerecord SET status='%s' WHERE uid='%s'" % (status, uid))
            self.connection.commit()
        except:
            print("?")
            self.connection.rollback()
        finally:
            print("?")
            cursor.close()
        print("!")


def main():
    # ?????????????????????
    db = pymysql.connect(config.mysql_utl, config.mysql_name, config.mysql_passwd, config.mysql_db)

    # ?????? cursor() ?????????????????????????????? cursor
    cursor = db.cursor()

    # ?????? execute()  ???????????? SQL ??????
    cursor.execute("SELECT VERSION()")

    # ?????? fetchone() ????????????????????????.
    data = cursor.fetchone()

    print("Database version : %s " % data)

    # ?????????????????????
    db.close()


if __name__ == "__main__":
    # main()
    values = {
        "host": config.mysql_utl,
        "user": config.mysql_name,
        "password": config.mysql_passwd,
        "db": config.mysql_db,
        "port": 3306,
    }
    db = DbHandler(values)
    message = db.select_submit_message("480c82f6110b11ecbf0ef2e82abba5ba")
    # print(message)
    if db.update_submit_message("480c82f6110b11ecbf0ef2e82abba5ba", message[0]+" ljw.\n"):
        print('success')
    else:
        print("error")
