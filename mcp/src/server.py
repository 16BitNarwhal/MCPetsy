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


async def send_poke_notification(message: str):
    """Send notification via Poke API when browser automation completes"""
    try:
        import requests

        poke_api_key = os.environ.get("POKE_API_KEY")
        if not poke_api_key:
            print("⚠️ No POKE_API_KEY found - skipping notification")
            return

        response = requests.post(
            "https://poke.com/api/v1/inbound-sms/webhook",
            headers={
                "Authorization": f"Bearer {poke_api_key}",
                "Content-Type": "application/json",
            },
            json={"message": message},
        )

        if response.ok:
            print(f"✅ Poke notification sent: {message[:100]}...")
        else:
            print(f"❌ Poke notification failed: {response.status_code}")

    except Exception as e:
        print(f"❌ Error sending Poke notification: {e}")


def run_browser_search_background(job_id: str, query: str):
    """Run browser automation in background thread and notify via Poke when done"""
    try:
        jobs[job_id]["status"] = "running"
        jobs[job_id]["started_at"] = time.time()

        # Run browser automation
        async def search():
            llm = ChatAnthropic(model="claude-sonnet-4-0", temperature=0.0)
            task = f"Go to kijiji.ca, search for '{query}', and tell me what the top result is (include the title and the URL to the listing)."

            # Simple agent - Docker handles all browser setup
            agent = Agent(task=task, llm=llm)
            result = await asyncio.wait_for(
                agent.run(), timeout=180.0
            )  # 3 minute timeout

            # Store successful result
            jobs[job_id].update(
                {
                    "status": "completed",
                    "result": str(result),
                    "completed_at": time.time(),
                }
            )

            # Send Poke notification with result
            notification_message = f"This is a message from the Kijiji integration. The browser agent has finished searching for '{query}' and returned: {str(result)[:200]}... Alert the user now in your natural voice."
            await send_poke_notification(notification_message)

            return result

        # Run in new event loop (background thread)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(search())
        loop.close()

    except asyncio.TimeoutError:
        # Handle timeout specifically
        jobs[job_id].update(
            {
                "status": "failed",
                "error": "Kijiji search timed out after 3 minutes",
                "completed_at": time.time(),
            }
        )

        # Send timeout notification
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        timeout_message = f"This is a message from the Kijiji integration. The browser agent timed out while searching for '{query}' (took longer than 3 minutes). Alert the user about this timeout in your natural voice."
        loop.run_until_complete(send_poke_notification(timeout_message))
        loop.close()

    except Exception as e:
        # Store error result and notify
        jobs[job_id].update(
            {"status": "failed", "error": str(e), "completed_at": time.time()}
        )

        # Send Poke notification about failure
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        error_message = f"This is a message from the Kijiji integration. The browser agent failed while searching for '{query}'. Error: {str(e)}. Alert the user about this failure in your natural voice."
        loop.run_until_complete(send_poke_notification(error_message))
        loop.close()


@mcp.tool(description="Greet a user by name with a welcome message from the MCP server")
def greet(name: str) -> str:
    print(f"Greeting {name}")
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


@mcp.tool(description="Start a Kijiji search and get notified via Poke when complete")
def search_kijiji(query: str) -> dict:
    """
    Start a Kijiji search in the background.
    Returns immediately and sends results via Poke API when complete.

    Args:
        query: The search term to look for on Kijiji

    Returns:
        dict: Immediate response confirming search started
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
        "query": query,
        "status": "working_on_it",
        "message": f"🔍 Working on it now! Starting Kijiji search for '{query}'...",
        "notification": "You'll get a Poke notification when the search completes with results!",
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
    mcp.run(transport="http", host=host, port=port, stateless_http=True)
