# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
# Debian GNU/Linux 10 (buster)

ENV DEBIAN_FRONTEND="noninteractive" 
ENV TZ="America/Bahia"
ENV OPENSSL_CONF=/etc/ssl/

RUN apt-get update && apt-get install -y \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 \
    curl unzip wget \
    xvfb

# install geckodriver and firefox

RUN GECKODRIVER_VERSION=`curl --silent "https://api.github.com/repos/mozilla/geckodriver/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/'` && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
    apt-get purge firefox && \
    wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
    tar -xjvf $FIREFOX_SETUP -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/bin/firefox && \
    rm $FIREFOX_SETUP

# Install PHP and chrome to run RPA

# RUN apt-get update && apt-get -y upgrade && \
#     apt-get -y install php php-common

# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
#     apt-get install -y /google-chrome-stable_current_amd64.deb

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=main.py
ENV FLASK_ENV=development

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]