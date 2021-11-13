import json
import os
import subprocess
from compile import utils
from compile import constants as const
from compile import situation


def compile_project(values):
    print("Compile with values: ", values)
    fh = utils.FileRequest(values)
    reporter = situation.SituationHandler(values)

    if fh.get_tcl() == const.request_failed:
        reporter.post_result(const.request_failed, "获取tcl失败", "Failed: get tcl file error.\n")
        return
    else:
        reporter.post_status(const.request_success, "获取tcl成功", "Success: get tcl file complete.\n")

    if fh.get_questions() == const.request_failed:
        reporter.post_result(const.request_failed, "获取zip失败", "Failed: get zip file error.\n")
        return
    else:
        reporter.post_status(const.request_success, "获取zip成功", "Success: get zip file complete.\n")

    if fh.get_tests() == const.request_failed:
        reporter.post_result(const.request_failed, "获取v失败", "Failed: get v file error.\n")
        return
    else:
        reporter.post_status(const.request_success, "获取v成功", "Success: get v file complete.\n")

    res = subprocess.call([
        "/bin/bash",
        const.compileScript,  # 0
        os.path.join(const.work_dir, values[const.c_topic] + const.questions_suffix),  # 1
        os.path.join(const.work_dir, values[const.c_topic]),  # 2
        const.vivado,  # vivado.exe dir     # 3
        os.path.join(const.work_dir, values[const.c_tcl] + const.tcls_suffix),  # 4 main.tcl
        const.FPGAVersion,  # 5 FPGAVersion
        os.path.join(const.work_dir),  # 6 workDir
        values[const.c_topModuleName],  # 7 topModuleName
        const.compileThread,  # 8 threads
    ], shell=False)
    print("Compile result: ", res)

    if fh.post_log() == const.request_failed:
        reporter.post_result(const.request_failed, "提交log失败", "Failed: put log file error.\n")
        return
    else:
        reporter.post_status(const.request_success, "提交log成功", "Success: put log file complete.\n")

    if fh.post_rpt() == const.request_failed:
        reporter.post_result(const.request_failed, "编译失败rpt", "Failed: put rpt file error.\n")
        return
    else:
        reporter.post_status(const.request_success, "提交rpt成功", "Success: put rpt file complete.\n")

    if fh.post_project() == const.request_failed:
        reporter.post_result(const.request_failed, "编译失败project", "Failed: put project file error.\n")
        return
    else:
        reporter.post_status(const.request_success, "提交project成功", "Success: put project file complete.\n")

    if fh.post_bit() == const.request_failed:
        reporter.post_result(const.request_failed, "编译失败bit", "Failed: compile bit file error.\n")
        return
    else:
        reporter.post_result(const.request_success, "编译成功", "Success: compile bit file complete.\n")


def compile_online_project(values):
    print("Compile online with values: ", values)
    fh = utils.FileOnlineRequest(values)
    reporter = situation.SituationOnlineHandler(values)

    if fh.get_tcl() == const.request_failed:
        reporter.post_online_result(const.request_failed, "获取tcl失败", "Failed: get tcl file error.\n")
        return
    else:
        reporter.post_online_status(const.request_success, "获取tcl成功", "Success: get tcl file complete.\n")

    fileNames = json.loads(values[const.c_fileNames])
    print(values[const.c_fileNames])
    for fileName in fileNames:
        if fh.get_src(fileName) == const.request_failed:
            reporter.post_online_result(const.request_failed, "获取src失败", "Failed: get {0} file error.\n".format(fileName))
            return
    reporter.post_online_status(const.request_success, "获取src成功", "Success: get zip file complete.\n")

    res = subprocess.call([
        "/bin/bash",
        const.compileOnlineScript,  # 0
        os.path.join(const.work_dir),  # 1 not use
        os.path.join(const.work_dir),  # 2 not use
        const.vivado,  # vivado.exe dir     # 3
        os.path.join(const.work_dir, values[const.c_tcl] + const.tcls_suffix),  # 4 main_online.tcl
        const.FPGAVersion,  # 5 FPGAVersion
        os.path.join(const.work_dir),  # 6 workDir
        values[const.c_topModuleName],  # 7 topModuleName
        const.compileThread,  # 8 threads
    ], shell=False)
    print("Compile result: ", res)

    if fh.post_online_log() == const.request_failed:
        reporter.post_online_result(const.request_failed, "提交log失败", "Failed: put log file error.\n")
        return
    else:
        reporter.post_online_status(const.request_success, "提交log成功", "Success: put log file complete.\n")

    if fh.post_online_rpt() == const.request_failed:
        reporter.post_online_result(const.request_failed, "编译失败rpt", "Failed: put rpt file error.\n")
        return
    else:
        reporter.post_online_status(const.request_success, "提交rpt成功", "Success: put rpt file complete.\n")

    if fh.post_online_project() == const.request_failed:
        reporter.post_online_result(const.request_failed, "编译失败project", "Failed: put project file error.\n")
        return
    else:
        reporter.post_online_status(const.request_success, "提交project成功", "Success: put project file complete.\n")

    if fh.post_online_bit() == const.request_failed:
        reporter.post_online_result(const.request_failed, "编译失败", "Failed: compile bit file error.\n")
        return
    else:
        reporter.post_online_result(const.request_success, "编译成功", "Success: compile bit file complete.\n")
