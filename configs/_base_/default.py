image_path = "./images"
labels = dict(
    manager="dhole",
)
server = dict(
    ip="192.168.1.18",
    port_id=4,
    ports=[
        ("{port_id}00{container_id}", 22, "tcp"),
        ("{port_id}88{container_id}", 8888, "tcp"),
    ],
    volumes=[
        ("{host_home}/tmp/{user}", "{home}/tmp", "rw"),
    ],
)
