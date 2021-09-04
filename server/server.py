import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

from server.help import HelpHandler
from server.health import HealthHandler
from filehandler.upfile import UpfileHandler
from filehandler.downfile import DownfileHandler
from compiler.compile import CompileHandler


from tornado.options import define, options
define("port", default=8012, help="run on the given port ", type=int)
define("log_path", default='/tmp', help="log path ", type=str)

class CompileServer:
    def __init__(self, configs):
        print("config")
        print(configs)
        print(options.port)

    def init_compile_server(self):
        print("init")
        tornado.options.parse_command_line()
        app = tornado.web.Application(handlers=[
            (r"/help/", HelpHandler),
            (r"/ping/", HealthHandler),
            (r"/upfile/", UpfileHandler),
            (r"/downfile/", DownfileHandler),
            (r"/compile/", CompileHandler),
            (r"/", HelpHandler),
        ])
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)


    def run(self):
        print("run")
        tornado.ioloop.IOLoop.instance().start()