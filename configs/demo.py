_base_ = ['./_base_/default.py']
server = dict(
    volumes=[],
    users=[],
)
user1 = dict(
    u18_user1=dict(
        container_id=0,
        image_name="u18",
        extra_ports=[88, 89],
    )
)
