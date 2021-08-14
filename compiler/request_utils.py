import requests
import logging
import os
from compiler import constants as const
import config
from filehandler import filehandler

logger = logging.getLogger(__name__)


class FileHandler:
    def __init__(self, values):
        self.values = values

    def get_tests(self):
        logger.info("Try to request TEST with values: " + self.values)
        userId = self.values[const.c_userId]
        testId = self.values[const.c_testId]
        submitId = self.values[const.c_submitId]
        topic = self.values[const.c_topic]
        api = const.tests_API

        url = config.file_server_url + api + "/"
        values = {
            const.c_userId: userId,
            const.c_testId: testId,
            const.c_submitId: submitId,
            const.c_topic: topic
        }
        r = requests.get(url, params=values)
        if r.status_code != "200":
            logger.error("Request TEST failed: " + r.headers.__str__())
            return

        if r.headers['content-type'] == "application/octet-stream":
            dest_direction = os.path.join(config.compile_file_tmp_root, const.user_dir,
                                          userId, const.c_testing, testId, submitId)
            dest_filename = topic + const.tests_suffix
            filehandler.file_writer(dest_direction, dest_filename, r.content)

    def get_questions(self):
        logger.info("Try to request QUESTION with values: " + self.values)
        testId = self.values[const.c_testId]
        topic = self.values[const.c_topic]
        api = const.questions_API

        url = config.file_server_url + api + "/"
        values = {
            const.c_testId: testId,
            const.c_topic: topic
        }
        r = requests.get(url, params=values)
        if r.status_code != "200":
            logger.error("Request QUESTION failed: " + r.headers.__str__())
            return

        if r.headers['content-type'] == "application/octet-stream":
            dest_direction = os.path.join(config.compile_file_tmp_root, const.sys_dir,
                                          const.c_testing, testId)
            dest_filename = topic + const.questions_suffix
            filehandler.file_writer(dest_direction, dest_filename, r.content)

    def post_bits(self):
        logger.info("Try to request BIT with values: " + self.values)
        userId = self.values[const.c_userId]
        testId = self.values[const.c_testId]
        submitId = self.values[const.c_submitId]
        topic = self.values[const.c_topic]
        api = const.bits_API

        url = config.file_server_url + api + "/"
        values = {
            const.c_userId: userId,
            const.c_testId: testId,
            const.c_submitId: submitId,
            const.c_topic: topic
        }

        sour_direction = os.path.join(config.compile_file_tmp_root, const.user_dir,
                                      userId, const.c_testing, testId, submitId)
        sour_filename = topic + const.bits_suffix
        source = os.path.join(sour_direction, sour_filename)
        content = filehandler.file_reader(source)
        if content is None:
            logger.error("Post BIT failed, file not found.")
            return

        # files = {'file': ('nameoffile', open('namoffile', 'rb'), 'text/html', 'other header'),
        #          'file2': ('nameoffile2', open('nameoffile2', 'rb'), 'application/xml', 'other header')}
        files = {'file': content}
        r = requests.post(url, files=files, data=values)
        if r.status_code != "200":
            logger.error("Post BIT failed: request status not health: " + r.headers.__str__())
            return

    def post_logs(self):
        logger.info("Try to request LOG with values: " + self.values)
        userId = self.values[const.c_userId]
        testId = self.values[const.c_testId]
        submitId = self.values[const.c_submitId]
        topic = self.values[const.c_topic]
        api = const.logs_API

        url = config.file_server_url + api + "/"
        values = {
            const.c_userId: userId,
            const.c_testId: testId,
            const.c_submitId: submitId,
            const.c_topic: topic
        }

        sour_direction = os.path.join(config.compile_file_tmp_root, const.user_dir,
                                      userId, const.c_testing, testId, submitId)
        sour_filename = topic + const.logs_suffix
        source = os.path.join(sour_direction, sour_filename)
        content = filehandler.file_reader(source)
        if content is None:
            logger.error("Post LOG failed, file not found.")
            return

        # files = {'file': ('nameoffile', open('namoffile', 'rb'), 'text/html', 'other header'),
        #          'file2': ('nameoffile2', open('nameoffile2', 'rb'), 'application/xml', 'other header')}
        files = {'file': content}
        r = requests.post(url, files=files, data=values)
        if r.status_code != "200":
            logger.error("Post LOG failed: request status not health: " + r.headers.__str__())
            return
