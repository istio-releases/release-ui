proto_library(
    name = "releases_proto",
    srcs = [ "releases.proto" ],
)

py_proto_library(
    name = "releases_py_pb2",
    api_version = 2,
    deps = [":releases_proto"],
)

py_library(
    name = "releases_py",
    srcs = ["releases.py"],
    deps = [":releases_py_pb2"],
)
