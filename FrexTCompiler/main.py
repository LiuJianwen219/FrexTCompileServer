#!/usr/bin/python3

import sys, getopt
from compile import constants as const
from compile import compile


def main(argv):
    values = {}
    try:
        opts, args = getopt.getopt(argv, "u:t:s:c:n:l:f:", [
            "userId=", "testId=",
            "submitId=", "topic=",
            "topModuleName=", "tcl=",
            "fileServerUrl=",
        ])
    except getopt.GetoptError:
        print('we need help.')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('we need help.')
            sys.exit()
        elif opt in ("-u", "--userId"):
            values[const.c_userId] = arg
        elif opt in ("-t", "--testId"):
            values[const.c_testId] = arg
        elif opt in ("-s", "--submitId"):
            values[const.c_submitId] = arg
        elif opt in ("-c", "--topic"):
            values[const.c_topic] = arg
        elif opt in ("-n", "--topModuleName"):
            values[const.c_topModuleName] = arg
        elif opt in ("-l", "--tcl"):
            values[const.c_tcl] = arg
        elif opt in ("-f", "--fileServerUrl"):
            values[const.c_file_server_url] = arg

    compile.compile_project(values)


# python main.py -u uljw -t t123 -s s123 -c mod60 -n topMod60 -l mod60 -f http://frext-file-svc:8010/
if __name__ == "__main__":
    main(sys.argv[1:])
