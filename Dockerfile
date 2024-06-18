FROM python:3.11

WORKDIR .

ADD . .
RUN pip install -r ./requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "./api/app.py"]