import json
import requests
import logging
from compile import constants as const

logger = logging.getLogger(__name__)


class SituationHandler:
    def __init__(self, values):
        self.values = values
        self.compile_server_url = values[const.c_compile_server_url]
        self.userId = values[const.c_userId]
        self.testId = values[const.c_testId]
        self.submitId = values[const.c_submitId]
        self.topic = values[const.c_topic]
        self.tclName = values[const.c_tcl]
        self.topModuleName = values[const.c_topModuleName]
        self.threadIndex = values[const.c_thread_index]
        pass

    def post_status(self, state, status, message):
        logger.info("Try to request Status: " + json.dumps(self.values))

        url = self.compile_server_url + const.status_API + "/"
        values = {
            const.c_userId: self.userId,
            const.c_testId: self.testId,
            const.c_submitId: self.submitId,
            const.c_topic: self.topic,
            "state": state,
            "status": status,
            "message": message,
            const.c_thread_index: self.threadIndex,
        }
        data = {
            "state": state,
            "status": status,
            "message": message,
            const.c_thread_index: self.threadIndex,
        }
        r = requests.post(url=url, params=values, data=data)
        if r.status_code.__str__() != "200":
            logger.error("Request STATUS failed: " + r.headers.__str__())
            return const.request_failed

        logger.info("Receive response: " + r.content.__str__())
        return const.request_success

    def post_result(self, state, status, message):
        logger.info("Try to request Result: " + json.dumps(self.values))

        url = self.compile_server_url + const.result_API + "/"
        values = {
            const.c_userId: self.userId,
            const.c_testId: self.testId,
            const.c_submitId: self.submitId,
            const.c_topic: self.topic,
            "state": state,
            "status": status,
            "message": message,
            const.c_thread_index: self.threadIndex,
        }
        data = {
            "state": state,
            "status": status,
            "message": message,
            const.c_thread_index: self.threadIndex,
        }
        r = requests.post(url=url, params=values, data=data)
        if r.status_code.__str__() != "200":
            logger.error("Request RESULT failed: " + r.headers.__str__())
            return const.request_failed

        logger.info("Receive response: " + r.content.__str__())
        return const.request_success


class SituationOnlineHandler:
    def __init__(self, values):
        self.values = values
        self.compile_server_url = values[const.c_compile_server_url]
        self.userId = values[const.c_userId]
        self.tclName = values[const.c_tcl]
        self.topModuleName = values[const.c_topModuleName]
        self.threadIndex = values[const.c_thread_index]
        self.experimentType = values[const.c_experimentType]
        self.experimentId = values[const.c_experimentId]
        self.compileId = values[const.c_compileId]
        pass

    def post_online_status(self, state, status, message):
        logger.info("Try to request Status: " + json.dumps(self.values))

        url = self.compile_server_url + const.status_online_API + "/"
        values = {
            const.c_userId: self.userId,
            const.c_experimentType: self.experimentType,
            const.c_experimentId: self.experimentId,
            const.c_compileId: self.compileId,
            "state": state,
            "status": status,
            "message": message,
            const.c_thread_index: self.threadIndex,
        }
        data = {
            "state": state,
            "status": status,
            "message": message,
            const.c_thread_index: self.threadIndex,
        }
        r = requests.post(url=url, params=values, data=data)
        if r.status_code.__str__() != "200":
            logger.error("Request STATUS failed: " + r.headers.__str__())
            return const.request_failed

        logger.info("Receive response: " + r.content.__str__())
        return const.request_success

    def post_online_result(self, state, status, message):
        logger.info("Try to request Result: " + json.dumps(self.values))

        url = self.compile_server_url + const.result_online_API + "/"
        values = {
            const.c_userId: self.userId,
            const.c_experimentType: self.experimentType,
            const.c_experimentId: self.experimentId,
            const.c_compileId: self.compileId,
            const.c_topModuleName: self.topModuleName,
            "state": state,
            "status": status,
            "message": message,
            const.c_thread_index: self.threadIndex,
        }
        data = {
            "state": state,
            "status": status,
            "message": message,
            const.c_thread_index: self.threadIndex,
        }
        r = requests.post(url=url, params=values, data=data)
        if r.status_code.__str__() != "200":
            logger.error("Request RESULT failed: " + r.headers.__str__())
            return const.request_failed

        logger.info("Receive response: " + r.content.__str__())
        return const.request_success
