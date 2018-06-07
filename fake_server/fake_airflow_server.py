from concurrent import futures
import time
import grpc
import config_pb2
import config_pb2_grpc
from fake_data import releases


_ONE_DAY_IN_SECONDS = 60 * 60 * 24



# for debugging
print config_pb2.SingleRelease()

def FindRelease(self, id, context):
    for release in releases:
        for release in releases:
            single_release = config_pb2.SingleRelease()
            single_release.id.id = release['id']
            print 'Trigger3'
            single_release.labels.extend(release['labels'])
            single_release.ref = release['ref']
            single_release.state = release['state']
            single_release.stage = release['stage']
            single_release.started = release['started']
            single_release.last_modified = release['last_modified']
            single_release.artifacts_link = release['artifacts_link']
            single_release.release_url = release['release_url']
            # for task in release['ReleaseTask']:
            #     single_release.ReleaseTask.task_name = task['task_name']
            #     single_release.ReleaseTask.start_time = task['start_time']
            #     single_release.ReleaseTask.end_time = task['end_time']
            #     single_release.ReleaseTask.status = task['status']
            #     single_release.ReleaseTask.error_message = task['error_message']
            #     single_release.ReleaseTask.log_link = task['log_link']
            print release
            if release['id'] == id:
                print 'Trigger1'
                print release
                return release

class Release(config_pb2_grpc.ReleaseServicer):
    def GetRelease(self, request, context):
        print request
        print 'Trigger2'
        return config_pb2.GetReleaseResponse(release=FindRelease(self, request.id, context))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    config_pb2_grpc.add_ReleaseServicer_to_server(Release(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
