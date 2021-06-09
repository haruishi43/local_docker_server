image_path = "./images"
labels = dict(
    manager="dhole",
)
server = dict(
    ip="192.168.1.18",
    port_id=4,
    ports={
        "{port_id}00{container_id}/tcp": 22,
        "{port_id}88{container_id}/tcp": 8888,
    },
    volumes={
        "{host_home}/tmp/{user}": {
            "bind": "{home}/tmp",
            "mode": "rw",
        },
    }
)
