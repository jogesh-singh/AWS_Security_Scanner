FROM python:3.10-alpine

COPY ./requirements.txt /app/requirements.txt

RUN apk add build-base make

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD ["app.py" ]