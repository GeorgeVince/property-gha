FROM python:3.10-alpine
ADD . /app
WORKDIR /app

RUN apk add gcc gfortran build-base wget freetype-dev libpng-dev openblas-dev jpeg-dev zlib-dev libffi-dev

RUN pip install --target=/app -r requirements.txt

WORKDIR /app
ENV PYTHONPATH /app
CMD "python" "main.py"