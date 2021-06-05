#!/usr/bin/env python3

CONFIG = dict(
    successfulServer=dict(
        userA=dict(
            userA_containerA=dict(
                container_id=0,
                image_name="AlpineTestA",
                extra_ports=[1, 88, 89],
            ),
            userA_containerB=dict(
                container_id=10,
                image_name="alpine",
                extra_ports=[88, 89],
            ),
        ),
        userB=dict(
            userB_containerA=dict(
                container_id=1,
                image_name="alpine",
                extra_ports=[1, 88, 89],
            ),
            userB_containerB=dict(
                container_id=11,
                image_name="alpine",
                extra_ports=[88, 89],
            ),
        ),
    ),
    failureServer=dict(
        userA=dict(
            userA_containerA=dict(
                container_id=0,
                image_name="alpine",
                extra_ports=[1, 88, 89],
            ),
            userA_containerB=dict(
                container_id=10,
                image_name="alpine",
                extra_ports=[88, 89],
            ),
        ),
        userB=dict(
            userB_containerA=dict(
                container_id=0,
                image_name="alpine",
                extra_ports=[1, 88, 89],
            ),
            userB_containerB=dict(
                container_id=10,
                image_name="alpine",
                extra_ports=[88, 89],
            ),
        ),
    )
)
