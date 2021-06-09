#!/usr/bin/env python3

from copy import deepcopy
from typing import List, Union

from .config import Config, ConfigDict
from .env import CLIENT
from .errors import APIError, BuildError
from .logger import logger


def build_image(
    root: str,
    dockerfile: str,
    tag: str,
):
    try:
        logger.debug(f"building image {tag}")
        img, _ = CLIENT.images.build(
            path=root,
            dockerfile=dockerfile,
            tag=tag,
            rm=True,
        )
    except BuildError as e:
        logger.error(e)
        raise e
    except APIError as e:
        logger.error(e)
        raise e

    return img


class Image:
    def __init__(
        self,
        name: str,
        image_cfg: ConfigDict,
    ) -> None:
        self.name = name
        self.path = image_cfg.path
        self.labels = image_cfg.labels

    def __repr__(self) -> str:
        return (
            f"Image: {self.name}\n"
            f"\tpath: {self.path}\n"
            f"\tlabels: {self.labels}\n"
        )

    def build(self):
        logger.info(f"Building {self.name}...")
        image = build_image(
            root=self.path,
            dockerfile=f"{self.name}.dockerfile",
            tag=self.labels,
        )
        return image

    def delete(self):
        pass


class ImageCollection:
    def __init__(
        self,
        images: List[str],
        cfg: Config,
    ) -> None:
        if len(set(images)) < len(images):
            logger.warning("WARN: there are duplicate images")
            images = list(set(images))

        self.names = images

        default_path = deepcopy(cfg.image_path)
        default_labels = deepcopy(cfg.labels)
        image_cfg = {}
        for image in images:
            if image not in cfg.keys():
                cfg[image] = {
                    "name": image,
                    "path": default_path,
                    "labels": default_labels,
                }
            else:
                keys = cfg[image].keys()
                # name
                if "name" not in keys:
                    cfg[image].name = image
                # path
                if "path" not in keys:
                    cfg[image].path = default_path
                # labels
                labels = {}
                labels.update(default_labels)
                if "labels" in keys:
                    labels.update(cfg[image].labels)
                cfg[image].labels = labels

            image_cfg[image] = cfg[image]

        self.image_cfg = ConfigDict(image_cfg)

        self.images = {}
        for k, v in self.image_cfg.items():
            self.images[k] = Image(
                name=k,
                image_cfg=v,
            )

    def __len__(self) -> int:
        return len(self.names)

    def __getitem__(self, i: Union[int, str]) -> Image:
        if isinstance(i, int):
            name = self.names[i]
        elif isinstance(i, str):
            name = i
        assert name in self.images.keys(), \
            f"ERR: {name} is not a valid image name"
        return self.images[name]
