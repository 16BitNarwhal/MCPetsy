import os
import asyncio
from fastmcp import FastMCP # type: ignore
from dotenv import load_dotenv

# Optional browser automation import
try:
    from browser_use import Agent, ChatAnthropic
    BROWSER_AVAILABLE = True
except ImportError:
    BROWSER_AVAILABLE = False
    Agent = None
    ChatAnthropic = None

# Load environment variables
load_dotenv()

mcp = FastMCP("Sample MCP Server with Browser Automation")


@mcp.tool(description="Greet a user by name with a welcome message from the MCP server")
def greet(name: str) -> str:
    return f"Hello, {name}! Welcome to our sample MCP server running on Heroku!"


@mcp.tool(
    description="Get information about the MCP server including name, version, environment, and Python version"
)
def get_server_info() -> dict:
    return {
        "server_name": "Sample MCP Server with Browser Automation",
        "version": "1.0.0",
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "python_version": os.sys.version.split()[0],
        "browser_automation": "enabled",
    }


@mcp.tool(
    description="Search for a query using browser automation and return the top result"
)
async def search_web(query: str) -> dict:
    """
    Search for a query using browser automation and return the top search result.

    Args:
        query: The search term to look for

    Returns:
        dict: Contains information about the search result
    """
    try:
        llm = ChatAnthropic(model="claude-3-5-haiku-latest", temperature=0.0)
        task = f"Search Google for '{query}' and tell me what the top result is (include the title and the URL)"
        agent = Agent(task=task, llm=llm)

        # Run the browser automation
        result = await asyncio.wait_for(agent.run(), timeout=60.0)

        return {
            "query": query,
            "result": str(result),
            "status": "success",
            "message": f"Browser search completed for: {query}",
        }

    except asyncio.TimeoutError:
        return {
            "query": query,
            "error": "Browser automation timed out - search took too long",
            "status": "timeout",
            "message": f"Search for '{query}' exceeded 60 seconds",
        }
    except Exception as e:
        return {
            "query": query,
            "error": str(e),
            "status": "error",
            "message": f"Browser automation failed for: {query}",
        }


# @mcp.tool(description="Get information about browser automation capabilities")
# def get_browser_capabilities() -> dict:
#     """
#     Get information about the browser automation setup and capabilities.

#     Returns:
#         dict: Information about browser automation status and available features
#     """
#     return {
#         "browser_automation": "Browser Use with Claude Haiku",
#         "capabilities": [
#             "Web search and result extraction",
#             "Form filling and interaction",
#             "Content scraping",
#             "Navigation and clicking",
#             "Screenshot capture",
#         ],
#         "model": "claude-3-5-haiku-latest",
#         "status": "ready",
#         "anthropic_api_configured": bool(os.environ.get("ANTHROPIC_API_KEY")),
#     }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    print(f"Starting FastMCP server on {host}:{port}")
    mcp.run(transport="http", host=host, port=port)
