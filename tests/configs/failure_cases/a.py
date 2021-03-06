image_path = "./tests/images",  # path to the dockerfiles
labels = dict(
    manager="dhole_test",
)
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
    users=[
        "testuser1",
    ],
)
testuser1 = dict(
    testuser1_alpinetest=dict(  # container name
        container_id=0,
        image_name="alpinetest",  # image name
        target_user_name="alpine",  # user for the os
        volumes={
            "{host_home}/tmp/{user}": {
                "bind": "{home}/tmp",
                "mode": "rw",
            },
        },
        ports={
            "{port_id}88{container_id}/tcp": 8888,
            "{port_id}89{container_id}/tcp": 8889,
        },
        shm_size="32G",
    ),
)
