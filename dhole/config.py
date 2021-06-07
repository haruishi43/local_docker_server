#!/usr/bin/env python3

"""
Manages Server Configs
"""

import ast
import os.path as osp
import platform
import re
import shutil
import sys
import tempfile
import warnings
from argparse import ArgumentParser
from collections import abc
from importlib import import_module

from addict import Dict

BASE_KEY = "_base_"
DELETE_KEY = "_delete_"
RESERVED_KEYS = ["filename", "text"]


class ConfigDict(Dict):
    def __missing__(self, name):
        raise KeyError(name)

    def __getattr__(self, name):
        try:
            value = super(ConfigDict, self).__getattr__(name)
        except KeyError:
            ex = AttributeError(
                f"'{self.__class__.__name__}' object has no "
                f"attribute '{name}'"
            )
        except Exception as e:
            ex = e
        else:
            return value
        raise ex


def add_args(parser, cfg, prefix=""):
    for k, v in cfg.items():
        if isinstance(v, str):
            parser.add_argument("--" + prefix + k)
        elif isinstance(v, int):
            parser.add_argument("--" + prefix + k, type=int)
        elif isinstance(v, float):
            parser.add_argument("--" + prefix + k, type=float)
        elif isinstance(v, bool):
            parser.add_argument("--" + prefix + k, action="store_true")
        elif isinstance(v, dict):
            add_args(parser, v, prefix + k + ".")
        elif isinstance(v, abc.Iterable):
            parser.add_argument("--" + prefix + k, type=type(v[0]), nargs="+")
        else:
            print(f"cannot parse key {prefix + k} of type {type(v)}")
    return parser


