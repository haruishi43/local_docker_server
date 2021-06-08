_base_ = ["./_base_/default.py"]
server = dict(
    users=[
        "user1",
    ],
)
user1 = dict(
    user1_container1=dict(  # container name
        container_id=0,
        image_name="alpinetest",  # image name
        target_user_name="ubuntu",  # user for the os
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
    ),
)
