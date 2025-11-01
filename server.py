import sys
# Twisted Reactor 설치 코드는 이제 Scrapy를 직접 실행하므로 필요 없습니다.
# 이 코드는 그대로 두어도 무방하지만, 삭제해도 됩니다.
if sys.platform == 'win32':
    from twisted.internet import iocpreactor
    iocpreactor.install()
else:
    from twisted.internet import asyncioreactor
    asyncioreactor.install()

import subprocess
import json
import os
from typing import List, Dict
from pathlib import Path
from crochet import setup, wait_for
from mcp.server.fastmcp import FastMCP
from smithery.decorators import smithery

# crochet 초기 설정
setup()

# @wait_for는 subprocess.run 이라는 동기적(blocking) 코드를
# Smithery의 비동기 환경에서 안전하게 실행할 수 있도록 해줍니다.
@wait_for(timeout=60.0) # 프로세스 실행 시간이 길 수 있으므로 타임아웃을 60초로 늘립니다.
def _run_scrapy_command() -> List[Dict]:
    """
    터미널에서 'uv run scrapy crawl' 명령어를 직접 실행하고,
    결과 JSON 파일을 읽어 내용을 반환합니다.
    """
    spider_name = "mju_notice"
    output_filename = "notices_output.json"
    output_path = Path(output_filename)

    # 이전에 생성된 결과 파일이 있다면 삭제
    if output_path.exists():
        output_path.unlink()

    # 실행할 터미널 명령어
    command = [
        "uv", "run", "scrapy", "crawl", spider_name,
        "-o", output_filename
    ]

    print(f"명령어 실행: {' '.join(command)}")
    
    # 자식 프로세스로 명령어 실행
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')

    # 명령어 실행 실패 시 에러 로그 출력
    if result.returncode != 0:
        print("[ERROR] Scrapy crawl 명령어 실행 실패:")
        print(result.stderr)
        # 에러가 발생하면 빈 리스트를 반환하여 'no notices found'가 되도록 함
        return []

    # 결과 파일이 생성되었는지 확인
    if not output_path.exists():
        print("[ERROR] 크롤링은 성공했으나 결과 파일이 생성되지 않았습니다.")
        return []
    
    # 결과 파일을 읽어서 notices 변수에 저장
    with open(output_path, 'r', encoding='utf-8') as f:
        notices = json.load(f)
    
    # 사용이 끝난 임시 파일 삭제
    output_path.unlink()

    return notices


@smithery.server()
def create_server():
    server = FastMCP("mju_notice_bot")

    @server.tool()
    def get_mju_notices(limit: int = 5) -> List[Dict]:
        print(f"-> Tool 'get_mju_notices' called with limit={limit}")
        try:
            # 이제 이 함수는 'scrapy crawl'을 직접 실행하고 그 결과를 받습니다.
            all_notices = _run_scrapy_command()
            
            if not all_notices:
                return [{"error": "Crawl completed, but no notices were found."}]

            return all_notices[:limit]
        except Exception as e:
            print(f"[ERROR] in get_mju_notices: {e}")
            return [{"error": f"An unexpected error or timeout occurred during the crawl: {str(e)}"}]

    return server