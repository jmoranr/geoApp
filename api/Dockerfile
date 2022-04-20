# FROM python:latest
# RUN mkdir /usr/src/app/
# COPY . /usr/src/app/
# WORKDIR /usr/src/app/
# RUN pip install psycopg2-binary
# RUN pip install flask
# EXPOSE 5000
# CMD ["python", "app.py"]

FROM python:3.6.1
RUN groupadd flaskgroup && useradd -m -g flaskgroup -s /bin/bash flask
RUN mkdir /usr/src/app/
WORKDIR /usr/src/app/
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app/
RUN chown -R flask:flaskgroup /usr/src
USER flask
EXPOSE 5000
CMD ["python", "app.py"]