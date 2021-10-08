import logging
import os
import signal
import socket

from server.server import CompileServer

#
# def onSigChld(signo, frame):
#     print("onSigChld")
#
#
# def onSigInt(signo, frame):
#     print("onSigInt")
#
#
# def onSigTerm(signo, frame):
#     print("onSigTerm")


# get path
# cur_dir = os.path.abspath(__file__).rsplit("/", 1)[0]
rootPath = "/data/FrexT"
log_path = os.path.join(rootPath, "FrexTCompileServer_" + socket.gethostname() + ".log")

# encoding='utf-8'
logging.basicConfig(filename=log_path, level=logging.DEBUG,
                    filemode='w', format='%(levelname)s:%(asctime)s:%(message)s',
                    datefmt='%Y-%d-%m %H:%M:%S')


if __name__ == "__main__":
    # # 子进程退出后向父进程发送的信号
    # signal.signal(signal.SIGCHLD, onSigChld)
    #
    # # 主进程退出信号
    # signal.signal(signal.SIGINT, onSigInt)
    # signal.signal(signal.SIGTERM, onSigTerm)

    compileServer = CompileServer({
        "user": "ljw",
    })
    compileServer.init_compile_server()
    compileServer.run()
