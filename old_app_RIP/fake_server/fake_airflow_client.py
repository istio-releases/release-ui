#from __future__ import print_funtion
import grpc
import config_pb2_grpc
import config_pb2
test = config_pb2.GetReleaseRequest()
test.id = '5649681819846168'
def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = config_pb2_grpc.ReleaseStub(channel)
    response = stub.GetRelease(config_pb2.GetReleaseRequest(test))
    print(response)

if __name__ == '__main__':
    run()
