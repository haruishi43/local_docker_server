server = dict(
    volumes=[],
    users=[
        "user1",
    ],
)
user1 = dict(
    user1_container1=dict(  # container name
        container_id=0,
        image_name="alpinetest",  # image name
        extra_ports=[1, 88, 89],
    ),
)
