_base_ = ['./_base_/default.py']
server = dict(
    name="demo",
    users=[
        "user1",
        "user2",
    ],
)
user1 = dict(
    user1_u18=dict(
        container_id=0,
        image_name="u18",
        target_user_name="ubuntu",  # user for the os
        ports=[
            ("{port_id}89{container_id}", 8889, "tcp"),
        ],
        shm_size="32G",
    ),
    user1_u18c111=dict(
        container_id=1,
        image_name="u18c111",
        target_user_name="ubuntu",
        ports=[
            ("{port_id}89{container_id}", 8889, "tcp"),
        ],
        shm_size="32G",
        gpus="all",
    )
)
user2 = dict(
    user2_u18=dict(
        container_id=2,
        image_name="u18",
        target_user_name="ubuntu",  # user for the os
        ports=[
            ("{port_id}89{container_id}", 8889, "tcp"),
        ],
        shm_size="32G",
    ),
    user2_u18c111=dict(
        container_id=3,
        image_name="u18c111",
        target_user_name="ubuntu",
        ports=[
            ("{port_id}89{container_id}", 8889, "tcp"),
        ],
        shm_size="32G",
        gpus="all",
    )
)
