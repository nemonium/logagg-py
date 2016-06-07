# -*- coding: utf-8 -*-
import enum

class CompressType(enum.Enum):
  __order__ = 'none gz'
  none = { "cmd" : "cat" }
  gz   = { "cmd" : "zcat" }
