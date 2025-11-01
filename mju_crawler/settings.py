# -*- coding: utf-8 -*-

# Scrapy settings for mju_crawler project

# 1. Scrapy 봇의 이름과 모듈 위치를 정의합니다. (필수)
BOT_NAME = 'mju_crawler'
SPIDER_MODULES = ['mju_crawler.spiders']
NEWSPIDER_MODULE = 'mju_crawler.spiders'

# 2. 명지대 서버 차단을 피하기 위한 User-Agent 설정 (가장 중요)
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'

# 3. robots.txt 규칙을 준수하도록 설정합니다. (권장)
ROBOTSTXT_OBEY = True

# 4. JSON 파일 등으로 결과를 출력할 때 한글이 깨지지 않도록 인코딩을 설정합니다. (필수)
FEED_EXPORT_ENCODING = "utf-8"

# 5. Scrapy의 향후 버전을 위한 호환성 설정 (권장)
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"

# ※※※ 주의: TWISTED_REACTOR 설정은 여기서 반드시 제거해야 합니다. ※※※
# 이 설정은 server.py의 asyncio 환경과 충돌을 일으킬 수 있습니다.
# scrapy crawl 명령어는 이 설정 없이도 리눅스 환경에서 잘 동작합니다.