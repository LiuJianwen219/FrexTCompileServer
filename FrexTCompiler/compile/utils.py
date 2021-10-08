import json

import requests
import logging
import os
from compile import constants as const
from compile import filehandler
from compile.ZipUtilities import ZipUtilities


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

    def get_tcl(self):
        logger.info("Try to request TCL with values: " + json.dumps(self.values))

        url = self.file_server_url + const.tcls_API + "/"
        values = {}
        r = requests.get(url, params=values)
        if r.status_code.__str__() != "200":
            logger.error("Request TCL failed: " + r.headers.__str__())
            return const.request_failed

        if r.headers['content-type'] == "application/octet-stream" and r.content:
            dest_direction = const.work_dir
            dest_filename = self.tclName + const.tcls_suffix
            if not filehandler.file_writer(dest_direction, dest_filename, r.content):
                return const.request_failed
            return const.request_success
        return const.request_failed

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
            return const.request_failed

        if r.headers['content-type'] == "application/octet-stream" and r.content:
            dest_direction = const.work_dir
            dest_filename = self.topic + const.questions_suffix
            if not filehandler.file_writer(dest_direction, dest_filename, r.content):
                return const.request_failed
            return const.request_success
        return const.request_failed

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
            return const.request_failed

        if r.headers['content-type'] == "application/octet-stream" and r.content:
            dest_direction = const.work_dir
            dest_filename = self.topic + const.tests_suffix
            if not filehandler.file_writer(dest_direction, dest_filename, r.content):
                return const.request_failed
            return const.request_success
        return const.request_failed

    def post_log(self):
        logger.info("Try to request LOG with values: " + json.dumps(self.values))

        url = self.file_server_url + const.logs_API + "/"
        values = {
            const.c_userId: self.userId,
            const.c_testId: self.testId,
            const.c_submitId: self.submitId,
            const.c_topic: self.topic,
        }

        sour_direction = const.work_dir
        sour_filename = self.topModuleName + const.logs_suffix
        source = os.path.join(sour_direction, sour_filename)
        content = filehandler.file_reader(source)
        if content is None:
            logger.error("Post LOG failed, file not found.")
            return const.request_failed

        # files = {'file': ('nameoffile', open('namoffile', 'rb'), 'text/html', 'other header'),
        #          'file2': ('nameoffile2', open('nameoffile2', 'rb'), 'application/xml', 'other header')}
        files = {'file': content}
        r = requests.post(url, files=files, data=values)
        if r.status_code.__str__() != "200":
            logger.error("Post LOG failed: request status not health: " + r.headers.__str__())
            return const.request_failed
        return const.request_success

    def post_rpt(self):
        logger.info("Try to request RPT with values: " + json.dumps(self.values))

        url = self.file_server_url + const.rpts_API + "/"
        values = {
            const.c_userId: self.userId,
            const.c_testId: self.testId,
            const.c_submitId: self.submitId,
            const.c_topic: self.topic,
        }

        sour_direction = os.path.join(const.work_dir, "output", "impl_1")
        sour_filename = self.topModuleName + const.rpts_suffix
        source = os.path.join(sour_direction, sour_filename)
        content = filehandler.file_reader(source)
        if content is None:
            logger.error("Post RPT failed, file not found.")
            return const.request_failed

        # files = {'file': ('nameoffile', open('namoffile', 'rb'), 'text/html', 'other header'),
        #          'file2': ('nameoffile2', open('nameoffile2', 'rb'), 'application/xml', 'other header')}
        files = {'file': content}
        r = requests.post(url, files=files, data=values)
        if r.status_code.__str__() != "200":
            logger.error("Post LOG failed: request status not health: " + r.headers.__str__())
            return const.request_failed
        return const.request_success

    def post_project(self):
        logger.info("Try to request PROJECT with values: " + json.dumps(self.values))

        url = self.file_server_url + const.projects_API + "/"
        values = {
            const.c_userId: self.userId,
            const.c_testId: self.testId,
            const.c_submitId: self.submitId,
            const.c_topic: self.topic,
        }

        utilities = ZipUtilities()
        utilities.toZip(const.work_dir, "")
        sour_direction = const.work_dir
        sour_filename = self.topModuleName + const.projects_suffix
        source = os.path.join(sour_direction, sour_filename)
        utilities.toLocal(source)

        content = filehandler.file_reader(source)
        if content is None:
            logger.error("Post RPT failed, file not found.")
            return const.request_failed

        # files = {'file': ('nameoffile', open('namoffile', 'rb'), 'text/html', 'other header'),
        #          'file2': ('nameoffile2', open('nameoffile2', 'rb'), 'application/xml', 'other header')}
        files = {'file': content}
        r = requests.post(url, files=files, data=values)
        if r.status_code.__str__() != "200":
            logger.error("Post PROJECT failed: request status not health: " + r.headers.__str__())
            return const.request_failed
        return const.request_success

    def post_bit(self):
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
            return const.request_failed

        # files = {'file': ('nameoffile', open('namoffile', 'rb'), 'text/html', 'other header'),
        #          'file2': ('nameoffile2', open('nameoffile2', 'rb'), 'application/xml', 'other header')}
        files = {'file': content}
        r = requests.post(url, files=files, data=values)
        if r.status_code.__str__() != "200":
            logger.error("Post BIT failed: request status not health: " + r.headers.__str__())
            return const.request_failed
        return const.request_success


