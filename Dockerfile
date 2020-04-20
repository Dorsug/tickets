# -- Build image --
FROM python:3.8-alpine3.11 AS builder
RUN apk add --no-cache linux-headers g++ zlib-dev jpeg-dev

COPY requirements.txt .
RUN pip3 wheel --wheel-dir=/root/wheels -r requirements.txt


# -- Prod image --
FROM python:3.8-alpine3.11 AS runner
EXPOSE 80

WORKDIR /tickets
RUN apk add --no-cache jpeg-dev
COPY --from=builder /root/wheels /root/wheels
COPY requirements.txt .
RUN pip install \
      --no-index \
      --find-links=/root/wheels \
      -r requirements.txt

COPY . .

ENV FLASK_APP tickets
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0", "--port=80"]
