import os
import tornado.web

tag = "downfile"


class DownfileHandler(tornado.web.RequestHandler):
    def get(self):
        filename = "download.txt"
        print('i download file handler : ', filename)
        self.set_header ('Content-Type', 'application/octet-stream')
        self.set_header ('Content-Disposition', 'attachment; filename='+filename)
        with open(filename, 'rb') as f:
            while True:
                data = f.read(10240)
                if not data:
                    break
                self.write(data)
        self.finish()

    def post(self):
        upload_path = os.path.join(os.path.dirname(__file__), 'files')
        file_metas = self.request.files['file']
        for meta in file_metas:
            filename = meta['filename']
            filepath = os.path.join(upload_path, filename)
            print(filepath)
            with open(filepath, 'wb') as up:
                up.write(meta['body'])
            self.write('finished! ' + tag)

    def write_error(self, status_code, **kwargs):
        self.write('Holly Shit Error? %s %s' % (status_code, tag))
