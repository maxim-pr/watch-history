FROM python:3.10

WORKDIR /opt/app/

COPY watched/ ./watched/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY config.ini .
CMD ["python", "-m", "watched"]
