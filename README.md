XBlog
======

![index-page](https://raw.githubusercontent.com/xcw0754/xblog/master/screenshots/index-page.png)

XBlog是个基于Flask的博客。


Requirements
------------

- Python3
- Flask
- Flask-SQLAlchemy
- Jinja2
- Markdown
- MarkupSafe
- Pygments
- Werkzeug
- SQLAlchemy
- lxml
- PyYAML
- requests


Quick Start
-----------

依赖工具的版本都在`requirements.txt`中，类似如下命令安装即可
```
sudo pip3 install Flask==0.10.1
```

创建数据库
```
$./create_db.py
```

配置文件
```
$vim config.py
```

开始监听
```
$./run.py
```

现在可以在浏览器中访问http://127.0.0.1


Writing and Publishing
-------------

请参照`example.md`仿写文章，tools目录下有个push工具可以用来发表文章，比如这样
```
$./push.py -a http://127.0.0.1 -p example.md -t 123456
```

修改文章也是push工具，比如修改编号为3(以uri中的编号为准)的文章可以这样
```
$./push.py -a http://127.0.0.1 -p example.md -t 123456 -i 3

```


Notes
-----

- 文章以markdown格式存储于sqlite中
- markdown转html是在请求时进行的
- h1是文章标题，一般不要使用
- 代码块需要用`~~~~`括起来，并附带语言才会高亮


TODO
----

* 文章超过n篇自动换页  √
* 支持修改文章  √
* 支持文章带图片
* 支持评论
* SQL安全检查
* 文章搜索
* 缓存文章以避免多次解析markdown
* 支持跳转至首末页
* 支持HTTPS
* 单元测试
