import json
import logging
import requests
import tornado.web
import config
from compiler import constants as const

logger = logging.getLogger(__name__)


class ResultHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        print(args)
        print(kwargs)
        userId = self.get_argument("userId")
        testId = self.get_argument("testId")
        submitId = self.get_argument("submitId")
        topic = self.get_argument("topic")
        state = self.get_argument("state")
        status = self.get_argument("status")
        message = self.get_argument("message")
        threadIndex = self.get_argument("threadIndex")

        print(state)

        values = {
            const.c_userId: userId,
            const.c_testId: testId,
            const.c_submitId: submitId,
            const.c_topic: topic,
            "state": state,
            "status": status,
            "message": message,
            "threadIndex": threadIndex,
        }
        if update_result(values) == config.request_failed:
            self.set_status(404)
            self.set_header("language", "python")
            res = {
                "state": config.request_failed,
                "message": "Failed: result.\n",
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
                "message": "Success: result.\n",
                "content": values,
            }
            self.write(res)


def update_result(values):
    logger.info("Try to request Result: " + json.dumps(values))
    url = config.web_server_url + config.web_server_api_compile_result + "/"

    print(url)
    print(values)

    r = requests.post(url=url, params=values, data=values)

    if r.status_code.__str__() != "200":
        logger.error("Request Result failed: " + r.headers.__str__())
        return config.request_failed

    logger.info("Receive response: " + r.content.__str__())
    return config.request_success
