import os

import tornado.web
import subprocess
from compile import utils
from compile import constants as const


def compile_project(values):
    print("Compile with values: ", values)
    fh = utils.FileRequest(values)
    fh.get_tcls()
    fh.get_questions()
    fh.get_tests()

    res = subprocess.call([
        "/bin/bash",
        const.compileScript,# 0
        os.path.join(const.work_dir, values[const.c_topic] + const.questions_suffix),# 1
        os.path.join(const.work_dir, values[const.c_topic]),# 2
        const.vivado,  # vivado.exe dir     # 3
        os.path.join(const.work_dir, values[const.c_tcl] + const.tcls_suffix), # 4 main.tcl
        const.FPGAVersion,                  # 5 FPGAVersion
        os.path.join(const.work_dir),       # 6 workDir
        values[const.c_topModuleName],      # 7 topModuleName
        const.compileThread,                # 8 threads
    ], shell=False)
    print("Compile result: ", res)

    fh.post_logs()
    fh.post_bits()

# class CompileHandler(tornado.web.RequestHandler):
#     def post(self, *args, **kwargs):
#         print(args)
#         print(kwargs)
#         userId = self.get_argument("userId")
#         testId = self.get_argument("testId")
#         submitId = self.get_argument("submitId")
#         topic = self.get_argument("topic")
#         topModuleName = self.get_argument("topModuleName")
#         values = {
#             "userId": userId,
#             "testId": testId,
#             "submitId": submitId,
#             "topic": topic,
#             "topModuleName": topModuleName,
#             "tclName": const.tcls_Name,
#             const.c_file_server_url: "",
#         }
#         fh = utils.FileRequest(values)
#         fh.get_tcls()
#         fh.get_questions()
#         fh.get_tests()
#
#         subprocess.call([
#             "/bin/bash",
#             const.compileScript,
#             os.path.join(const.work_dir, topic + const.questions_suffix),
#             os.path.join(const.work_dir, topic),
#             const.vivado,  # vivado.exe dir
#             os.path.join(const.work_dir, topic + const.tcls_suffix),
#             const.FPGAVersion,
#             os.path.join(const.work_dir),
#             topModuleName,
#             const.compileThread,
#         ], shell=False)
#
#         fh.post_logs()
#         fh.post_bits()
#
#         self.write(const.request_success)
#
#     def write_error(self, status_code, **kwargs):
#         self.write('Holly Shit Error? %s %s' % (status_code, const.request_failed))
