FROM alpine:3.12.1

COPY . /tweet-bot

RUN apk add python3 curl gcc build-base python3-dev

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

RUN python3 get-pip.py

RUN pip install --upgrade pip

WORKDIR /tweet-bot

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh

ENTRYPOINT ./entrypoint.sh