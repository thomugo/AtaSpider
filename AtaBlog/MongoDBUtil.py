#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from random import randint

import math
from bson import Code
from bson import SON
from scrapy import log
from pymongo import MongoClient
from scrapy.utils.decorators import deprecated

from AtaBlog.settings import *
from pymongo.son_manipulator import AutoReference, NamespaceInjector # 自动解引用所需要的库


class MongoDBUtil(object):
    @classmethod
    def __init__(cls):
        uri = 'mongodb://' + MONGODB_USERNAME + ':' + MONGODB_PWD + '@' + MONGODB_SERVER + ':' + MONGODB_PORT \
              + '/' + MONGODB_DB
        client = MongoClient(uri)
        cls.database = client.get_database(MONGODB_DB)
        database = client.get_database(MONGODB_DB)
        # 自动创建与解引用
        database.add_son_manipulator(NamespaceInjector())
        database.add_son_manipulator(AutoReference(database))
        cls.blogItemCollection = database.get_collection(MONGODB_BLOG_ITEM_COLLECTION)
        cls.authorItemCollection = database.get_collection(MONGODB_AUTHOR_ITEM_COLLECTION)

    @classmethod
    def get_blog(cls, title):
        blog = cls.blogItemCollection.find_one({'title': title})
        return blog

    @classmethod
    def save_blog(cls, authorItem, blogItem):
        authorCollection = cls.authorItemCollection
        author = authorCollection.find_one({"authorName": authorItem['authorName']})
        if author is None:
            # 作者信息尚未保持
            author = dict(authorItem)
            cls.save_author_item(author)
        blogItem['author'] = author
        blog = dict(blogItem)
        cls.save_blog_item(blog)

    @classmethod
    def save_blog_item(cls, item):
        """persistance the blog into mongodb"""
        result = cls.blogItemCollection.insert(item)
        log.msg("blog [%s] was saved into MongoDB" % item['title'], level=log.DEBUG)
        return result

    @classmethod
    def save_author_item(cls, item):
        """persistance the author into mongodb"""
        result = cls.authorItemCollection.insert(item)
        log.msg("author [%s] was saved into MongoDB" % item['authorName'], level=log.DEBUG)
        return result

    @classmethod
    def get_start_article_url(cls):
        """get the last article url from mongodb
            算法是随机选取当前文章中被赞数大于平均值的一个文章的url
        """
        # match = {'$group': {'_id': "$_id", 'vote': {'$max': "$vote"}}}
        # max = cls.blogItemCollection.aggregate([match])
        maxCursor = cls.blogItemCollection.find({}, {"vote": 1, '_id': 0}).sort('vote', -1).limit(1)
        maxVoteList = list(maxCursor)
        if maxVoteList.__len__() <= 0:
            # 数据库中尚未有数据
            log.msg("there isn't any article in mongodb", level=log.DEBUG)
            return None
        max = SON.to_dict(maxVoteList[0])['vote']
        avg = math.floor(cls.get_avg_vote())
        articlesCursor = cls.blogItemCollection.find({"vote": {'$lte': max, '$gte': avg}}, {"id": 1, "vote": 1, '_id': 0})\
            .sort('vote', -1).limit(3)
        articlesList = list(articlesCursor)
        index = randint(0, articlesList.__len__()-1)
        article = SON.to_dict(articlesList[index])
        return article['id']

    @classmethod
    def get_vote_avg(cls):
        avgCursor = cls.blogItemCollection.aggregate([{'$group': {'_id': '$source', 'avgVote': {'$avg': "$vote"}}}])
        avgList = list(avgCursor)
        avg = SON.to_dict(avgList[0])['avgVote']
        print avg

    @classmethod
    @deprecated
    def get_avg_vote(cls):
        """采用map-reduce方法计算monggodb中当前博文中被赞数量的平均值，
        但会有副作用会产生中间collection"""
        map = Code('''function() {
                       emit(this.source, this.vote);
                    }'''
                   )

        reduce = Code('''function(key,values){
                        var sum = 0
                        for (var i = 0; i < values.length; i++) {
                              sum += values[i];
                            }
                        return {source: key, avgVote: sum/values.length};
                        }'''
                      )
        cls.blogItemCollection.map_reduce(map, reduce, "avg")
        avg = cls.database.avg.find_one({}, {'value': 1, '_id': 0})
        return avg['value']['avgVote']

    @classmethod
    def isUrlScrawled(cls, url):
        """check if the url is saved in mongodb"""
        article = cls.blogItemCollection.find_one({"id": url}, {"id": 1, "_id": 0})
        if article is None:
            # 该url尚未被爬取
            log.msg("the article [%s] havn't been scrawled: " % url, level=log.DEBUG)
            return False
        else:
            # 该url已经被爬取过
            log.msg("the article [%s] was already scrawled: " % url, level=log.DEBUG)
            return True
