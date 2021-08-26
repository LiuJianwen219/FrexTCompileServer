import json
import shutil
import uuid

import requests
import logging
import os
from compile import constants as const
from compile import filehandler


logger = logging.getLogger(__name__)


class FileRequest:
    def __init__(self, values):
        self.values = values
        self.file_server_url = values[const.c_file_server_url]
        self.userId = values[const.c_userId]
        self.testId = values[const.c_testId]
        self.submitId = values[const.c_submitId]
        self.topic = values[const.c_topic]
        self.tclName = values[const.c_tcl]
        self.topModuleName = values[const.c_topModuleName]

    # def make_work_dir(self):
    #     sub_work_dir = uuid.uuid1().__str__()
    #     work_dir = os.path.join(const.compile_job_tmp_work_dir, sub_work_dir)
    #     os.mkdir(work_dir)
    #     # always new for every job
    #     ques_src = os.path.join(const.see_path, const.sys_dir,
    #                             const.c_testing, self.testId,
    #                             self.topic + const.questions_suffix)
    #     shutil.copyfile(ques_src, os.path.join(work_dir, self.topic + const.questions_suffix))
    #     test_src = os.path.join(const.see_path, const.user_dir,
    #                             self.userId, const.c_testing,
    #                             self.testId, self.submitId,
    #                             self.topic + const.tests_suffix)
    #     shutil.copyfile(test_src, os.path.join(work_dir, self.topic + const.tests_suffix))
    #     main_src = os.path.join(const.see_path, const.user_dir,
    #                             self.userId, const.c_testing,
    #                             self.testId, self.submitId,
    #                             self.tclName + const.tcls_suffix)
    #     shutil.copyfile(main_src, os.path.join(work_dir, self.topic + const.tcls_suffix))
    #     return sub_work_dir

    def get_tcls(self):
        logger.info("Try to request TCL with values: " + json.dumps(self.values))

        url = self.file_server_url + const.tcls_API + "/"
        values = {}
        r = requests.get(url, params=values)
        if r.status_code.__str__() != "200":
            logger.error("Request TCL failed: " + r.headers.__str__())
            return

        if r.headers['content-type'] == "application/octet-stream":
            dest_direction = const.work_dir
            dest_filename = self.tclName + const.tcls_suffix
            filehandler.file_writer(dest_direction, dest_filename, r.content)

    def get_questions(self):
        logger.info("Try to request QUESTION with values: " + json.dumps(self.values))

        url = self.file_server_url + const.questions_API + "/"
        values = {
            const.c_testId: self.testId,
            const.c_topic: self.topic
        }
        r = requests.get(url, params=values)
        if r.status_code.__str__() != "200":
            logger.error("Request QUESTION failed: " + r.headers.__str__())
            return

        if r.headers['content-type'] == "application/octet-stream":
            dest_direction = const.work_dir
            dest_filename = self.topic + const.questions_suffix
            filehandler.file_writer(dest_direction, dest_filename, r.content)

    def get_tests(self):
        logger.info("Try to request TEST with values: " + json.dumps(self.values))

        url = self.file_server_url + const.tests_API + "/"
        values = {
            const.c_userId: self.userId,
            const.c_testId: self.testId,
            const.c_submitId: self.submitId,
            const.c_topic: self.topic
        }
        r = requests.get(url, params=values)
        if r.status_code.__str__() != "200":
            logger.error("Request TEST failed: " + r.headers.__str__())
            return

        if r.headers['content-type'] == "application/octet-stream":
            dest_direction = const.work_dir
            dest_filename = self.topic + const.tests_suffix
            filehandler.file_writer(dest_direction, dest_filename, r.content)

    def post_logs(self):
        logger.info("Try to request LOG with values: " + json.dumps(self.values))

        url = self.file_server_url + const.logs_API + "/"
        values = {
            const.c_userId: self.userId,
            const.c_testId: self.testId,
            const.c_submitId: self.submitId,
            const.c_topic: self.topic,
            const.c_topModuleName: self.topModuleName,
        }

        sour_direction = const.work_dir
        sour_filename = self.topModuleName + const.logs_suffix
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

        url = self.file_server_url + const.bits_API + "/"
        values = {
            const.c_userId: self.userId,
            const.c_testId: self.testId,
            const.c_submitId: self.submitId,
            const.c_topic: self.topic
        }

        sour_direction = const.work_dir
        sour_filename = self.topModuleName + const.bits_suffix
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
