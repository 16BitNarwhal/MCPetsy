import os
import asyncio
import threading
import time
import uuid
from fastmcp import FastMCP  # type: ignore
from dotenv import load_dotenv
from browser_use import Agent, ChatAnthropic

# Load environment variables
load_dotenv()

mcp = FastMCP("Sample MCP Server with Browser Automation")

# Simple in-memory job store for background tasks
jobs = {}


def run_browser_search_background(job_id: str, query: str):
    """Run browser automation in background thread"""
    try:
        jobs[job_id]["status"] = "running"
        jobs[job_id]["started_at"] = time.time()

        # Run browser automation
        async def search():
            llm = ChatAnthropic(model="claude-3-5-haiku-latest", temperature=0.0)
            task = f"Search Google for '{query}' and tell me what the top result is (include the title and the URL)"

            # Configure for production environment
            if os.environ.get("ENVIRONMENT") == "production":
                agent = Agent(task=task, llm=llm, browser="chrome", headless=True)
            else:
                agent = Agent(task=task, llm=llm)

            return await agent.run()

        # Run in new event loop (background thread)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(search())
        loop.close()

        # Store successful result
        jobs[job_id].update(
            {"status": "completed", "result": str(result), "completed_at": time.time()}
        )

    except Exception as e:
        # Store error result
        jobs[job_id].update(
            {"status": "failed", "error": str(e), "completed_at": time.time()}
        )


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


@mcp.tool(description="Start a background browser search and return job ID")
def search_web(query: str) -> dict:
    """
    Start a browser automation search in the background.
    Returns immediately with a job ID that can be polled for results.

    Args:
        query: The search term to look for

    Returns:
        dict: Contains job ID and polling instructions
    """
    # Generate unique job ID
    job_id = str(uuid.uuid4())

    # Initialize job in store
    jobs[job_id] = {"query": query, "status": "queued", "created_at": time.time()}

    # Start background thread for browser automation
    thread = threading.Thread(
        target=run_browser_search_background, args=(job_id, query), daemon=True
    )
    thread.start()

    return {
        "job_id": job_id,
        "query": query,
        "status": "queued",
        "message": "Browser search started in background",
        "instructions": "Use get_search_status tool to check progress",
    }


@mcp.tool(description="Check the status of a background browser search")
def get_search_status(job_id: str) -> dict:
    """
    Check the status of a background browser search job.

    Args:
        job_id: The job ID returned from search_web

    Returns:
        dict: Contains job status and results if completed
    """
    if job_id not in jobs:
        return {"job_id": job_id, "status": "not_found", "error": "Job ID not found"}

    job = jobs[job_id]
    response = {
        "job_id": job_id,
        "query": job["query"],
        "status": job["status"],
        "created_at": job["created_at"],
    }

    if job["status"] == "running":
        response["message"] = "Browser automation in progress..."
        if "started_at" in job:
            response["running_for"] = f"{int(time.time() - job['started_at'])} seconds"

    elif job["status"] == "completed":
        response.update(
            {
                "result": job["result"],
                "completed_at": job["completed_at"],
                "total_time": f"{int(job['completed_at'] - job['created_at'])} seconds",
                "message": "Browser search completed successfully",
            }
        )

    elif job["status"] == "failed":
        response.update(
            {
                "error": job["error"],
                "completed_at": job["completed_at"],
                "total_time": f"{int(job['completed_at'] - job['created_at'])} seconds",
                "message": "Browser search failed",
            }
        )

    return response


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
