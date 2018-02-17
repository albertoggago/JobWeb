FROM jenkins/jenkins

USER root

RUN apt-get -y update  
RUN apt-get install -y python-pip

RUN cd /home && mkdir alberto && cd alberto

RUN cd /home/alberto && git clone https://github.com/albertoggago/JobWeb

RUN pip install -r /home/alberto/JobWeb/docker/requirements.txt

RUN mkdir /home/alberto/JobWeb/pythonBatch/test/config && mkdir /home/alberto/JobWeb/pythonBatch/config
COPY config.json /home/alberto/JobWeb/pythonBatch/config/config.json
COPY config.json /home/alberto/JobWeb/pythonBatch/test/config/configOk.json
