# -*- coding: utf-8 -*-
import os, subprocess
import hashlib

class Downloader:

  def __init__(self, path, host, port = 22):
    self.path      = path
    self.host      = host
    self.port      = port
    self.resultdir = "."
    self.suffix    = ""
    self.debug     = None
    self.cmd       = "cat"

  def filename(self):
    return "%s/%s" % (self.resultdir, hashlib.md5(self.host + self.path).hexdigest()) + self.suffix

  def paths(self):
    cmd = "ssh -p %d %s 'ls %s'" % (self.port, self.host, self.path)
    if self.debug is not None: self.debug("      %s" % cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return stdout.split()

  def download(self, path):
    cmd = "ssh -p %d %s '%s %s'" % (self.port, self.host, self.cmd, path)
    if self.debug is not None: self.debug("      %s" % cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return stdout

  def wdownload(self, resultdir = None, suffix = None):
    if resultdir is not None:
      self.resultdir = resultdir
    if suffix is not None:
      self.suffix = suffix
    for path in self.paths():
      self.write(self.download(path))

  def write(self, str):
    f = open(self.filename(), "a")
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