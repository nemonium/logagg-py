# logagg-py

Log aggregator

## Usage

    logagg.py [-c config]...[-d date][-D][-e env][-o dir][-p port][-v][-H]

        -c <arg> : config of yaml. default logagg.yml
        -d <arg> : target date. default `1 day ago`
        -D       : debug
        -e <arg> : environment
        -o <arg> : directory for outputting a temporary file
                   In fact , `<arg>/logagg` is output destination
                   default `/tmp`
        -p <arg> : default ssh port. default `22`
        -H       : Output Html format
        -v       : verbose

## Config

### logagg.yml

*format*

~~~
 - hosts:
   - <user>@<hostname>
   - <env>:
     - <user>@<hostname>
   logs:
   - path: <logfile-path>
     compress-type: <none|gz>        # Undefined is `none`
     ignore-patterns:
       - <ignore-message-pattern>
     patterns:
       - <grep-message-pattern>
       # OR
       - regex: <grep-message-pattern>
         alias: <alias value>        # Displayed for report
~~~

## Temporary files

~~~
/tmp/logagg
|-- <host + path to hexdigest>              # Original
|-- <host + path to hexdigest>.ignore       # Result of applying the ignore patterns from Original
|-- <host + path to hexdigest>.ignore.grep  # Result of applying the extraction pattern from .ignore
`-- <host + path to hexdigest>.ignore.diff  # Line that was not the case in the extraction pattern
~~~

## Package Dependencies

- pyyaml
- enum
- markdown
