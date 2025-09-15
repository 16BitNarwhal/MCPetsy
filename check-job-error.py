#!/usr/bin/env python3
import asyncio
from fastmcp import Client


async def check_error():
    client = Client("https://fastmcp-server-wf77.onrender.com/mcp")

    async with client:
        # Start a job to get a fresh error
        job_result = await client.call_tool("search_web", {"query": "test"})
        job_id = job_result.data["job_id"]
        print(f"Started job: {job_id}")

        # Wait and check error
        await asyncio.sleep(15)
        status_result = await client.call_tool("get_search_status", {"job_id": job_id})
        status = status_result.data

        print(f"Status: {status['status']}")
        if "error" in status:
            print(f"Error details: {status['error']}")


if __name__ == "__main__":
    asyncio.run(check_error())
