#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import codecs
import sys
import os
import html2text
import Queue
from AtaBlog.items import *
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from AtaBlog.settings import *
from AtaBlog.MongoDBUtil import MongoDBUtil

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


class AtaBlogSpider(scrapy.Spider):
    # url 连接池采用优先级队列，上篇博文优先级最高, 下篇其次，相关博文优先级最低
    name = "AtaBlogSpider"
    download_delay = 4
    allowed_domains = ["atatech.org"]
    basePath = BLOG_BASE_PATH
    url_pools = Queue.PriorityQueue()
    used_urls = []
    rules = (
        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=('item\.html',))),
    )

    def __init__(self):
        self.source = "www.atatech.org"
        self.user_names = []
        self.headers = HEADER
        self.cookies = COOKIES
        self.url_pools.put((1, "https://www.atatech.org/articles/72373"))
        MongoDBUtil.__init__()
        startUrl = MongoDBUtil.get_start_article_url()
        if startUrl is not None:
            startUrl = "https://www.atatech.org/articles/" + startUrl
            self.url_pools.get()
            self.url_pools.put((1, startUrl))

    def start_requests(self):
        yield scrapy.Request(self.url_pools.get()[1], cookies=self.cookies, headers=self.headers)

    # 格式化text，去除空白符
    def stripList(self, list):
        list = map(lambda x: x.strip(), list)
        while '' in list:
            list.remove('')
        return list

    # 提取同类文章url
    def parse_similar_articles(self, response):
        print "in parse_similar_articles"
        context = response.xpath('//table').extract()[0].decode('utf-8')
        urls = response.xpath('//a[contains(@href, "/articles")]/@href').extract()
        for url in urls:
            self.log("similar url: " + response.urljoin(url))
            self.url_pools.put((3, response.urljoin(url)))
        while self.url_pools.qsize() > 0:
            url = self.url_pools.get()[1]
            uri = url.split('/')[-1]
            if url not in self.used_urls:
                if (not MongoDBUtil.isUrlScrawled(uri)):
                    print "crawl next url: " + url
                    yield scrapy.Request(url, cookies=self.cookies, headers=self.headers)
                    break
        yield response.meta['item']


    # 提取文章上下页url
    def getUrls(self, item, response):
        selfUrl = response.url
        previousArticle = response.xpath('//li[@class="previous cnzz_block"]//a/@href').extract()
        nextArticle = response.xpath('//li[@class="next cnzz_block"]//a/@href').extract()
        if len(previousArticle) > 0:
            previousArticleUrl = response.urljoin(previousArticle[0])
            self.url_pools.put((1, previousArticleUrl))
            self.log("Get a previousUrl: %s from [%s]" % (previousArticleUrl, selfUrl))
        if len(nextArticle) > 0:
            nextArticleUrl = response.urljoin(nextArticle[0])
            self.url_pools.put((2, nextArticleUrl))
            self.log("Get a nextUrl: %s from [%s]" % (nextArticleUrl, selfUrl))
        similarArticle = response.xpath('//div[re:test(@js-load-url, "/similar$")]//@js-load-url').extract()[0]
        similarArticleUrl = response.urljoin(similarArticle)
        self.log("similarArticleUrl: [%s]" % similarArticleUrl)
        request = scrapy.Request(similarArticleUrl, callback=self.parse_similar_articles)
        request.meta['item'] = item
        return request

    def parse(self, response):
        url = response.url
        print "parse article: [%s]" % url
        title = response.xpath('//title/text()').extract()[0]
        print title
        if title != " 404 NOT FOUND ":
            # 解析文章
            # self.write2file("articles", context[0].decode('utf-8'))
            item = self.parse_page_contents(response)
            self.used_urls.append(url)
            yield self.getUrls(item, response)
        else:
            self.log("article: [%s] not exist!!!" % response.url)
            while self.url_pools.qsize() > 0:
                url = self.url_pools.get()[1]
                uri = url.split('/')[-1]
                if url not in self.used_urls:
                    if(not MongoDBUtil.isUrlScrawled(uri)):
                        print "crawl next url: " + url
                        yield scrapy.Request(url, cookies=self.cookies, headers=self.headers)
                        break
        while self.url_pools.qsize() > 0:
            url = self.url_pools.get()[1]
            uri = url.split('/')[-1]
            if url not in self.used_urls:
                if (not MongoDBUtil.isUrlScrawled(uri)):
                    print "crawl next url: " + url
                    yield scrapy.Request(url, cookies=self.cookies, headers=self.headers)
                    break

    # 解析文章内容
    def parse_page_contents(self, response):
        self.log("parse contents from %s " % response.url)
        blogItem = AtablogItem()
        blogItem['source'] = self.source
        authorItem = AuthorItem()
        authorName = response.xpath('//a[@class="info"]//@title').extract()[0].decode('utf-8')
        self.log("authorName: " + authorName)
        authorItem['authorName'] = authorName
        authorHomePage = response.xpath('//a[@class="info"]//@href').extract()[0]
        authorHomeUrl = response.urljoin(authorHomePage)
        self.log("authorHomePage: " + authorHomeUrl)
        authorItem['authorHomePage'] = authorHomeUrl
        blogItem['tags'] = response.xpath('//div[@class="form-group"]//@value').extract()[0].split()
        dir = response.xpath('//span[@class="info"]//a[contains(@href, "teams")]//text()').extract()
        articlePath = self.basePath
        if len(dir) > 0:
            for dirName in dir:
                articlePath = articlePath + dirName.decode('utf-8') + "/"
        elif len(blogItem['tags']) > 0:
            articlePath = articlePath + blogItem['tags'][0].decode('utf-8') + "/"
        else:
            articlePath = articlePath + authorItem['authorName'] + "/"
        blogItem['dir'] = articlePath
        self.log("articlePath: " + articlePath)
        blogItem['title'] = response.xpath('//title/text()').extract()[0]
        self.log("Blog title: " + blogItem['title'].decode('utf-8'))
        id = response.xpath('//a[re:test(@href, "/mark$")]//@href').extract()[0]
        blogItem['id'] = id.split('/')[-2]
        self.log("id: " + blogItem['id'])
        mark = response.xpath('//a[re:test(@href, "/mark$")]//text()').extract()
        blogItem['mark'] = int(self.stripList(mark)[0])
        vote = response.xpath('//a[re:test(@href, "/voteup$")]//text()').extract()
        blogItem['vote'] = int(self.stripList(vote)[0])
        article = response.xpath('//div[@class="content unsafe"]').extract()[0]
        html2textHandler = html2text.HTML2Text()
        html2textHandler.ignore_links = True
        blogContent = html2textHandler.handle(article.decode('utf-8'))
        blogItem['blog'] = blogContent
        self.persistenceBlog(authorItem, blogItem)
        return blogItem

    # 将文章持久化到本地和数据库中
    def persistenceBlog(self, authorItem, blogItem):
        uri = blogItem['id']
        if not os.path.exists(blogItem['dir']):
            os.makedirs(blogItem['dir'])
        fileName = blogItem['dir'] + blogItem['title'] + ".md"
        alreadyWritten = os.path.exists(fileName)
        alreadyScrawled = MongoDBUtil.isUrlScrawled(uri)
        if not alreadyWritten:
            # 将爬取到的文章保存到本地文件系统
            with codecs.open(fileName, 'wb', encoding="utf-8") as md:
                md.write(blogItem['blog'])
        if not alreadyScrawled:
            # 将解析到的article保存到数据库
            MongoDBUtil.save_blog(authorItem, blogItem)

    def write2file(self, filename, context):
        si = codecs.open(filename, "wb", encoding="utf-8")
        si.writelines(context)
        si.close()

    # def closed(self, reason):
    #     # 爬取结束的时候发送邮件
    #     from scrapy.mail import MailSender
    #     mailer = MailSender(
    #         smtphost="smtp.163.com",  # 发送邮件的服务器
    #         mailfrom="thomugoO@163.com",  # 邮件发送者
    #         smtpuser="thomugoO@163.com",  # 用户名
    #         smtppass="haohao827774266",  # 发送邮箱的密码不是你注册时的密码，而是授权码！！！切记！
    #         smtpport=25  # 端口号
    #     )
    #     body = u"""
    #     AtaBlog Test
    #     """
    #     subject = u'AtaBlog'
    #     mailer.send(to=STATSMAILER_RCPTS, subject=subject.encode("utf-8"), body=body.encode("utf-8"))
    #     print "send succeed"

