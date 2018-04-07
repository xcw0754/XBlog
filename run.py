#!/usr/bin/python3
#coding=utf8

from blog import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
