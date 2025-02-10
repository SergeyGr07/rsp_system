import grpc
from concurrent import futures
import time
import data_transfer_pb2
import data_transfer_pb2_grpc


class DataTransferServicer(data_transfer_pb2_grpc.DataTransferServicer):
    def SendData(self, request, context):
        received_timestamp = request.timestamp
        current_timestamp = int(time.time() * 1000)

        return data_transfer_pb2.DataResponse(
            success=True,
            timestamp=current_timestamp
        )


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_send_message_length', 50 * 1024 * 1024),
            ('grpc.max_receive_message_length', 50 * 1024 * 1024)
        ]
    )
    data_transfer_pb2_grpc.add_DataTransferServicer_to_server(
        DataTransferServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
