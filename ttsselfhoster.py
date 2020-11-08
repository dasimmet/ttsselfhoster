#!/usr/bin/env python3

def main():
    import os
    import json
    import re
    import sys
    p = parser()
    args = p.parse_args()
    with open(args.input_file) as fd:
        js = json.load(fd)
    jsgen = dict_generator(js)
    url_regex = re.compile("^https?://")
    for it in jsgen:
        val = it[-1]
        if type(val)==str and url_regex.match(val):
            print(it, file=sys.stderr)
            if args.server_dir:
                sha, cachefile = cache_file(val, args.server_dir)
                print(cachefile, file=sys.stderr)
            if args.url:
                newurl = args.url + "/blocks/" + sha
                dict_set(js, it[:-1], newurl)
    if args.output_file == "-":
        json.dump(js, sys.stdout)
    else:
        with open(args.output_file, "w") as fd:
            json.dump(js, sys.stdout)


def parser():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("-f","--input_file", required=True)
    p.add_argument("-o","--output_file", default="-")
    p.add_argument("-s","--server_dir", default=None)
    p.add_argument("-u","--url", default=None)
    return p

def dict_set(dic , path, val):
    iter_dic = dic
    for p in path:
        last_dic = iter_dic
        iter_dic = iter_dic[p]
    last_dic[p] = val


def cache_file(url, cache_dir):
    from urllib.request import urlopen
    import os
    import uuid
    import hashlib
    blocks_dir = os.path.join(cache_dir,"blocks")
    sha_url = hashlib.sha512()
    sha_url.update(url.encode())
    sha_url = sha_url.hexdigest()

    if not os.path.isdir(blocks_dir):
        os.makedirs(blocks_dir)
    cachefile = os.path.join(blocks_dir, sha_url)
    mode = "wb"
    # if os.path.isfile(cachefile):
    #     mode = "rb"
    BS=2**20
    sha_req = hashlib.sha512()
    sha_cache = hashlib.sha512()
    with urlopen(url) as req:
        with open(cachefile,mode) as fd:
            BUF = True
            while BUF:
                BUF = req.read()
                fd.write(BUF)
                sha_req.update(BUF)


    return (sha_url, cachefile)

def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in dict_generator(value, pre + [key]):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                i = 0
                for v in value:
                    for d in dict_generator(v, pre + [key,i]):
                        yield d
                    i += 1
            else:
                yield pre + [key, value]
    else:
        yield pre + [indict]

if __name__ == "__main__":
    main()
