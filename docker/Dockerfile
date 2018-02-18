FROM jenkins/jenkins

USER root

RUN apt-get -y update  
RUN apt-get install -y python-pip
#RUN apt-get install -y chromium-chromedriver
RUN wget https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv -f chromedriver /usr/local/bin/chromedriver
RUN chown root:root /usr/local/bin/chromedriver
RUN chmod 0755 /usr/local/bin/chromedriver
RUN apt-get install xvfb xserver-xephyr vnc4server

RUN cd /home && mkdir alberto && cd alberto

RUN cd /home/alberto && git clone https://github.com/albertoggago/JobWeb

RUN pip install -r /home/alberto/JobWeb/docker/requirements.txt

RUN mkdir /home/alberto/JobWeb/pythonBatch/test/config && mkdir /home/alberto/JobWeb/pythonBatch/config
COPY config.json /home/alberto/JobWeb/pythonBatch/config/config.json
COPY config.json /home/alberto/JobWeb/pythonBatch/test/config/configOk.json
