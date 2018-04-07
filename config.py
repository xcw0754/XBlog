#coding=utf8

# db path (must change)
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/blog.db'

# blog name
AUTHOR = 'xcw0754'

# for sorting
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# for publish article
TOKEN = '123456'

POSTS_PER_PAGE = 10

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_TEARDOWN = True
