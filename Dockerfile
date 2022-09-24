# Base Image
FROM python:3.10

# create and set working directory
RUN mkdir /app
WORKDIR /app

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# install environment dependencies
COPY ./requirements.txt /app/requirements.txt
COPY ./requirements-dev.txt /app/requirements-dev.txt
RUN pip install --upgrade pip
ARG REQUIREMENTS=requirements.txt
RUN pip install -r ${REQUIREMENTS}

# Add current directory code to working directory
ADD . /app

EXPOSE 8000
CMD ["gunicorn", "app.asgi:application", "-k", "uvicorn.workers.UvicornWorker"]
