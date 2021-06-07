#!/usr/bin/env python3

import os
import time

import docker


global_client = docker.from_env()


def test_flow():

    client = docker.from_env()

    tag = "alpinetest_failure"
    image_root = "./tests/images/"
    dockerfile = f"{tag}.dockerfile"
    assert os.path.exists(image_root)

    img = build_image(
        root=image_root,
        dockerfile=dockerfile,
        tag=tag,
    )

    # img, _ = client.images.build(
    #     path=image_root,
    #     dockerfile=dockerfile,
    #     tag="alpinetest",
    #     rm=True,
    # )
    print(img)
    print(img.attrs)
    print(img.id)
    print(img.tags)

    container_name = "alpinetest_containerA"
    ret = client.containers.run(
        image="alpinetest",
        # command="/bin/ash -c 'uname -r'",
        name=container_name,
        # tty=True,  # `-i`
        # stdin_open=True,  # `-t`
        detach=True,  # `-d`
        publish_all_ports=True,  # `-P`
        privileged=True,  # `--privileged`
    )
    print(ret)

    container = client.containers.get(container_name)
    print(container.status)
    container.stop()

    time.sleep(0)
    container.reload()  # you have to call `reload()` since it's cached
    print(container.status)
    container.remove()

    client.images.remove(img.id)
