# -*- coding: utf-8 -*-
"""test read_config"""
from configparser import ConfigParser
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict
import pytest
from configmanager import ConfigManager


@pytest.mark.skip
def test_read_config():
    """test read_config"""
    accesstokenkey = NamedTemporaryFile("w+", prefix="tmpacctoken")
    accesstokenkey.write("    accesstokenkey")
    accesstokenkey.seek(0)
    with NamedTemporaryFile("w", suffix=".ini") as tmpconf:
        config: ConfigParser = ConfigParser()
        config["KEYS"] = {
            "ConsumerKey": "consumerkey",
            "ConsumerSecret": "CONSUMERSECRET",
            "AccessTokenKey": accesstokenkey.name,
            "AccessTokenSecret": "AccessTokenSecret",
        }

        config["LOCATIONS"] = {
            "TweetDir": str(Path().home()),
            "LogLocation": "/fake/log/dir",
        }

        config.write(tmpconf)
        # TODO (jam) reintegrate this
        myconfig = ConfigManager(project="test", template={}, config_file=tmpconf.name)
        conf: Dict[str, Dict[str, str]] = myconfig.read_config()

    assert conf["keys"]["ConsumerKey"] == "consumerkey"
    assert conf["keys"]["ConsumerSecret"] == "CONSUMERSECRET"
    assert conf["keys"]["AccessTokenKey"] == "accesstokenkey"
    assert conf["keys"]["AccessTokenSecret"] == "AccessTokenSecret"
    assert conf["locations"]["TweetDir"] == str(Path().home())
    assert conf["locations"]["LogLocation"] == "/fake/log/dir"
    accesstokenkey.close()
