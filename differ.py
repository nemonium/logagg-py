# -*- coding: utf-8 -*-
import os, subprocess

from outputlevel import OutputLevel

class Differ:

  def __init__(self, fromfile, tofile):
    self.fromfile = fromfile
    self.tofile   = tofile
    self.suffix   = ".diff"
    self.preview  = 10
    self.debug    = None

  def filename(self):
    return self.fromfile + self.suffix

  def diff(self):
    cmd = "diff --new-line-format='%%L' --unchanged-line-format='' %s %s" % (self.fromfile, self.tofile)
    if self.debug is not None: self.debug("      %s" % cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return stdout

  def wdiff(self, suffix = None):
    if suffix is not None:
      self.suffix = suffix
    self.write(self.diff())

  def write(self, str):
    f = open(self.filename(), "w")
    try:
      f.write(str)
    finally:
      f.close()

  def length(self):
    return sum(1 for line in open(self.filename()))

  def isfile(self):
    return os.path.isfile(self.filename())

  def remove(self):
    if self.isfile():
      return os.remove(self.filename())

  def message(self, level = OutputLevel.default):
    rt = []
    if self.length() < 1:
      return rt
    msg = ""
    for idx, line in enumerate(open(self.filename(), "r")):
      if idx >= self.preview:
        msg = msg + "<br>..."
        break
      msg = msg + ("<br>%s" % (line.strip()))
    rt.append("|%8d|[other]%s|" % (self.length(), msg))
    return rt