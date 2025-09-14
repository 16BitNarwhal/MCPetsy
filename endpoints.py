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
from handleImage import analyze_image

load_dotenv()

mcp = FastMCP("Kijiji Auto-Posting MCP Server")

jobs = {}
agent_running = False

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
                "completed_at": time.time()
            }
        )

    except Exception as e:
        jobs[job_id].update(
            {
                "status": "failed", 
                "error": str(e), 
                "completed_at": time.time()
            }
        )
    finally:
        agent_running = False

@mcp.tool(description="Analyze image and post to Kijiji")
def analyze_and_post_to_kijiji(image_data: str, image_media_type: str = "image/jpeg") -> dict:
    global agent_running
    
    if agent_running:
        return {
            "success": False,
            "error": "Agent already running",
            "message": "Please wait for the current posting to complete"
        }
    
    try:
        product_info = analyze_image(image_data, image_media_type)
        
        job_id = str(uuid.uuid4())
        
        jobs[job_id] = {
            "product_info": product_info, 
            "status": "queued", 
            "created_at": time.time()
        }
        
        thread = threading.Thread(
            target=run_kijiji_posting_background, 
            args=(job_id, product_info), 
            daemon=True
        )
        thread.start()
        
        return {
            "success": True,
            "message": "Image analyzed and agent started",
            "product_info": product_info,
            "job_id": job_id,
            "status": "queued"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error processing image: {str(e)}"
        }

@mcp.tool(description="Mark conversation as finished")
def conversation_finished() -> dict:
    global agent_running
    
    agent_running = False
    return {
        "success": True,
        "message": "Conversation finished"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    print(f"Starting Kijiji Auto-Posting MCP server on {host}:{port}")
    mcp.run(transport="http", host=host, port=port)