server = dict(
    ip="localhost",
    port_id=9,  # first number of the 5 number port
    volumes={
        "{host_curdir}/tests/data": {
            "bind": "{home}/data",
            "mode": "ro",
        },
    },
    ports={
        "{port_id}00{container_id}/tcp": 22,
    },
    labels={
        "manager": "dhole",
    },
)
