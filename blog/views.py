#coding=utf8

from datetime import datetime
import json

from flask import render_template, request, abort, redirect, url_for 
from . import app
from .models import (Article, Tag, create_article, repost_article)
from .utils import markdown2html, load_content


@app.errorhandler(404)
def page_not_found(error):
    # title = unicode(error)
    title = error
    message = error.description
    return render_template('errors.html',
                           title=title,
                           message=message)


@app.errorhandler(500)
def internal_server_error(error):
    # title = unicode(error)
    title = error
    message = error.description
    return render_template('errors.html',
                           title=title,
                           message=message)


@app.route('/')
def redirect2index():
    return redirect(url_for('index'), code=301)


@app.route('/index')
def index():
    posts = app.config['POSTS_PER_PAGE']
    page = request.args.get('page', 1, type=int)    
    pagination = Article.query.order_by(Article.id.desc()).paginate(page, posts, True)
    posts = pagination.items
    return render_template('index.html', posts=posts,
                           pagination=pagination)


@app.route('/article/<id>')
def show_article(id):
    article = Article.query.get_or_404(id)
    content = '<h1>' + article.title +'</h1>' + markdown2html(article.content)
    return render_template('page.html',
                           title=article.title,
                           content=content,
                           pub_time=article.pub_time,
                           tags=article.tags)

@app.route('/tags')
def show_tags():
    tags = Tag.query.all()
    return render_template('tags.html',
                           tags=tags)

@app.route('/tag/<id>')
def show_tag(id):
    tag = Tag.query.get_or_404(id)
    articles = tag.articles.all()
    return render_template('tag.html',
                           tag=tag,
                           entries=articles)


@app.route('/about')
def about():
    content = load_content('personel/about')
    return render_template('page.html',
                           title='About',
                           content=content)


@app.route('/links')
def links():
    content = load_content('personel/links')
    return render_template('page.html',
                           title='Links',
                           content=content)


def auth(token):
    if token != app.config['TOKEN']:
        return False
    return True


@app.route('/repost', methods=['GET', 'POST'])
def repost():
    if request.method == 'GET':
        abort(404)

    id = request.args.get('id')
    if not id:
        return 'no id found', 500

    token = request.form.get('token', '')
    if not auth(token):
        return 'invalid access token', 500

    token = request.form.get('token', '')
    if not auth(token):
        return 'invalid access token', 500

    title = request.form.get('title', None)
    if not title:
        return 'no title found', 500

    summary = request.form.get('summary', None)
    if not summary:
        return 'no summary found', 500

    content = request.form.get('content', None)
    if not content:
        return 'no content found', 500

    # pub_time = request.form.get('pub_time', None)
    # if pub_time:
        # pub_time = datetime.strptime(pub_time, app.config['TIME_FORMAT'])

    tags = request.form.getlist('tags')
    
    if repost_article(id, title, summary, content, tags):
        return 'reposted successfully', 200

    return 'some errors occured when reposting', 500


@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'GET':
        abort(404)

    token = request.form.get('token', '')
    if not auth(token):
        return 'invalid access token', 500

    title = request.form.get('title', None)
    if not title:
        return 'no title found', 500

    summary = request.form.get('summary', None)
    if not summary:
        return 'no summary found', 500

    content = request.form.get('content', None)
    if not content:
        return 'no content found', 500

    pub_time = request.form.get('pub_time', None)
    if pub_time:
        pub_time = datetime.strptime(pub_time, app.config['TIME_FORMAT'])

    tags = request.form.getlist('tags')

    create_article(title, summary, content, pub_time, tags)
    return 'posted successfully', 200
