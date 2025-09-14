import os
import asyncio
import threading
import time
import uuid
import sys
from fastmcp import FastMCP  # type: ignore
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_to_integrate import main as run_agent
from handleImage import analyze_image, categorize_product_with_anthropic

load_dotenv()

mcp = FastMCP("Kijiji Auto-Posting MCP Server")

jobs = {}
agent_running = False


def send_poke_notification(message: str):
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


def run_kijiji_posting_background(job_id: str, product_info: dict):
    global agent_running
    try:
        jobs[job_id]["status"] = "running"

        jobs[job_id]["started_at"] = time.time()
        agent_running = True

        async def post_to_kijiji():
            return await run_agent(product_info)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(post_to_kijiji())
        loop.close()

        jobs[job_id].update(
            {
                "status": "completed",
                "result": "Successfully posted to Kijiji",
                "product_info": product_info,
                "completed_at": time.time(),
            }
        )

        notification_message = f"This is a message from the Kijiji integration. The browser agent has finished posting the item and returned: {str(result)[:200]}... Alert the user now in your natural voice."
        send_poke_notification(notification_message)

        return result

    except Exception as e:
        jobs[job_id].update(
            {"status": "failed", "error": str(e), "completed_at": time.time()}
        )
    finally:
        agent_running = False


# @mcp.tool(description="Analyze image and post to Kijiji")
# def analyze_and_post_to_kijiji(image_data: str, image_media_type: str = "image/jpeg") -> dict:
def post_to_kijiji(title: str, description: str, price: str) -> dict:
    global agent_running, post_status

    if agent_running:
        return {
            "success": False,
            "error": "Agent already running",
            "message": "Please wait for the current posting to complete",
        }

    try:
        # product_info = analyze_image(image_data, image_media_type)
        # product_info = {
        #     "title": "sample product",
        #     "description": "sample description here",
        #     "price": price,
        #     "category": "Books",
        # }
        category = categorize_product_with_anthropic(title, description)
        product_info = {
            "title": title,
            "description": description,
            "price": price,
            "category": category,
        }

        job_id = str(uuid.uuid4())

        jobs[job_id] = {
            "product_info": product_info,
            "status": "queued",
            "created_at": time.time(),
        }

        thread = threading.Thread(
            target=run_kijiji_posting_background,
            args=(job_id, product_info),
            daemon=True,
        )
        thread.start()

        post_status = {
            "success": True,
            "message": "Image analyzed and agent started",
            "product_info": product_info,
            "job_id": job_id,
            "status": "queued",
        }
        return post_status

    except Exception as e:
        post_status = {
            "success": False,
            "error": f"Error processing image: {str(e)}",
        }
        return post_status


@mcp.tool(description="Check if conversation/agent is finished")
def conversation_finished() -> dict:
    global agent_running, post_status

    if post_status["status"] == "completed":
        return {
            "success": True,
            "message": "Conversation finished",
        }
    else:
        return {
            "success": False,
            "message": "Conversation not finished",
        }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    print(f"Starting Kijiji Auto-Posting MCP server on {host}:{port}")
    mcp.run(transport="http", host=host, port=port)
