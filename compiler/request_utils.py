import json
import shutil
import uuid

import requests
import logging
import os
from compiler import constants as const
import config
from filehandler import filehandler

logger = logging.getLogger(__name__)


class FileRequest:
    def __init__(self, values):
        self.values = values

    def make_work_dir(self):
        userId = self.values[const.c_userId]
        testId = self.values[const.c_testId]
        submitId = self.values[const.c_submitId]
        topic = self.values[const.c_topic]
        tclName = self.values[const.c_tclName]

        sub_work_dir = uuid.uuid1().__str__()
        work_dir = os.path.join(const.compile_job_tmp_work_dir, sub_work_dir)
        os.mkdir(work_dir)

        ques_src = os.path.join(const.see_path, const.sys_dir, const.c_testing, testId, topic + const.questions_suffix)
        shutil.copyfile(ques_src, os.path.join(work_dir, topic + const.questions_suffix)) # always new for every job
        test_src = os.path.join(const.see_path, const.user_dir, userId, const.c_testing, testId, submitId, topic + const.tests_suffix)
        shutil.copyfile(test_src, os.path.join(work_dir, topic + const.tests_suffix))  # always new for every job
        main_src = os.path.join(const.see_path, const.user_dir, userId, const.c_testing, testId, submitId, tclName + const.tcls_suffix)
        shutil.copyfile(main_src, os.path.join(work_dir, topic + const.tcls_suffix))  # always new for every job
        return sub_work_dir

    def get_tcls(self):
        logger.info("Try to request TCL with values: " + json.dumps(self.values))
        userId = self.values[const.c_userId]
        testId = self.values[const.c_testId]
        submitId = self.values[const.c_submitId]
        tclName = self.values[const.c_tclName]
        api = const.tcls_API

        url = config.file_server_url + api + "/"
        values = {}
        r = requests.get(url, params=values)
        if r.status_code.__str__() != "200":
            logger.error("Request TCL failed: " + r.headers.__str__())
            return

        if r.headers['content-type'] == "application/octet-stream":
            dest_direction = os.path.join(const.see_path, const.user_dir,
                                          userId, const.c_testing, testId, submitId)
            dest_filename = tclName + const.tcls_suffix
            filehandler.file_writer(dest_direction, dest_filename, r.content)

    def get_questions(self):
        logger.info("Try to request QUESTION with values: " + json.dumps(self.values))
        testId = self.values[const.c_testId]
        topic = self.values[const.c_topic]
        api = const.questions_API

        url = config.file_server_url + api + "/"
        values = {
            const.c_testId: testId,
            const.c_topic: topic
        }
        r = requests.get(url, params=values)
        if r.status_code.__str__() != "200":
            logger.error("Request QUESTION failed: " + r.headers.__str__())
            return

        if r.headers['content-type'] == "application/octet-stream":
            dest_direction = os.path.join(const.see_path, const.sys_dir,
                                          const.c_testing, testId)
            dest_filename = topic + const.questions_suffix
            filehandler.file_writer(dest_direction, dest_filename, r.content)

    def get_tests(self):
        logger.info("Try to request TEST with values: " + json.dumps(self.values))
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
        if r.status_code.__str__() != "200":
            logger.error("Request TEST failed: " + r.headers.__str__())
            return

        if r.headers['content-type'] == "application/octet-stream":
            dest_direction = os.path.join(const.see_path, const.user_dir,
                                          userId, const.c_testing, testId, submitId)
            dest_filename = topic + const.tests_suffix
            filehandler.file_writer(dest_direction, dest_filename, r.content)

    def post_logs(self):
        logger.info("Try to request LOG with values: " + json.dumps(self.values))
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

        sour_direction = os.path.join(const.see_path, const.user_dir,
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
        if r.status_code.__str__() != "200":
            logger.error("Post LOG failed: request status not health: " + r.headers.__str__())
            return

    def post_bits(self):
        logger.info("Try to request BIT with values: " + json.dumps(self.values))
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

        sour_direction = os.path.join(const.see_path, const.user_dir,
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
        if r.status_code.__str__() != "200":
            logger.error("Post BIT failed: request status not health: " + r.headers.__str__())
            return
