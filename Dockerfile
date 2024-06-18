FROM python:3.11

WORKDIR .

RUN pip install -r ./requirement.txt

EXPOSE 3000

ENTRYPOINT ["./api/start.py"]