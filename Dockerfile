FROM python:3.13.0a4-alpine3.18 AS builder

RUN apk add --no-cache cargo gcc build-base
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

FROM python:3.13.0a4-alpine3.18

LABEL org.label-schema.schema-version = "1.0"
LABEL org.label-schema.name = "NotifyMe"
LABEL org.label-schema.vendor = "nagaev.sv@gmail.com"
LABEL org.label-schema.vcs-url = "https://github.com/s-nagaev/notifyme"

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app
COPY . .
RUN addgroup -S notifyme && adduser -S notifyme -G notifyme
USER notifyme

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=30s CMD python scripts/healthcheck.py || exit 1
ENTRYPOINT []
CMD python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