class Config:
    """A facility for config and config files.
    It supports common file formats as configs: python/json/yaml. The interface
    is the same as a dict object and also allows access config values as
    attributes.
    Example:
        >>> cfg = Config(dict(a=1, b=dict(b1=[0, 1])))
        >>> cfg.a
        1
        >>> cfg.b
        {'b1': [0, 1]}
        >>> cfg.b.b1
        [0, 1]
        >>> cfg = Config.fromfile('tests/data/config/a.py')
        >>> cfg.filename
        "/home/kchen/projects/mycv/tests/data/config/a.py"
        >>> cfg.item4
        'test'
        >>> cfg
        "Config [path: /home/kchen/projects/mycv/tests/data/config/a.py]: "
        "{'item1': [1, 2], 'item2': {'a': 0}, 'item3': True, 'item4': 'test'}"
    """

    @staticmethod
    def _validate_py_syntax(filename):
        with open(filename, "r", encoding="utf-8") as f:
            # Setting encoding explicitly to resolve coding issue on windows
            content = f.read()
        try:
            ast.parse(content)
        except SyntaxError as e:
            raise SyntaxError(
                "There are syntax errors in config " f"file {filename}: {e}"
            )

    @staticmethod
    def _substitute_predefined_vars(filename, temp_config_name):
        file_dirname = osp.dirname(filename)
        file_basename = osp.basename(filename)
        file_basename_no_extension = osp.splitext(file_basename)[0]
        file_extname = osp.splitext(filename)[1]
        support_templates = dict(
            fileDirname=file_dirname,
            fileBasename=file_basename,
            fileBasenameNoExtension=file_basename_no_extension,
            fileExtname=file_extname,
        )
        with open(filename, "r", encoding="utf-8") as f:
            # Setting encoding explicitly to resolve coding issue on windows
            config_file = f.read()
        for key, value in support_templates.items():
            regexp = r"\{\{\s*" + str(key) + r"\s*\}\}"
            value = value.replace("\\", "/")
            config_file = re.sub(regexp, value, config_file)
        with open(temp_config_name, "w") as tmp_config_file:
            tmp_config_file.write(config_file)

    @staticmethod
    def _file2dict(filename, use_predefined_variables=True):
        filename = osp.abspath(osp.expanduser(filename))
        assert osp.isfile(filename)
        fileExtname = osp.splitext(filename)[1]
        if fileExtname not in [".py", ".json", ".yaml", ".yml"]:
            raise IOError("Only py/yml/yaml/json type are supported now!")

        with tempfile.TemporaryDirectory() as temp_config_dir:
            temp_config_file = tempfile.NamedTemporaryFile(
                dir=temp_config_dir, suffix=fileExtname
            )
            if platform.system() == "Windows":
                temp_config_file.close()
            temp_config_name = osp.basename(temp_config_file.name)
            # Substitute predefined variables
            if use_predefined_variables:
                Config._substitute_predefined_vars(
                    filename, temp_config_file.name
                )
            else:
                shutil.copyfile(filename, temp_config_file.name)

            temp_module_name = osp.splitext(temp_config_name)[0]
            sys.path.insert(0, temp_config_dir)
            Config._validate_py_syntax(filename)
            mod = import_module(temp_module_name)
            sys.path.pop(0)
            cfg_dict = {
                name: value
                for name, value in mod.__dict__.items()
                if not name.startswith("__")
            }
            # delete imported module
            del sys.modules[temp_module_name]

            # close temp file
            temp_config_file.close()

        cfg_text = filename + "\n"
        with open(filename, "r", encoding="utf-8") as f:
            # Setting encoding explicitly to resolve coding issue on windows
            cfg_text += f.read()

        if BASE_KEY in cfg_dict:
            cfg_dir = osp.dirname(filename)
            base_filename = cfg_dict.pop(BASE_KEY)
            base_filename = (
                base_filename
                if isinstance(base_filename, list)
                else [base_filename]
            )

            cfg_dict_list = list()
            cfg_text_list = list()
            for f in base_filename:
                _cfg_dict, _cfg_text = Config._file2dict(osp.join(cfg_dir, f))
                cfg_dict_list.append(_cfg_dict)
                cfg_text_list.append(_cfg_text)

            base_cfg_dict = dict()
            for c in cfg_dict_list:
                if len(base_cfg_dict.keys() & c.keys()) > 0:
                    raise KeyError("Duplicate key is not allowed among bases")
                base_cfg_dict.update(c)

            base_cfg_dict = Config._merge_a_into_b(cfg_dict, base_cfg_dict)
            cfg_dict = base_cfg_dict

            # merge cfg_text
            cfg_text_list.append(cfg_text)
            cfg_text = "\n".join(cfg_text_list)

        return cfg_dict, cfg_text

    @staticmethod
    def _merge_a_into_b(a, b, allow_list_keys=False):
        """merge dict ``a`` into dict ``b`` (non-inplace).
        Values in ``a`` will overwrite ``b``. ``b`` is copied first to avoid
        in-place modifications.
        Args:
            a (dict): The source dict to be merged into ``b``.
            b (dict): The origin dict to be fetch keys from ``a``.
            allow_list_keys (bool): If True, int string keys (e.g. '0', '1')
                are allowed in source ``a`` and will replace the element of the
                corresponding index in b if b is a list. Default: False.
        Returns:
            dict: The modified dict of ``b`` using ``a``.
        Examples:
            # Normally merge a into b.
            >>> Config._merge_a_into_b(
            ...     dict(obj=dict(a=2)), dict(obj=dict(a=1)))
            {'obj': {'a': 2}}
            # Delete b first and merge a into b.
            >>> Config._merge_a_into_b(
            ...     dict(obj=dict(_delete_=True, a=2)), dict(obj=dict(a=1)))
            {'obj': {'a': 2}}
            # b is a list
            >>> Config._merge_a_into_b(
            ...     {'0': dict(a=2)}, [dict(a=1), dict(b=2)], True)
            [{'a': 2}, {'b': 2}]
        """
        b = b.copy()
        for k, v in a.items():
            if allow_list_keys and k.isdigit() and isinstance(b, list):
                k = int(k)
                if len(b) <= k:
                    raise KeyError(f"Index {k} exceeds the length of list {b}")
                b[k] = Config._merge_a_into_b(v, b[k], allow_list_keys)
            elif (
                isinstance(v, dict) and k in b and not v.pop(DELETE_KEY, False)
            ):
                allowed_types = (dict, list) if allow_list_keys else dict
                if not isinstance(b[k], allowed_types):
                    raise TypeError(
                        f"{k}={v} in child config cannot inherit from base "
                        f"because {k} is a dict in the child config but is of "
                        f"type {type(b[k])} in base config. You may set "
                        f"`{DELETE_KEY}=True` to ignore the base config"
                    )
                b[k] = Config._merge_a_into_b(v, b[k], allow_list_keys)
            else:
                b[k] = v
        return b

    @staticmethod
    def fromfile(
        filename, use_predefined_variables=True
    ):
        cfg_dict, cfg_text = Config._file2dict(
            filename, use_predefined_variables
        )
        return Config(cfg_dict, cfg_text=cfg_text, filename=filename)

    @staticmethod
    def fromstring(cfg_str, file_format):
        """Generate config from config str.
        Args:
            cfg_str (str): Config str.
            file_format (str): Config file format corresponding to the
                config str. Only py type are supported now!
        Returns:
            obj:`Config`: Config obj.
        """
        if file_format not in [".py"]:
            raise IOError("Only py type are supported now!")
        if file_format != ".py" and "dict(" in cfg_str:
            # check if users specify a wrong suffix for python
            warnings.warn(
                'Please check "file_format", the file format may be .py'
            )

        with tempfile.NamedTemporaryFile("w", suffix=file_format) as temp_file:
            temp_file.write(cfg_str)
            temp_file.flush()
            cfg = Config.fromfile(temp_file.name)
        return cfg

    @staticmethod
    def auto_argparser(description=None):
        """Generate argparser from config file automatically (experimental)"""
        partial_parser = ArgumentParser(description=description)
        partial_parser.add_argument("config", help="config file path")
        cfg_file = partial_parser.parse_known_args()[0].config
        cfg = Config.fromfile(cfg_file)
        parser = ArgumentParser(description=description)
        parser.add_argument("config", help="config file path")
        add_args(parser, cfg)
        return parser, cfg

    def __init__(self, cfg_dict=None, cfg_text=None, filename=None):
        if cfg_dict is None:
            cfg_dict = dict()
        elif not isinstance(cfg_dict, dict):
            raise TypeError(
                "cfg_dict must be a dict, but " f"got {type(cfg_dict)}"
            )
        for key in cfg_dict:
            if key in RESERVED_KEYS:
                raise KeyError(f"{key} is reserved for config file")

        super(Config, self).__setattr__("_cfg_dict", ConfigDict(cfg_dict))
        super(Config, self).__setattr__("_filename", filename)
        if cfg_text:
            text = cfg_text
        elif filename:
            with open(filename, "r") as f:
                text = f.read()
        else:
            text = ""
        super(Config, self).__setattr__("_text", text)

    @property
    def filename(self):
        return self._filename

    @property
    def text(self):
        return self._text

    def __repr__(self):
        return f"Config (path: {self.filename}): {self._cfg_dict.__repr__()}"

    def __len__(self):
        return len(self._cfg_dict)

    def __getattr__(self, name):
        return getattr(self._cfg_dict, name)

    def __getitem__(self, name):
        return self._cfg_dict.__getitem__(name)

    def __setattr__(self, name, value):
        if isinstance(value, dict):
            value = ConfigDict(value)
        self._cfg_dict.__setattr__(name, value)

    def __setitem__(self, name, value):
        if isinstance(value, dict):
            value = ConfigDict(value)
        self._cfg_dict.__setitem__(name, value)

    def __iter__(self):
        return iter(self._cfg_dict)

    def __getstate__(self):
        return (self._cfg_dict, self._filename, self._text)

    def __setstate__(self, state):
        _cfg_dict, _filename, _text = state
        super(Config, self).__setattr__("_cfg_dict", _cfg_dict)
        super(Config, self).__setattr__("_filename", _filename)
        super(Config, self).__setattr__("_text", _text)

    def merge_from_dict(self, options, allow_list_keys=True):
        """Merge list into cfg_dict.
        Merge the dict parsed by MultipleKVAction into this cfg.
        Examples:
            >>> options = {'model.backbone.depth': 50,
            ...            'model.backbone.with_cp':True}
            >>> cfg = Config(dict(model=dict(backbone=dict(type='ResNet'))))
            >>> cfg.merge_from_dict(options)
            >>> cfg_dict = super(Config, self).__getattribute__('_cfg_dict')
            >>> assert cfg_dict == dict(
            ...     model=dict(backbone=dict(depth=50, with_cp=True)))
            # Merge list element
            >>> cfg = Config(dict(pipeline=[
            ...     dict(type='LoadImage'), dict(type='LoadAnnotations')]))
            >>> options = dict(pipeline={'0': dict(type='SelfLoadImage')})
            >>> cfg.merge_from_dict(options, allow_list_keys=True)
            >>> cfg_dict = super(Config, self).__getattribute__('_cfg_dict')
            >>> assert cfg_dict == dict(pipeline=[
            ...     dict(type='SelfLoadImage'), dict(type='LoadAnnotations')])
        Args:
            options (dict): dict of configs to merge from.
            allow_list_keys (bool): If True, int string keys (e.g. '0', '1')
              are allowed in ``options`` and will replace the element of the
              corresponding index in the config if the config is a list.
              Default: True.
        """
        option_cfg_dict = {}
        for full_key, v in options.items():
            d = option_cfg_dict
            key_list = full_key.split(".")
            for subkey in key_list[:-1]:
                d.setdefault(subkey, ConfigDict())
                d = d[subkey]
            subkey = key_list[-1]
            d[subkey] = v

        cfg_dict = super(Config, self).__getattribute__("_cfg_dict")
        super(Config, self).__setattr__(
            "_cfg_dict",
            Config._merge_a_into_b(
                option_cfg_dict, cfg_dict, allow_list_keys=allow_list_keys
            ),
        )
