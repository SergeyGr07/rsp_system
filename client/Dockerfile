FROM python:3.9-slim

WORKDIR /app

COPY proto/data_transfer.proto .
COPY client/client.py .

RUN pip install grpcio grpcio-tools prometheus-client
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. data_transfer.proto

CMD ["python", "client.py"] 