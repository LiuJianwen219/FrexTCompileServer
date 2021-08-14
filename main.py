from server.server import CompileServer

if __name__=="__main__":
    compileServer = CompileServer({
        "user": "ljw",
    })
    compileServer.init_compile_server()
    compileServer.run()
