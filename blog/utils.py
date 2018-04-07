#coding=utf8

import markdown
from datetime import datetime
from . import app


def format_date(dateobj):
    return dateobj.strftime(
        '%Y-%m-%d')


def format_date_weekday(dateobj):
    return dateobj.strftime(
        ' %Y-%m-%d  %A')


def format_datetime(dateobj):
    return dateobj.strftime(
        '%A %b %d,%Y %H:%M:%S')


def format_datetime_weekday(dateobj):
    return dateobj.strftime(
        '%Y-%m-%d %H:%M')


app.jinja_env.globals['format_date'] = format_date
app.jinja_env.globals['format_date_weekday'] = format_date_weekday
app.jinja_env.globals['format_datetime'] = format_datetime
app.jinja_env.globals['format_datetime_weekday'] = format_datetime_weekday


def markdown2html(mdtext):
    exts = ['extra',
            'codehilite',
            'tables',
            'fenced_code',
            'toc']

    # return markdown.markdown(mdtext, extensions=['fenced_code', 'codehilite'])
    return markdown.markdown(mdtext, extensions=exts)

# load local markdown file
def load_content(name):
    # suffix must be ".md"
    with open('{}.md'.format(name)) as f:
        # mdtext = f.read().decode('utf8', 'ignore')
        mdtext = f.read()
    return markdown2html(mdtext)
