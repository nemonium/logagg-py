# -*- coding: utf-8 -*-
import os, subprocess, re

from outputlevel import OutputLevel

class Greper:

  def __init__(self, basefile, patterns, ignore = False):
    self.basefile = basefile
    self.patterns = patterns
    self.ignore   = ignore
    self.suffix   = ".grep"
    self.debug    = None

  def filename(self):
    return self.basefile + self.suffix

  def grep(self):
    conditions = []
    cmd = "cat %s" % (((self.ignore and self.basefile) or "/dev/null"))
    if self.patterns is not None:
      if self.ignore: conditions.append("-v")
      for pattern in self.patterns:
        if isinstance(pattern, dict):
          conditions.append("-e '%s'" % re.sub(r'\'', '\'"\'"\'', pattern["regex"]))
        else:
          conditions.append("-e '%s'" % re.sub(r'\'', '\'"\'"\'', pattern))
      cmd = "grep %s %s" % (" ".join(conditions), self.basefile)
    if self.debug is not None: self.debug("      %s" % cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return stdout

  def wgrep(self, suffix = None):
    if suffix is not None:
      self.suffix = suffix
    self.write(self.grep())

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

  def glength(self, pattern):
    conditions = []
    conditions.append("-e '%s'" % re.sub(r'\'', '\'"\'"\'', pattern))
    cmd = "grep %s %s | wc -l" % (" ".join(conditions), self.basefile)
    if self.debug is not None: self.debug("      %s" % cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return int(stdout.rstrip())

  def message(self, level = OutputLevel.default):
    rt = []
    if type(self.patterns) is not list:
      return rt
    elif level == OutputLevel.minimum:
      return rt
    elif self.ignore == True and level > OutputLevel.maximum:
      return rt
    for pattern in self.patterns:
      length = self.glength(pattern["regex"] if isinstance(pattern, dict) else pattern)
      if level > OutputLevel.verbose and length == 0:
        continue
      rt.append("|%8d|%s|" % (length, (pattern["alias"] if isinstance(pattern, dict) else pattern)))
    return rt