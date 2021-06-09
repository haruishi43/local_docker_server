#!/usr/bin/env python3

from copy import deepcopy
from typing import List

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
        image_name: str,
        image_cfg: ConfigDict,
    ) -> None:
        self.image_name = image_name
        self.image_path = image_cfg.image_name
        self.image_labels = image_cfg.labels

    def build(self):
        pass

    def delete(self):
        pass


class ImageCollection:
    def __init__(
        self,
        images: List[str],
        cfg: Config,
    ) -> None:
        self.images = images

        default_image_path = deepcopy(cfg.image_path)
        default_labels = deepcopy(cfg.labels)
        image_cfg = {}
        for image in self.images:
            if image not in list(cfg.keys()):
                cfg[image] = {
                    "image_path": default_image_path,
                    "labels": default_labels,
                }
            else:
                keys = list(cfg[image].keys())
                # image_path
                if "image_path" not in keys:
                    cfg[image].image_path = default_image_path
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
                image_name=k,
                image_cfg=v,
            )
