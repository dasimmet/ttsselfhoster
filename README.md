# ttsselfhoster.py

this is a python3 Script to download Ressources for Tabletop Simulator.

- it reads a JSON encoded TTS Save file from stdin (or set by "-i")
- downloads all found Assets in an output directory
- builds sha512sums of them
- replaces the url in the json if one is supplied via "-u"
- and outputs a edited JSON Save file into the output directory or stdout if "-o -" is given.

the resulting json can be run in TTS, if the output directory is available via the supplied url.

```
usage: ttsselfhoster.py [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [-s SERVER_DIR]
                        [-n] [-u URL]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
  -s SERVER_DIR, --server_dir SERVER_DIR
  -n, --no_cache
  -u URL, --url URL
```

