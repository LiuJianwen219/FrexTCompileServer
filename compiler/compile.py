
import tornado.web
import zipfile
import os

from tornado.escape import json_decode

tag = "das"


class CompileHandler(tornado.web.RequestHandler):
    #def get(self, filename):
    def get(self):
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
        print(self.get_arguments("userName"))

    def write_error(self, status_code, **kwargs):
        self.write('Holly Shit Error? %s %s' % (status_code, tag))
