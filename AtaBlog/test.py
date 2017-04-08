#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
import codecs

from AtaBlog.MongoDBUtil import MongoDBUtil
from AtaBlog.items import *

MongoDBUtil.__init__()

def save1():
    # authorItem = AuthorItem()
    # authorItem['authorName'] = "thomugo"
    # authorItem['authorHomePage'] = "www.baidu.com"
    # author = dict(authorItem)
    #MongoDBUtil.save_author_item(authorItem)
    #MongoDBUtil.authorItemCollection.insert(author)
    authorItem = MongoDBUtil.authorItemCollection.find_one({'authorName':"thomugo"})
    blogItem = AtablogItem()
    blogItem['id'] = "123"
    blogItem['blog'] = "test"
    blogItem['dir'] = './test'
    blogItem['title'] = "title"
    blogItem['tags'] = ['a', 'b']
    blogItem['mark'] = 2
    blogItem['vote'] = 3
    blogItem['author'] = authorItem
    blog = dict(blogItem)
    MongoDBUtil.blogItemCollection.insert(blog)
    #MongoDBUtil.save_blog_item(blogItem)

def save2():
    authorItem = AuthorItem()
    authorItem['authorName'] = "thomugo"
    authorItem['authorHomePage'] = "www.baidu.com"
    blogItem = AtablogItem()
    blogItem['id'] = "123"
    blogItem['blog'] = "test"
    blogItem['dir'] = './test'
    blogItem['title'] = "title"
    blogItem['tags'] = ['a', 'b']
    blogItem['mark'] = 2
    blogItem['vote'] = 3
    MongoDBUtil.save_blog(authorItem, blogItem)

def find():
    author = MongoDBUtil.authorItemCollection.find_one({"authorName":"thomugo"})
    print author
    blog = MongoDBUtil.blogItemCollection.find_one({"id":'123'})
    author = blog['author']['authorName']
    print author
    print blog

def find1():
    blog = MongoDBUtil.blogItemCollection.find_one({"id":'123'}, {"id": 1, "_id":0})
    print blog

def getStartUrl():
    print MongoDBUtil.get_last_article_url()

def testPriorityQueue():
    q = Queue.PriorityQueue()
    q.put((1, "test1"))
    q.put((3, "test3"))
    q.put((2, "test2"))
    print q.get()[1]
    print q.qsize()
    print q.get()[1]
    print q.qsize()
    print q.get()[1]
    print q.qsize()

def testGetBlog():
    blog = MongoDBUtil.get_blog("0、Python与设计模式--前言")
    with codecs.open(u"0、Python与设计模式--前言.md", 'wb', encoding="utf-8") as md:
        md.write(blog['blog'])

#save1()
#save2()
#find()
#find1()
#getStartUrl()
#MongoDBUtil.get_avg_vote()
#MongoDBUtil.get_vote_avg()
#testPriorityQueue()
#testGetBlog()
#print MongoDBUtil.isUrlScrawled('72373')