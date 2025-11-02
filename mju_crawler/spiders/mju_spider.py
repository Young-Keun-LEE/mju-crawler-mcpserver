import scrapy
import re

class MjuNoticeSpider(scrapy.Spider):
    name = "mju_notice"
    start_urls = [
        "https://www.mju.ac.kr/mjukr/255/subview.do"  # Notice page URL
    ]

    def parse(self, response):
        # Select all <a> elements inside <td class="_artclTdTitle">
        notice_links = response.css("td._artclTdTitle a")

        # Regex to match various date formats (e.g., YYYY-MM-DD or YYYY년 MM월 DD일)
        date_regex = re.compile(r"(\d{4}[-./]\d{1,2}[-./]\d{1,2})|\d{4}\s*년\s*\d{1,2}\s*월\s*\d{1,2}\s*일")

        for notice in notice_links:
            # Extract the title text
            title = notice.css("strong::text").get()
            if title:
                title = title.strip()
            else:
                title = notice.xpath("normalize-space(string(.))").get() or ""

            # Extract the hyperlink
            link = notice.attrib.get('href') or notice.css('::attr(href)').get()
            absolute_link = response.urljoin(link) if link else ""

            # --- Date extraction ---
            # Search for possible date patterns in nearby table cells
            tr = notice.xpath("ancestor::tr[1]")
            candidates = []

            # 1) Check adjacent <td> elements (next and next-next)
            for idx in (1, 2):
                texts = notice.xpath(f"ancestor::td[1]/following-sibling::td[{idx}]//text()").getall()
                candidates.extend([t.strip() for t in texts if t and t.strip()])

            # Also check the last <td> in the same row
            last_texts = notice.xpath("ancestor::td[1]/parent::tr/td[last()]//text()").getall()
            candidates.extend([t.strip() for t in last_texts if t and t.strip()])

            # 2) Fallback: all text within the same table row
            if not candidates:
                candidates = [t.strip() for t in tr.xpath('.//td//text()').getall() if t and t.strip()]

            # Match the first valid date pattern found
            found_date = ""
            for t in candidates:
                m = date_regex.search(t)
                if m:
                    found_date = m.group(0)
                    break
            
            # Yield the result only if a valid title and link are found
            if title and link:
                yield {
                    'title': title,
                    'link': absolute_link,
                    'date': found_date,
                }
