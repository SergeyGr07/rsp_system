FROM python:3.9-slim

WORKDIR /app

COPY visualization/visualize.py .

RUN pip install matplotlib

CMD ["python", "visualize.py"] 