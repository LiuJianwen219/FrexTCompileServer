FROM centos/python-36-centos7

COPY requirements.txt /tmp
RUN ["pip", "install", "-r", "/tmp/requirements.txt"]

# create workspace
WORKDIR /tmp

# copy source
COPY ./bin/unzip /bin
COPY ./ /tmp

RUN ["sed", "-i", "s/\r//g", "scripts/compile.sh"]
RUN ["sed", "-i", "s/\r//g", "scripts/compile_online.sh"]
## make environment
#RUN ["pip", "install", "-r", "requirements.txt"]
