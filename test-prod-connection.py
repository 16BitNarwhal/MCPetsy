#!/usr/bin/env python3
import asyncio
from fastmcp import Client


async def test_production_server():
    print("🧪 Testing production MCP server connection...")

    try:
        client = Client("https://fastmcp-server-wf77.onrender.com/mcp")

        async with client:
            print("✅ Connected successfully!")

            # List tools
            tools = await client.list_tools()
            print(f"📋 Available tools: {[tool.name for tool in tools]}")

            # Test background job pattern
            print("\n🔍 Testing background search...")
            job_result = await client.call_tool("search_web", {"query": "AI music"})
            print(f"🆔 Job started: {job_result}")

            if hasattr(job_result, "data") and "job_id" in job_result.data:
                job_id = job_result.data["job_id"]
                print(f"\n⏳ Polling job {job_id}...")

                # Poll a few times
                for i in range(5):
                    await asyncio.sleep(10)  # Wait 10 seconds
                    status_result = await client.call_tool(
                        "get_search_status", {"job_id": job_id}
                    )
                    status = status_result.data
                    print(
                        f"📊 Status {i + 1}: {status['status']} - {status.get('message', '')}"
                    )

                    if status["status"] in ["completed", "failed"]:
                        print("🎉 Job finished!")
                        if "result" in status:
                            print(f"📤 Result: {status['result'][:200]}...")
                        break

    except Exception as e:
        print(f"❌ Connection failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_production_server())
