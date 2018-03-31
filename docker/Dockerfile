FROM jenkins/jenkins

USER root

RUN apt-get -y update && apt-get install -y python-pip

#install git
RUN cd /home && mkdir alberto
COPY requirements.txt /home/alberto/requirements.txt 

#install python requeriments
RUN pip install -r /home/alberto/requirements.txt

#add files of testing
COPY config.json /home/alberto
COPY configMailAccessError.json /home/alberto
COPY configMongoDBError.json /home/alberto