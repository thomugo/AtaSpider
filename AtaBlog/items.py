# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AtablogItem(scrapy.Item):
    # define the fields for your item here like:
    # 博客来源
    source = scrapy.Field()
    # 文章标识
    id = scrapy.Field()
    # 文章内容
    blog = scrapy.Field()
    # 文章路径
    dir = scrapy.Field()
    # 文章标题
    title = scrapy.Field()
    # 文章分类
    tags = scrapy.Field()
    # 收藏数量
    mark = scrapy.Field()
    # 点赞数
    vote = scrapy.Field()
    # 作者
    author = scrapy.Field()


class AuthorItem(scrapy.Item):
    # 文章作者
    authorName = scrapy.Field()
    # 作者主页
    authorHomePage = scrapy.Field()
