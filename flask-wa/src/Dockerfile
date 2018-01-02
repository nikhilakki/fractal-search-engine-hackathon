FROM python:3
ADD . /src
WORKDIR /src
EXPOSE 5000
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "server.py"]

