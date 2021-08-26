FROM centos/python-36-centos7

COPY requirements.txt /tmp
RUN ["pip", "install", "-r", "/tmp/requirements.txt"]

# create workspace
WORKDIR /FrexT

# copy source
COPY ./bin/unzip /bin
COPY ./ /FrexT

RUN ["sed", "-i", "s/\r//g", "compile/compile.sh"]

## make environment
#RUN ["pip", "install", "-r", "requirements.txt"]
