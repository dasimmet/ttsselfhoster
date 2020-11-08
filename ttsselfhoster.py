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
                sha_url, sha_f = cache_file(val, args.server_dir, force=args.no_cache)
                print(sha_f, file=sys.stderr)
            if args.url and sha_f:
                newurl = args.url + "/blocks/" + sha_f
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
    p.add_argument("-n","--no_cache", action="store_true")
    p.add_argument("-u","--url", default=None)
    return p

def dict_set(dic , path, val):
    iter_dic = dic
    for p in path:
        last_dic = iter_dic
        iter_dic = iter_dic[p]
    last_dic[p] = val


def cache_file(url, cache_dir, force=True):
    import os
    import hashlib
    blocks_dir = os.path.join(cache_dir,"blocks")
    sha_url = hashlib.sha512()
    sha_url.update(url.encode())
    sha_url = sha_url.hexdigest()
    sha_dir = os.path.join(cache_dir, "sha")
    sha_file = os.path.join(sha_dir, sha_url)

    if not os.path.isdir(blocks_dir):
        os.makedirs(blocks_dir)
    if not os.path.isdir(sha_dir):
        os.makedirs(sha_dir)
    cachefile = os.path.join(blocks_dir, sha_url)
    if force or (not os.path.isfile(cachefile)):
        sha_req = get_file(url, cachefile, sha_file)

    return (sha_url, sha_req)

def get_file(url, cachefile, sha_file):
    from urllib.request import urlopen
    from urllib.error import HTTPError
    import hashlib
    import sys
    import os
    sha_f = hashlib.sha512()
    try:
        with urlopen(url) as req:
            with open(cachefile,"wb") as fd:
                BUF = True
                while BUF:
                    BUF = req.read()
                    fd.write(BUF)
                    sha_f.update(BUF)
    except HTTPError as ex:
        print(ex, file=sys.stderr)
        try:
            os.unlink(cachefile)
            os.unlink(sha_file)
        except:
            pass
        return None
    sha_f = sha_f.hexdigest()
    with open(sha_file, "w") as fd:
        fd.write(sha_f)
    return sha_f

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
