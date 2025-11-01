import scrapy
import re
from pathlib import Path # ★★★ 디버깅을 위해 pathlib를 임포트합니다.

class MjuNoticeSpider(scrapy.Spider):
    name = "mju_notice"
    start_urls = [
        "https://www.mju.ac.kr/mjukr/255/subview.do"
    ]

    def parse(self, response):
        # ★★★ 여기가 가장 중요합니다: 스파이더가 받은 HTML 응답을 파일로 저장합니다. ★★★
        # 이 파일의 내용을 보면 서버가 진짜 공지사항 페이지를 줬는지, 아니면 차단 페이지를 줬는지 알 수 있습니다.
        output_filename = "response_from_spider.html"
        Path(output_filename).write_bytes(response.body)
        self.log(f"응답 내용을 '{output_filename}' 파일에 저장했습니다. 이 파일을 확인하세요.")
        # ★★★ 디버깅 코드 끝 ★★★

        # ---- 아래는 제공해주신 기존의 좋은 로직을 그대로 유지합니다. ----

        # 제목 셀 안의 <a> 요소들을 선택합니다.
        notice_links = response.css("td._artclTdTitle a")

        date_regex = re.compile(r"(\d{4}[-./]\d{1,2}[-./]\d{1,2})|\d{4}\s*년\s*\d{1,2}\s*월\s*\d{1,2}\s*일")

        for notice in notice_links:
            # 제목 안전 추출
            title = notice.css("strong::text").get()
            if title:
                title = title.strip()
            else:
                title = notice.xpath("normalize-space(string(.))").get() or ""

            # 링크 추출
            link = notice.attrib.get('href') or notice.css('::attr(href)').get()
            absolute_link = response.urljoin(link) if link else ""

            # 날짜 추출: 여러 후보 텍스트에서 날짜 패턴을 찾음
            tr = notice.xpath("ancestor::tr[1]")
            candidates = []

            # 1) 바로 옆 td들 (다음 td, 다음다음 td, 마지막 td)
            for idx in (1, 2):
                texts = notice.xpath(f"ancestor::td[1]/following-sibling::td[{idx}]//text()").getall()
                candidates.extend([t.strip() for t in texts if t and t.strip()])
            last_texts = notice.xpath("ancestor::td[1]/parent::tr/td[last()]//text()").getall()
            candidates.extend([t.strip() for t in last_texts if t and t.strip()])

            # 2) fallback: tr 내부 모든 텍스트
            if not candidates:
                candidates = [t.strip() for t in tr.xpath('.//td//text()').getall() if t and t.strip()]

            found_date = ""
            for t in candidates:
                m = date_regex.search(t)
                if m:
                    found_date = m.group(0)
                    break
            
            # 유효한 제목이 있을 때만 데이터를 yield 합니다.
            if title and link:
                yield {
                    'title': title,
                    'link': absolute_link,
                    'date': found_date,
                }