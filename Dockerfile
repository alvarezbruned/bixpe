FROM python:3.6-slim
RUN apt-get update
RUN apt-get install -y firefox
RUN pip install selenium
ADD https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz /usr/local/bin/geckodriver-v0.24.0-linux64.tar.gz
WORKDIR /usr/local/bin
RUN tar -xvzf /usr/local/bin/geckodriver-v0.24.0-linux64.tar.gz
WORKDIR /root
RUN ls -lsa /usr/local/bin
RUN rm /usr/local/bin/geckodriver-v0.24.0-linux64.tar.gz

COPY bixpe.py /root/bixpe.py

ENTRYPOINT python3 /root/bixpe.py
