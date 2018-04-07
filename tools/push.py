#!/usr/bin/python3
#coding=utf8

import argparse
import json
from io import StringIO
import re
import requests
import yaml
import markdown
from lxml import html

# load article file
def _get_file(path):
    if (path.startswith('http://')
            or path.startswith('https://') 
            or path.startswith('ftp://')):
        r = requests.get(path)
        return StringIO(r.content)
    return open(path)


# default summary if no summary offered
def _gen_summary(mdtext, n=180):
    htmltext = markdown.markdown(mdtext)
    tree = html.fromstring(htmltext)
    node = tree.xpath('.')[0]
    text = re.sub('\s+', ' ', node.text_content()).strip()
    return text[:n] + ' ...'


def publish(stream, api, token):
    # parse article header by yaml
    headers = []
    for line in stream:
        if not line:
            break
        line = line.rstrip()
        headers.append(line)
        if line == '...':
            break

    cfg = yaml.load(StringIO('\n'.join(headers)))
    if not cfg:
        raise ValueError('no valid yaml config informations')
    if 'title' not in cfg:
        raise ValueError('no title found')
    if 'tags' in cfg and not isinstance(cfg['tags'], list):
        raise ValueError('invalid tags: it should be list')

    # parse article body
    bodies = []
    for line in stream:
        bodies.append(line.rstrip())
    # content = '\n'.join(bodies).strip().decode('utf8')
    content = '\n'.join(bodies).strip()
    if not content:
        raise ValueError('no content found')

    data = {
        'token': token,
        'title': cfg['title'],
        'summary': cfg.get('summary', None) or _gen_summary(content),
        'content': content,
    }
    if 'tags' in cfg:
        data['tags'] = cfg['tags']
    # if 'pub_time' in cfg:
        # data['pub_time'] = cfg['pub_time']
    
    # post it through network (handled in views.py)
    r = requests.post(api, data=data)
    assert r.status_code, r.content
    print('err:' + str(r.status_code) + ', msg:' + r.content.decode())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path',  help='file path or url(http, https or ftp)')
    parser.add_argument('-a', '--api',   help='api address')
    parser.add_argument('-t', '--token', help='access token')
    parser.add_argument('-i', '--id', help='article id if want to modify article')
    args = parser.parse_args()

    if not args.path or not args.api or not args.token:
        parser.print_help()
        return
    
    if args.id:
        args.api += "/repost?id=" + str(args.id)
    else:
        args.api += "/post"

    # load the file
    stream = _get_file(args.path)
    # publish it
    publish(stream, args.api, args.token)


if __name__ == '__main__':
    main()
