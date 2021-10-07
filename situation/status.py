import time

import requests
import tornado.web
from compiler import constants as const
from dbhandler import dbhandler
import logging, json
import config

logger = logging.getLogger(__name__)




class StatusHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        print(args)
        print(kwargs)
        userId = self.get_argument("userId")
        testId = self.get_argument("testId")
        submitId = self.get_argument("submitId")
        topic = self.get_argument("topic")
        status = self.get_argument("status")
        message = self.get_argument("message")

        # topModuleName = self.get_argument("topModuleName")
        values = {
            const.c_userId: userId,
            const.c_testId: testId,
            const.c_submitId: submitId,
            const.c_topic: topic,
            "status": status,
            "message": message
        }
        print(values)
        if update_status(values) == config.request_failed:
            self.set_status(404)
            self.set_header("language", "python")
            res = {
                "state": config.request_failed,
                "message": "Failed: status.\n",
                "content": values,
            }
            self.write(res)
        else:
            # 设置响应状态码
            self.set_status(200)
            # 设置头信息
            self.set_header("language", "python")
            # self.write方法除了帮我们将字典转换为json字符串之外，还帮我们将Content-Type设置为application/json; charset=UTF-8。
            res = {
                "state": config.request_success,
                "message": "Success: compile job started.\n",
                "content": values,
            }
            self.write(res)


def update_status(values):
    db_handler = dbhandler.DbHandler(values={
        "host": config.mysql_utl,
        "user": config.mysql_name,
        "password": config.mysql_passwd,
        "db": config.mysql_db,
        "port": 3306,
    })
    print(values)
    print(const.c_submitId)
    uid = ''.join(filter(str.isalnum, values[const.c_submitId]))
    message = db_handler.select_submit_message(uid)[0]
    print("message: "+message)
    if message:
        db_handler.update_submit_status(uid, values['status'])
        db_handler.update_submit_message(uid, message+values['message']+"\n")
        return config.request_success
    return config.request_failed


class StatusOnlineHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        print(args)
        print(kwargs)
        userId = self.get_argument("userId")
        experimentType = self.get_argument("experimentType")
        experimentId = self.get_argument("experimentId")
        compileId = self.get_argument("compileId")
        status = self.get_argument("status")
        message = self.get_argument("message")

        # topModuleName = self.get_argument("topModuleName")
        values = {
            const.c_userId: userId,
            const.c_experimentType: experimentType,
            const.c_experimentId: experimentId,
            const.c_compileId: compileId,
            "status": status,
            "message": message
        }
        print(values)
        if update_online_status(values) == config.request_failed:
            self.set_status(404)
            self.set_header("language", "python")
            res = {
                "state": config.request_failed,
                "message": "Failed: status.\n",
                "content": values,
            }
            self.write(res)
        else:
            # 设置响应状态码
            self.set_status(200)
            # 设置头信息
            self.set_header("language", "python")
            # self.write方法除了帮我们将字典转换为json字符串之外，还帮我们将Content-Type设置为application/json; charset=UTF-8。
            res = {
                "state": config.request_success,
                "message": "Success: compile job started.\n",
                "content": values,
            }
            self.write(res)


def update_online_status(values):
    db_handler = dbhandler.DbHandler(values={
        "host": config.mysql_utl,
        "user": config.mysql_name,
        "password": config.mysql_passwd,
        "db": config.mysql_online_db,
        "port": 3306,
    })
    print(values)
    uid = ''.join(filter(str.isalnum, values[const.c_compileId]))
    message = db_handler.select_online_compile_message(uid)[0]
    print("message: " + message)
    db_handler.update_online_compile_status(uid, values['status'])
    db_handler.update_online_compile_message(uid, message +
                                             str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) +
                                             " " + values['message'] + "\n")
    return config.request_success

