# Myongji University Notice Bot (MCP Server)

This project is an AI-powered tool server built with [Smithery](https://smithery.app/) and [MCP (Model-Context-Protocol)](https://docs.mcp.dev/) that provides real-time access to the latest notices from Myongji University's official website.

The server exposes a tool that can be called by AI agents or language models to fetch and display university announcements directly within a chat interface or other applications.

## ✨ Features

- **Real-time Notice Fetching**: Uses a Scrapy spider to crawl the official Myongji University notice board (`mju.ac.kr`) in real-time.
- **AI Tool Integration**: Exposes a `get_mju_notices` tool that AI agents can naturally call in response to user prompts like "What are the latest announcements from Myongji University?".
- **Robust and Asynchronous**: Built on a modern Python stack, leveraging `asyncio`, `crochet`, and `subprocess` to handle web crawling without blocking the main server loop.
- **Configurable**: The number of notices to retrieve can be specified with a `limit` parameter.

## 🛠️ How It Works

1.  An AI agent receives a user request for Myongji University notices.
2.  The agent identifies the `get_mju_notices` tool as the best way to fulfill the request.
3.  The Smithery MCP server executes the tool.
4.  The tool runs a Python `subprocess` to invoke a dedicated Scrapy spider.
5.  The Scrapy spider crawls the university's notice page, scrapes the announcements (title, link, date), and outputs the data as JSON.
6.  The tool reads the JSON output, formats it, and returns the list of notices to the AI agent.
7.  The AI agent presents the information to the user in a natural, conversational format.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- `uv` (or `pip`) for package management
- Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/<your-username>/mju-notice-mcpserver.git
    cd mju-notice-mcpserver
    ```

2.  **Create a virtual environment:**
    ```bash
    uv venv
    ```

3.  **Install dependencies in editable mode:**
    This command reads the `pyproject.toml` file and installs all necessary packages, including the local `mju_crawler` package.
    ```bash
    uv pip install -e .
    ```

### Running the Server

-   **Run the interactive playground:**
    This is the best way to test the tool. It starts the server and opens a web UI where you can chat with an AI agent that can use your tool.
    ```bash
    uv run playground
    ```

-   **Run in development mode:**
    To run the server and have it listen for requests from other MCP clients:
    ```bash
    uv run dev
    ```

### Example Usage (in Playground)

Once the playground is running, you can ask the AI agent things like:

> "Show me the 3 latest notices from Myongji University."

> "명지대학교 최신 공지사항 알려줘"

The agent will then call the `get_mju_notices` tool and display the results.```