class FileOnlineRequest:
    def __init__(self, values):
        self.values = values
        self.file_server_url = values[const.c_file_server_url]
        self.userId = values[const.c_userId]
        self.experimentType = values[const.c_experimentType]
        self.experimentId = values[const.c_experimentId]
        self.compileId = values[const.c_compileId]
        self.tclName = values[const.c_tcl]
        self.topModuleName = values[const.c_topModuleName]

    def get_tcl(self):
        logger.info("Try to request TCL with values: " + json.dumps(self.values))

        url = self.file_server_url + const.tcls_API + "/"
        values = {}
        r = requests.get(url, params=values)
        if r.status_code.__str__() != "200":
            logger.error("Request TCL failed: " + r.headers.__str__())
            return const.request_failed

        if r.headers['content-type'] == "application/octet-stream" and r.content:
            dest_direction = const.work_dir
            dest_filename = self.tclName + const.tcls_suffix
            if not filehandler.file_writer(dest_direction, dest_filename, r.content):
                return const.request_failed
            return const.request_success
        return const.request_failed

    def get_src(self, fileName):
        logger.info("Try to request SRC with values: " + json.dumps(self.values))

        url = self.file_server_url + const.src_API + "/"
        values = {
            const.c_userId: self.userId,
            const.c_experimentType: self.experimentType,
            const.c_experimentId: self.experimentId,
            const.c_compileId: self.compileId,
            const.c_fileName: fileName
        }
        r = requests.get(url, params=values)
        if r.status_code.__str__() != "200":
            logger.error("Request SRC failed: " + r.headers.__str__())
            return const.request_failed

        if r.headers['content-type'] == "application/octet-stream" and r.content:
            dest_direction = const.work_dir
            dest_filename = fileName
            if not filehandler.file_writer(dest_direction, dest_filename, r.content):
                return const.request_failed
            return const.request_success
        return const.request_failed

    def post_online_log(self):
        logger.info("Try to request online LOG with values: " + json.dumps(self.values))

        url = self.file_server_url + const.logs_online_API + "/"
        values = {
            const.c_userId: self.userId,
            const.c_experimentType: self.experimentType,
            const.c_experimentId: self.experimentId,
            const.c_compileId: self.compileId,
            const.c_topModuleName: self.topModuleName,
        }
        print(values)

        sour_direction = const.work_dir
        sour_filename = self.topModuleName + const.logs_suffix
        source = os.path.join(sour_direction, sour_filename)
        content = filehandler.file_reader(source)
        if content is None:
            logger.error("Post online LOG failed, file not found.")
            return const.request_failed

        # files = {'file': ('nameoffile', open('namoffile', 'rb'), 'text/html', 'other header'),
        #          'file2': ('nameoffile2', open('nameoffile2', 'rb'), 'application/xml', 'other header')}
        files = {'file': content}
        r = requests.post(url, files=files, data=values)
        if r.status_code.__str__() != "200":
            logger.error("Post online LOG failed: request status not health: " + r.headers.__str__())
            return const.request_failed
        return const.request_success

    def post_online_rpt(self):
        logger.info("Try to request RPT with values: " + json.dumps(self.values))

        url = self.file_server_url + const.rpts_online_API + "/"
        values = {
            const.c_userId: self.userId,
            const.c_experimentType: self.experimentType,
            const.c_experimentId: self.experimentId,
            const.c_compileId: self.compileId,
            const.c_topModuleName: self.topModuleName,
        }

        sour_direction = os.path.join(const.work_dir, "output", "impl_1")
        sour_filename = self.topModuleName + const.rpts_suffix
        source = os.path.join(sour_direction, sour_filename)
        content = filehandler.file_reader(source)
        if content is None:
            logger.error("Post RPT failed, file not found.")
            return const.request_failed

        # files = {'file': ('nameoffile', open('namoffile', 'rb'), 'text/html', 'other header'),
        #          'file2': ('nameoffile2', open('nameoffile2', 'rb'), 'application/xml', 'other header')}
        files = {'file': content}
        r = requests.post(url, files=files, data=values)
        if r.status_code.__str__() != "200":
            logger.error("Post LOG failed: request status not health: " + r.headers.__str__())
            return const.request_failed
        return const.request_success

    def post_online_project(self):
        logger.info("Try to request PROJECT with values: " + json.dumps(self.values))

        url = self.file_server_url + const.projects_online_API + "/"
        values = {
            const.c_userId: self.userId,
            const.c_experimentType: self.experimentType,
            const.c_experimentId: self.experimentId,
            const.c_compileId: self.compileId,
            const.c_topModuleName: self.topModuleName,
        }

        utilities = ZipUtilities()
        utilities.toZip(const.work_dir, "")
        sour_direction = const.work_dir
        sour_filename = self.topModuleName + const.projects_suffix
        source = os.path.join(sour_direction, sour_filename)
        utilities.toLocal(source)

        content = filehandler.file_reader(source)
        if content is None:
            logger.error("Post RPT failed, file not found.")
            return const.request_failed

        # files = {'file': ('nameoffile', open('namoffile', 'rb'), 'text/html', 'other header'),
        #          'file2': ('nameoffile2', open('nameoffile2', 'rb'), 'application/xml', 'other header')}
        files = {'file': content}
        r = requests.post(url, files=files, data=values)
        if r.status_code.__str__() != "200":
            logger.error("Post PROJECT failed: request status not health: " + r.headers.__str__())
            return const.request_failed
        return const.request_success


    def post_online_bit(self):
        logger.info("Try to request online BIT with values: " + json.dumps(self.values))

        url = self.file_server_url + const.bits_online_API + "/"
        values = {
            const.c_userId: self.userId,
            const.c_experimentType: self.experimentType,
            const.c_experimentId: self.experimentId,
            const.c_compileId: self.compileId,
        }

        sour_direction = const.work_dir
        sour_filename = self.topModuleName + const.bits_suffix
        source = os.path.join(sour_direction, sour_filename)
        content = filehandler.file_reader(source)
        if content is None:
            logger.error("Post online BIT failed, file not found.")
            return const.request_failed

        # files = {'file': ('nameoffile', open('namoffile', 'rb'), 'text/html', 'other header'),
        #          'file2': ('nameoffile2', open('nameoffile2', 'rb'), 'application/xml', 'other header')}
        files = {'file': content}
        r = requests.post(url, files=files, data=values)
        if r.status_code.__str__() != "200":
            logger.error("Post online BIT failed: request status not health: " + r.headers.__str__())
            return const.request_failed
        return const.request_success
