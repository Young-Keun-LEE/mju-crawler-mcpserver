import subprocess
import json
from typing import List, Dict
from pathlib import Path
from crochet import setup, wait_for
from mcp.server.fastmcp import FastMCP
from smithery.decorators import smithery

"""Server for crawling Myongji University notices
using Scrapy and exposing them as a Smithery tool."""

# Initialize Crochet
setup()

# @wait_for allows synchronous (blocking) code such as subprocess.run
# to safely execute in Smithery’s asynchronous environment.
@wait_for(timeout=60.0)  # Increase timeout to 60 seconds since crawling may take longer.
def _run_scrapy_command() -> List[Dict]:
    """
    Executes the 'uv run scrapy crawl' command in a subprocess
    and reads the generated JSON output file.
    """
    spider_name = "mju_notice"
    output_filename = "notices_output.json"
    output_path = Path(output_filename)

    # Remove any existing output file from previous runs
    if output_path.exists():
        output_path.unlink()

    # Command to execute
    command = [
        "uv", "run", "scrapy", "crawl", spider_name,
        "-o", output_filename
    ]

    print(f"Running command: {' '.join(command)}")
    
    # Run the command as a subprocess
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')

    # Log errors if the command fails
    if result.returncode != 0:
        print("[ERROR] Failed to execute 'scrapy crawl' command:")
        print(result.stderr)
        # Return an empty list to indicate "no notices found"
        return []

    # Verify the output file was successfully created
    if not output_path.exists():
        print("[ERROR] Crawling succeeded but the output file was not created.")
        return []
    
    # Read the output file into the 'notices' variable
    with open(output_path, 'r', encoding='utf-8') as f:
        notices = json.load(f)
    
    # Remove the temporary file after use
    output_path.unlink()

    return notices


@smithery.server()
def create_server():
    server = FastMCP("mju_notice_bot")

    @server.tool()
    def get_mju_notices(limit: int = 5) -> List[Dict]:
        print(f"-> Tool 'get_mju_notices' called with limit={limit}")
        try:
            # Run the Scrapy crawl command and retrieve the results
            all_notices = _run_scrapy_command()
            
            if not all_notices:
                return [{"error": "Crawl completed, but no notices were found."}]

            return all_notices[:limit]
        except Exception as e:
            print(f"[ERROR] in get_mju_notices: {e}")
            return [{"error": f"An unexpected error or timeout occurred during the crawl: {str(e)}"}]

    return server
