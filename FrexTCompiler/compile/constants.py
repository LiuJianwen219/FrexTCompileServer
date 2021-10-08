# -----------------------
# sys config

work_dir = "/tmp/project/"
request_success = "Success"
request_failed = "Failed"

# -----------------------
# for request compile files
tcls_API = "tcls"
tcls_suffix = ".tcl"

questions_API = "questions"
questions_suffix = ".zip"

tests_API = "tests"
tests_suffix = ".v"

bits_API = "bits"
bits_suffix = ".bit"

logs_API = "logs"
logs_suffix = ".log"

rpts_API = "rpts"
rpts_suffix = "_utilization_placed.rpt"

projects_API = "projects"
projects_suffix = ".zip"

c_userId = "userId"
c_testId = "testId"
c_submitId = "submitId"
c_topic = "topic"
c_topModuleName = "topModuleName"
c_tcl = "tcl"
c_file_server_url = "fileServerUrl"
c_thread_index = "threadIndex"

# -----------------------
# for return compile status/result
status_API = "compile_status"
result_API = "compile_result"

c_compile_server_url = "compileServerUrl"

# -----------------------
# other constants, maybe configurable in future
compileScript = "scripts/compile.sh"
vivado = "/tools/Xilinx/Vivado/2020.1/bin/vivado"
FPGAVersion = "xc7k160tffg676-2L"
compileThread = "4"

# -----------------------
# online addition
src_API = "experiment"

bits_online_API = "online_bits"
rpts_online_API = "online_rpts"
projects_online_API = "online_projects"
logs_online_API = "online_logs"

c_experimentType = "experimentType"
c_experimentId = "experimentId"
c_compileId = "compileId"
c_fileName = "fileName"
c_fileNames = "fileNames"

compileOnlineScript = "scripts/compile_online.sh"

status_online_API = "compile_online_status"
result_online_API = "compile_online_result"
