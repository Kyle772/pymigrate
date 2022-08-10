FROM python:3
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]