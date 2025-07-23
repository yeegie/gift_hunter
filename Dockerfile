FROM python:3.13-alpine

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir .


CMD ["gift_hunter_bot"]