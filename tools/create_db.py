#!/usr/bin/python3
import sys
sys.path.append("..")

from blog.database import db

if __name__ == '__main__':
    db.create_all()
