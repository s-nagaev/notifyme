FROM python:3.9-alpine3.16 AS builder

RUN apk add --no-cache cargo gcc build-base
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

FROM python:3.9-alpine3.16

LABEL org.label-schema.schema-version = "1.0"
LABEL org.label-schema.name = "NotifyMe"
LABEL org.label-schema.vendor = "nagaev.sv@gmail.com"
LABEL org.label-schema.vcs-url = "https://github.com/s-nagaev/notifyme"

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

WORKDIR /app
COPY . .
RUN addgroup -S notifyme && adduser -S notifyme -G notifyme
USER notifyme

EXPOSE 8000

HEALTHCHECK --interval=20s --timeout=3s --start-period=30s CMD python scripts/healthcheck.py || exit 1
ENTRYPOINT []
CMD python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
