FROM python:3.12

# set environment variables
ENV PYTHONBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME

# install production dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . ./

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 "main:create_app()"
