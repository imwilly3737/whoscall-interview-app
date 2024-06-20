FROM python:3.11

WORKDIR /service/
COPY requirements.txt /service/requirements.txt
RUN pip install -r /service/requirements.txt
COPY . /service/.
ENV PYTHONPATH="${PYTHONPATH}:/service"
EXPOSE 5000

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app.app:app", "--reload"]