FROM alpine:latest

RUN apk add --no-cache python3
RUN pip3 install mitmproxy

COPY 4lapy_phone_parser.py /app/4lapy_phone_parser.py

EXPOSE 8080

CMD ["mitmdump", "-q", "-s", "4lapy_phone_parser.py"]







