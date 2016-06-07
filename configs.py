# -*- coding: utf-8 -*-
import os, yaml

from compresstype import CompressType

class Configs:

  default_config_path = "%s/logagg.yml" % os.path.dirname(os.path.abspath(__file__))

  def __init__(self, env = None):
    self.configs = [Configs.default_config_path]
    self.init    = True
    self.env     = env

  def add(self, path):
    if self.init:
      self.configs.remove(Configs.default_config_path)
      self.init = False
    self.configs.append(path)

  def read(self):
    rt = ""
    for config in self.configs:
      if os.path.isfile(config) == False: continue
      rt = rt + open(config).read().decode('utf8')
    return rt

  def load(self):
    rt = []
    for group in yaml.load(self.read()):
      rt.append(Config(group, self.env))
    return rt

class Config:

  def __init__(self, config, env = None):
    self.config = config
    self.env    = env

  def hosts(self):
    rt = []
    for host in self.config["hosts"]:
      if isinstance(host, dict):
        if host.get(self.env) is not None:
          rt = rt + host.get(self.env)
      else:
        rt.append(host)
    return rt

  def logs(self):
    rt = []
    for logs in self.config["logs"]:
      rt.append(LogConfig(logs))
    return rt

class LogConfig:

  def __init__(self, config):
    self.config = config

  def path(self, replaces = {}):
    rt = self.config["path"]
    for k, v in replaces.items():
      rt = rt.replace(k, v)
    return rt

  def ignore_patterns(self):
    return self.config["ignore-patterns"]

  def grep_patterns(self):
    return self.config["patterns"]

  def compress_type(self):
    try:
      return CompressType[self.config["compress-type"]]
    except KeyError:
      return CompressType.none
