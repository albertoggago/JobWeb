FROM jenkins/jenkins

USER root
RUN echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
RUN apt-get -y update && apt-get install -y python-pip && apt-get install -y mongodb-org

RUN cd /home && mkdir alberto && cd alberto

RUN cd /home/alberto && git clone https://github.com/albertoggago/JobWeb

RUN pip install -r /home/alberto/JobWeb/docker/requirements.txt

RUN mkdir /home/alberto/JobWeb/test/config && mkdir /home/alberto/JobWeb/pythonBatch/config
RUN cp /home/alberto/JobWeb/docker/config.json /home/alberto/JobWeb/pythonBatch/config/configOk.json
RUN cp /home/alberto/JobWeb/docker/config.json /home/alberto/JobWeb/pythonBatch/test/config/configOk.json
