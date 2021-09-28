import json

import tornado.web
import config
from k8s_handler import k8s_handler
from compiler import constants as const
from situation import status


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
        threadIndex = self.get_argument("threadIndex")

        values = {
            const.c_userId: userId,
            const.c_testId: testId,
            const.c_submitId: submitId,
            const.c_topic: topic,
            const.c_topModuleName: topModuleName,
            const.c_tclName: const.tcls_Name,
            const.c_fileServerUrl: config.file_server_url,
            const.c_compile_server_url: config.compile_server_url,
            "state": config.request_success,
            "status": "开始处理编译任务",
            "message": "Success start to compile\n",
            const.c_thread_index: threadIndex,
        }
        status.update_status(values)

        kh = k8s_handler.k8s_handler()
        job = kh.create_job_object(values)

        # 设置响应状态码
        self.set_status(200)
        # 设置头信息
        self.set_header("language", "python")
        # self.write方法除了帮我们将字典转换为json字符串之外，还帮我们将Content-Type设置为application/json; charset=UTF-8。
        res = {
            "state": config.request_success,
            "status": "编译任务处理完成",
            "message": "Success: compile job started.\n",
            "content": values,
        }
        self.write(json.dumps(res))

        kh.create_job(job)

    def write_error(self, status_code, **kwargs):
        self.write('Holly Shit Error? (%s) (%s)' % (status_code, "FrexT Compile Server"))

class CompileOnlineHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        print(args)
        print(kwargs)
        userId = self.get_argument("userId")
        experimentType = self.get_argument("experimentType")
        experimentId = self.get_argument("experimentId")
        compileId = self.get_argument("compileId")
        fileNames = json.dumps(self.get_arguments("fileNames"))
        topModuleName = self.get_argument("topModuleName")
        threadIndex = self.get_argument("threadIndex")

        values = {
            const.c_userId: userId,
            const.c_experimentType: experimentType,
            const.c_experimentId: experimentId,
            const.c_compileId: compileId,
            const.c_topModuleName: topModuleName,
            const.c_fileNames: fileNames,
            const.c_tclName: const.tcls_Name,
            const.c_fileServerUrl: config.file_server_url,
            const.c_compile_server_url: config.compile_server_url,
            "state": config.request_success,
            "status": "开始处理编译任务",
            "message": "Success start to compile\n",
            const.c_thread_index: threadIndex,
        }
        status.update_online_status(values)

        kh = k8s_handler.k8s_handler()
        job = kh.create_online_job_object(values)

        # 设置响应状态码
        self.set_status(200)
        # 设置头信息
        self.set_header("language", "python")
        # self.write方法除了帮我们将字典转换为json字符串之外，还帮我们将Content-Type设置为application/json; charset=UTF-8。
        res = {
            "state": config.request_success,
            "status": "编译任务处理完成",
            "message": "Success: compile job started.\n",
            "content": values,
        }
        self.write(json.dumps(res))

        kh.create_job(job)

    def write_error(self, status_code, **kwargs):
        self.write('Holly Shit Error? (%s) (%s)' % (status_code, "FrexT Compile Server"))

