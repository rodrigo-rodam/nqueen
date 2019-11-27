FROM python:3.6

LABEL maintainer="Rodrigo Rodam"

ADD . /challenge
WORKDIR /challenge

RUN pip install --upgrade pip
RUN pip install -r /challenge/requirements.txt

EXPOSE 8080

ENV PYTHONPATH "${PYTHONPATH}:.:/challenge"

ENTRYPOINT ["python3"]
CMD ["app/api.py"]