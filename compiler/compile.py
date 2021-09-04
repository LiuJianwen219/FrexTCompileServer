import tornado.web
import zipfile
import os
from tornado.escape import json_decode
import config
from compiler import request_utils
from k8s_handler import k8s_handler
from compiler import constants as const


class CompileHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(config.request_failed)
        userId = self.get_argument("userId")
        testId = self.get_argument("testId")
        submitId = self.get_argument("submitId")
        topic = self.get_argument("topic")

#         count = len(os.listdir('/compiles/files/'))
#         print(count)
#         workPath = '/compiles/files/'+str(count)+'/'
# #        workPath = '/compiles/files/0/'
#         os.makedirs(workPath)
#         print(workPath)

        # if self.request.headers['Content-Type'] == 'application/x-json':
        #     self.args = json_decode(self.request.body)
        # print("start save file " +

        # fileMetas = self.request.files['file']

        print(self.get_arguments("asd"))
        print(self.get_argument("asd"))

        # for meta in fileMetas:
        #     filename=meta['filename']
        #     filepath=os.path.join(workPath, filename)
        #     print(filepath)
        #     with open(filepath, 'wb') as up:
        #         up.write(meta['body'])
        #     print("save file over" + tag)
        #
        #     print("start unzip " + tag)
        #     zFile = zipfile.ZipFile(filepath, "r")
        #     for fileM in zFile.namelist():
        #         zFile.extract(fileM, workPath)
        #     zFile.close()
        # print("unzip over " + tag)
        #
        # topModuleName = self.get_argument('topModuleName', 'top')
        # print(topModuleName)
        #
        # print("start compile file " + tag)
        # os.system('/tools/Xilinx/Vivado/2020.1/bin/vivado -mode batch -source main.tcl -tclargs ' + str(count) + ' ' + str(topModuleName))
        # print("compile file over " + tag)
        #
        # print("start to send file " + tag)
        # filename = workPath+"output/impl_1/"+topModuleName+".bit"
        # self.set_header ('Content-Type', 'application/octet-stream')
        # self.set_header ('Content-Disposition', 'attachment; filename='+filename)
        # with open(filename, 'rb') as f:
        #     while True:
        #         data = f.read(102400)
        #         if not data:
        #             break
        #         self.write(data)
        # self.finish()
        # print("send file over " + tag)
        # print("pid " + str(os.getpid()))

    def post(self, *args, **kwargs):
        print(args)
        print(kwargs)
        userId = self.get_argument("userId")
        testId = self.get_argument("testId")
        submitId = self.get_argument("submitId")
        topic = self.get_argument("topic")
        topModuleName = self.get_argument("topModuleName")
        values = {
            const.c_userId: userId,
            const.c_testId: testId,
            const.c_submitId: submitId,
            const.c_topic: topic,
            const.c_topModuleName: topModuleName,
            const.c_tclName: const.tcls_Name,
            const.c_fileServerUrl: config.file_server_url
        }
        kh = k8s_handler.k8s_handler()
        job = kh.create_job_object(values)
        kh.create_job(job)
        self.write(config.request_success)

    def write_error(self, status_code, **kwargs):
        self.write('Holly Shit Error? (%s) (%s)' % (status_code, "FrexT Compile Server"))
