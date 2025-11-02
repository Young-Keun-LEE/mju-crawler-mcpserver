# -*- coding: utf-8 -*-

# Scrapy settings for the mju_crawler project

# 1. Define the Scrapy bot name and the module locations. (Required)
BOT_NAME = 'mju_crawler'
SPIDER_MODULES = ['mju_crawler.spiders']
NEWSPIDER_MODULE = 'mju_crawler.spiders'

# 2. User-Agent setting to avoid being blocked by Myongji University server. (Most important)
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'

# 3. Follow the rules set in robots.txt. (Recommended)
ROBOTSTXT_OBEY = True

# 4. Ensure proper UTF-8 encoding to prevent Korean characters from breaking when exporting results (e.g., JSON files). (Required)
FEED_EXPORT_ENCODING = "utf-8"

# 5. Compatibility setting for future Scrapy versions. (Recommended)
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"

