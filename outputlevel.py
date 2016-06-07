# -*- coding: utf-8 -*-
import enum

class OutputLevel(enum.Enum):
  __order__ = 'maximum verbose default minimum'
  maximum = 1
  verbose = 2
  default = 3
  minimum = 4
