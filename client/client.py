import grpc
import time
import os
import json
import data_transfer_pb2
import data_transfer_pb2_grpc
from prometheus_client import start_http_server, Gauge, Counter

# Метрики Prometheus
TRANSFER_DURATION = Gauge('grpc_transfer_duration_seconds', 'Duration of gRPC transfer')
TRANSFER_SPEED = Gauge('grpc_transfer_speed_mbps', 'Speed of gRPC transfer in Mbps')
BYTES_TRANSFERRED = Counter('grpc_bytes_transferred_total', 'Total bytes transferred')


def run():
    # Запускаем HTTP сервер для метрик Prometheus
    start_http_server(8000)

    results = []
    # Создаем данные размером 24 МБ
    data = os.urandom(24 * 1024 * 1024)

    # Увеличиваем максимальный размер сообщения до 50MB
    channel = grpc.insecure_channel(
        'server:50051',
        options=[
            ('grpc.max_send_message_length', 50 * 1024 * 1024),
            ('grpc.max_receive_message_length', 50 * 1024 * 1024)
        ]
    )
    stub = data_transfer_pb2_grpc.DataTransferStub(channel)

    while True:  # Бесконечный цикл для непрерывного тестирования
        start_time = time.time()
        timestamp = int(start_time * 1000)

        response = stub.SendData(
            data_transfer_pb2.DataRequest(
                data=data,
                timestamp=timestamp
            )
        )

        end_time = time.time()
        duration = end_time - start_time
        speed_mbps = (len(data) * 8) / (duration * 1000000)

        # Обновляем метрики
        TRANSFER_DURATION.set(duration)
        TRANSFER_SPEED.set(speed_mbps)
        BYTES_TRANSFERRED.inc(len(data))

        results.append({
            'test_number': len(results) + 1,
            'duration': duration,
            'data_size': len(data),
            'speed_mbps': speed_mbps
        })

        # Сохраняем результаты после каждого теста
        with open('/shared/results.json', 'w') as f:
            json.dump(results, f)

        time.sleep(1)  # Пауза между тестами


if __name__ == '__main__':
    time.sleep(5)  # Ждем, пока сервер запустится
    run()
