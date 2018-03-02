FROM jenkins/jenkins

USER root

RUN apt-get -y update && apt-get install -y python-pip

#Packages prev to Chrome + ChromeDriver
RUN apt-get install -y xvfb xserver-xephyr vnc4server apt-transport-https

#Instalation Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && sh -c 'echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && apt-get -y update && apt-get install -y google-chrome-stable

#Instalation CromeDriver
RUN wget https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip && unzip chromedriver_linux64.zip && mv -f chromedriver /usr/local/bin/chromedriver && chown root:root /usr/local/bin/chromedriver && chmod 0755 /usr/local/bin/chromedriver

#install git
RUN cd /home && mkdir alberto
COPY requirements.txt /home/alberto/requirements.txt 

#install python requeriments
RUN pip install -r /home/alberto/requirements.txt