import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

from server.help import HelpHandler
from server.health import HealthHandler
from filehandler.upfile import UpfileHandler
from filehandler.downfile import DownfileHandler
from compiler.compile import CompileHandler, CompileOnlineHandler
from situation.status import StatusHandler, StatusOnlineHandler
from situation.result import ResultHandler, ResultOnlineHandler


from tornado.options import define, options
define("port", default=8012, help="run on the given port ", type=int)
define("log_path", default='/tmp', help="log path ", type=str)


class CompileServer:
    def __init__(self, configs):
        print("config compile server")
        print(configs)
        print(options.port)
        print(options.log_path)

    def init_compile_server(self):
        print("init compile server")
        tornado.options.parse_command_line()
        app = tornado.web.Application(handlers=[
            (r"/help/", HelpHandler),
            (r"/ping/", HealthHandler),
            (r"/upfile/", UpfileHandler),      # discard
            (r"/downfile/", DownfileHandler),  # discard
            (r"/compile/", CompileHandler),
            (r"/compile_status/", StatusHandler),
            (r"/compile_result/", ResultHandler),

            (r"/compile_online/", CompileOnlineHandler),
            (r"/compile_online_status/", StatusOnlineHandler),
            (r"/compile_online_result/", ResultOnlineHandler),
            (r"/", HelpHandler),
        ])
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)

    def run(self):
        print("run compile server")
        tornado.ioloop.IOLoop.instance().start()
