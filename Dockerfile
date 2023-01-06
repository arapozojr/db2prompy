FROM python:3.10.9

ENV DB_HOST 127.0.0.1
ENV DB_PORT 50000
ENV DB_NAME sample
ENV DB_USER db2inst1
ENV DB_PROGNAME DB2PROMPY

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD python3 app.py -H ${DB_HOST} -p ${DB_PORT} -d ${DB_NAME} -u ${DB_USER} -n ${DB_PROGNAME}
