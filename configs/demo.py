_base_ = ['./_base_/default.py']
server = dict(
    users=[
        "user1",
    ],
)
user1 = dict(
    user1_u18=dict(
        container_id=0,
        image_name="u18",
        target_user_name="ubuntu",  # user for the os
        ports={
            "{port_id}89{container_id}/tcp": 8889,
        },
    ),
    user1_alpine=dict(
        container_id=1,
        image_name="alpine",
        target_user_name="alpine",
    )
)
