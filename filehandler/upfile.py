import os

import tornado.web

tag = "upfile"

class UpfileHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''
        <html>
          <head><title>Upload File</title></head>
          <body>
            <p>''' + tag + '''<p>
            </form>
          </body>
        </html>
        ''')

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
        self.write('Holly Shit Error %s' % status_code)
