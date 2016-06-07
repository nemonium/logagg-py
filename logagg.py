# -*- coding: utf-8 -*-
import sys, os, subprocess, getopt, shutil, datetime
import markdown

from outputlevel import OutputLevel
from downloader import Downloader
from greper import Greper
from differ import Differ
from configs import Configs

# define
ignore_suffix = ".ignore"
grep_suffix = ".grep"
diff_suffix = ".diff"

# options
date = "1 day ago"
default_ssh_port = 22
app_name, ext = os.path.splitext(os.path.basename(__file__))
temporary_dir = "/tmp/%s" % (app_name)
debug = False
level = None
html = False
configs = Configs()

opts, args = getopt.getopt(sys.argv[1:], "c:d:e:o:p:DvH", ["maximum", "minimum"])
for o, a in opts:
  if o == "-c":
    configs.add(a)
  if o == "-d":
    date = a
  if o == "-e":
    configs.env = a
  if o == "-o":
    temporary_dir = "%s/%s" % (a, app_name)
  if o == "-p":
    default_ssh_port = int(a)
  if o == "-D":
    debug = True
  if o == "-H":
    html = True
  if o == "-v":
    if level == None or level > OutputLevel.verbose:
      level = OutputLevel.verbose
  if o in ("--maximum"):
    if level == None or level > OutputLevel.maximum:
      level = OutputLevel.maximum
  if o in ("--minimum"):
    if level == None or level > OutputLevel.minimum:
      level = OutputLevel.minimum

if level == None: level = OutputLevel.default

def target_date(date = date, format = "%Y%m%d"):
  cmd = "date --date '%s' +'%s'" % (date, format)
  p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout, stderr = p.communicate()
  return stdout.rstrip()

def debug_print(message):
  if debug:
    d = datetime.datetime.today()
    print >> sys.stderr, d.strftime("%Y-%m-%d %H:%M:%S"), message

def main():
  for config in configs.load():
    for host in config.hosts():
      debug_print(host)
      messages = []
      for log in config.logs():
        path = log.path({ "YYYYMMDD":target_date() })
        debug_print("  %s" % path)

        # download by scp
        debug_print("    Transferring a log-file to the local.")
        dl = Downloader(path, host, default_ssh_port)
        if debug is True: dl.debug = debug_print
        dl.cmd = log.compress_type().get("cmd")
        dl.wdownload(temporary_dir)
        if dl.isfile():
          # ignore
          debug_print("    Extracting of a exclude line.")
          i = Greper(dl.filename(), log.ignore_patterns(), True)
          if debug is True: i.debug = debug_print
          i.wgrep(ignore_suffix)
          # grep
          debug_print("    Extracting of a aggregation line.")
          g = Greper(i.filename(), log.grep_patterns())
          if debug is True: g.debug = debug_print
          g.wgrep(grep_suffix)
          # diff
          debug_print("    Extracting of a other messages.")
          d = Differ(i.filename(), g.filename())
          if debug is True: d.debug = debug_print
          d.wdiff(diff_suffix)
          # reporting
          if level > OutputLevel.verbose and i.length() == 0:
            dl.remove()
            i.remove()
            g.remove()
            d.remove()
            continue
          debug_print("    In reporting.")
          msg = []
          msg.extend(i.message(level))
          msg.extend(g.message(level))
          msg.extend(d.message(level))
          if level < OutputLevel.default or len(msg) > 0:
            if html:
              messages.append("")
              messages.append("### %s" % path)
              messages.append('| | |')
              messages.append('|-|-|')
            else:
              messages.append("### %s" % path)
            messages.extend(msg)
          i.remove()
          g.remove()
          d.remove()
        dl.remove()

      if len(messages) > 0:
        messages.insert(0, "# %s" % host)
        if html:
          md = markdown.Markdown(extensions = ['markdown.extensions.tables'])
          print md.convert("\n".join(messages))
        else:
          print ("\n".join(messages).replace('<br>', '\n|      '))

if __name__ == '__main__':
  if not os.path.exists(temporary_dir):
    os.makedirs(temporary_dir)
  main()