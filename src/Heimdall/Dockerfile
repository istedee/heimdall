FROM python:3.8-slim-buster

WORKDIR /backend

COPY ./backend backend/
COPY ./config /backend/config
COPY ./heimdall /backend/heimdall
COPY ./results /backend/results

ENV FLASK_APP=backend
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=True

COPY /backend/requirements.txt ./
COPY /backend/start_flask.sh ./
COPY requirements.txt /backend/heimdall/
COPY start_scanner.sh /backend/

RUN apt-get update
RUN apt-get install -y procps
RUN apt-get install -y libcurl4-gnutls-dev
RUN apt-get install -y librtmp-dev
RUN apt-get install -y nmap

RUN pip3 install -r requirements.txt

CMD [ "./start_flask.sh" ]