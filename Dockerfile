FROM ubuntu:latest

WORKDIR /app
ADD . /app
RUN set -xe \
    && apt-get update -y \
    && apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt                                                                        

EXPOSE 5000

ENTRYPOINT  ["python3"]

CMD ["app.py"]
