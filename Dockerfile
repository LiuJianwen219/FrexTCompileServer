FROM centos/python-36-centos7

WORKDIR /FrexT

COPY requirements.txt /FrexT/requirements.txt
RUN ["pip", "install", "-r", "requirements.txt"]

COPY ./bin/unzip /bin
COPY ./ /FrexT/FrextCompileServer/

# expose port
EXPOSE 8012/tcp

ENTRYPOINT ["python", "FrextCompileServer/main.py"]
