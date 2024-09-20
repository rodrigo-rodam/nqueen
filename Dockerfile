FROM python:3.6

LABEL maintainer="Rodrigo Rodam"

ADD . /nqueen
WORKDIR /nqueen

RUN pip install --upgrade pip
RUN pip install -r /nqueen/requirements.txt

EXPOSE 8080

ENV PYTHONPATH "${PYTHONPATH}:.:/nqueen"

ENTRYPOINT ["python3"]
CMD ["app/api.py"]