# -*- coding: utf-8 -*-

# Scrapy settings for AtaBlog project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'AtaBlog'
BLOG_BASE_PATH = "./articles/"
SPIDER_MODULES = ['AtaBlog.spiders']
NEWSPIDER_MODULE = 'AtaBlog.spiders'

COOKIES_DEBUG = False
RETRY_ENABLED = False
REDIRECT_ENABLED = False

DEPTH_LIMIT = 0
DEPTH_PRIORITY = 0

CONCURRENT_ITEMS = 1000
CONCURRENT_REQUESTS = 100
#The maximum number of concurrent (ie. simultaneous) requests that will be performed to any single domain.
CONCURRENT_REQUESTS_PER_DOMAIN = 100
CONCURRENT_REQUESTS_PER_IP = 0
CONCURRENT_REQUESTS_PER_SPIDER = 100

DNSCACHE_ENABLED = True

DOWNLOAD_DELAY = 0.5
DOWNLOAD_TIMEOUT = 10

#feed export
# FEED_URI = "ftp://10.157.171.20/pub/scraping/feeds/AtaBlogItems.json"
# FEED_URI_PARAMS = None
# FEED_EXPORT_ENCODING = 'utf-8'
# FEED_FORMAT = 'jsonlines'
# FEED_STORE_EMPTY = False
# FEED_STORAGES = {
#     's3': None,
# }
# FEED_STORAGES_BASE = {
#     '': 'scrapy.extensions.feedexport.FileFeedStorage',
#     'file': 'scrapy.extensions.feedexport.FileFeedStorage',
#     'stdout': 'scrapy.extensions.feedexport.StdoutFeedStorage',
#     's3': 'scrapy.extensions.feedexport.S3FeedStorage',
#     'ftp': 'scrapy.extensions.feedexport.FTPFeedStorage',
# }
# FEED_EXPORTERS = {
#     'json': None,
#     'jsonlines': 'scrapy.exporters.JsonLinesItemExporter',
#     'jl': None,
#     'csv': None,
#     'xml': None,
#     'marshal': None,
#     'pickle': None,
# }
# FEED_EXPORTERS_BASE = {
#     'json': 'scrapy.exporters.JsonItemExporter',
#     'jsonlines': 'scrapy.exporters.JsonLinesItemExporter',
#     'jl': 'scrapy.exporters.JsonLinesItemExporter',
#     'csv': 'scrapy.exporters.CsvItemExporter',
#     'xml': 'scrapy.exporters.XmlItemExporter',
#     'marshal': 'scrapy.exporters.MarshalItemExporter',
#     'pickle': 'scrapy.exporters.PickleItemExporter',
# }

#pipelines
ITEM_PIPELINES = {
    'AtaBlog.pipelines.AtablogPipeline': 0,
    'AtaBlog.pipelines.DuplicatesPipeline': 1,
    #'AtaBlog.pipelines.WriteJsonFilePipeline': 2,
    #'AtaBlog.pipelines.JsonExportPipeline': 2,
    #'AtaBlog.pipelines.JsonLinesExportPipeline': 3,
}

MONGODB_SERVER = "10.157.171.20"
MONGODB_PORT = "27017"
MONGODB_DB = "ata"
MONGODB_BLOG_ITEM_COLLECTION = "blog"
MONGODB_AUTHOR_ITEM_COLLECTION = "author"
MONGODB_USERNAME = "ata"
MONGODB_PWD = "ata"

#mail
STATSMAILER_RCPTS = ['sx-zhangmh@dtdream.com']
MAIL_DEBUG = False
MAIL_HOST = 'localhost'
MAIL_PORT = 25
MAIL_FROM = 'scrapy@localhost'
MAIL_PASS = None
MAIL_USER = None
MAIL_TLS = False
MAIL_SSL = False

DOWNLOADER_MIDDLEWARES = {
    ##'zhihu.misc.middleware.CustomHttpProxyMiddleware': 80,
    #'zhihu.misc.middleware.CustomUserAgentMiddleware': 81,
}

SCHEDULER_ORDER = 'BFO'

HEADER = {
    ":authority": "www.atatech.org",
    ":method": "GET",
    ":path": "/articles/75950",
    ":scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, sdch, br",
    "accept-language": "zh-CN,zh;q=0.8",
    "cache-control": "max-age=0",
    "referer": "https://www.atatech.org/teams/15",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}

COOKIES_ENABLED = True
REDIRECT_ENABLED = True

COOKIES = {
    "ATASESSION": r"0d3d9a28cf39a34956882797a04e1c73",
    "UM_distinctid": r"15b043f66df955-0d6fa807830bc8-5e4f2b18-1fa400-15b043f66e0a5d",
    "CNZZDATA1254194462": r"881952546-1490422737-https%253A%252F%252Flogin.alibaba-inc.com%252F%7C1490938483",
    "weigf": r"1cefz4kFhNfHXb0q8j9lT6n%2BziRrHrSQSRXaHl4KrN5ruUg",
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'AtaBlog (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'AtaBlog.middlewares.AtablogSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'AtaBlog.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'AtaBlog.pipelines.AtablogPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
