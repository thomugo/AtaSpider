# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from scrapy import signals
from scrapy.contrib.exporter import JsonLinesItemExporter, JsonItemExporter
from scrapy.exceptions import DropItem


# 过滤丢弃没有标题的Item
class AtablogPipeline(object):

    def process_item(self, item, spider):
        if item['title']:
            return item
        else:
            raise DropItem("Missing title in %s" % item)


class WriteJsonFilePipeline(object):
    def __init__(self):
        self.file = codecs.open('AtaBlogSpiderItems.json', 'w+b', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExportPipeline(object):
    __doc__ = '''
    将所有(从所有spider中)爬取到的item，存储到一个独立地 AtaBlogItems.json文件，每行包含一个序列化为JSON格式的item,
    JSON 是一个简单而有弹性的格式, 但对大量数据的扩展性不是很好，因为这里会将整个对象放入内存.
    如果你要JSON既强大又简单,可以考虑 JsonLinesItemExporter , 或把输出对象分为多个块.
    '''

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%sItems.json' % spider.name, 'a+')
        self.files[spider] = file
        self.exporter = JsonItemExporter(file, ensure_ascii=False)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class DuplicatesPipeline(object):
    __doc__ = '''item 去重'''

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item


# 性能太差
class JsonLinesExportPipeline(object):

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%sItems.json' % spider.name, 'w+b')
        self.files[spider] = file
        # 因为json.dumps 序列化时对中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii=False,否则将输出ascii编码
        self.exporter = JsonLinesItemExporter(file, ensure_ascii=False)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        #self.send_mail(item)
        return item

    def send_mail(self, item):
        # 爬取结束的时候发送邮件
        from scrapy.mail import MailSender
        mailer = MailSender(
            smtphost="smtp.163.com",  # 发送邮件的服务器
            mailfrom="thomugoO@163.com",  # 邮件发送者
            smtpuser="thomugoO@163.com",  # 用户名
            smtppass="haohao827774266",  # 发送邮箱的密码不是你注册时的密码，而是授权码！！！切记！
            smtpport=25  # 端口号
        )
        body = str(item)
        subject = item['title']
        #mailer.send(to=STATSMAILER_RCPTS, subject=subject.encode("utf-8"), body=body.encode("utf-8"))
        print "send succeed"
