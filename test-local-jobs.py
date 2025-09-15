#!/usr/bin/env python3
import asyncio
from fastmcp import Client


async def test_local_background_jobs():
    print("🧪 Testing local MCP server with background jobs...")

    try:
        # Connect to local server
        client = Client("http://localhost:8000/mcp")

        async with client:
            print("✅ Connected to local MCP server!")

            # List tools
            tools = await client.list_tools()
            print(f"📋 Available tools: {[tool.name for tool in tools]}")

            # Test background job pattern
            print("\n🔍 Starting background search...")
            job_result = await client.call_tool("search_web", {"query": "AI music"})
            job_data = job_result.data
            print(f"🆔 Job started: {job_data['job_id']}")
            print(f"📝 Status: {job_data['status']}")

            job_id = job_data["job_id"]

            # Poll for results
            print(f"\n⏳ Polling job {job_id}...")
            for i in range(10):  # Poll up to 10 times (100 seconds)
                await asyncio.sleep(10)

                status_result = await client.call_tool(
                    "get_search_status", {"job_id": job_id}
                )
                status = status_result.data

                print(f"📊 Poll {i + 1}: {status['status']}")
                if "message" in status:
                    print(f"   💬 {status['message']}")
                if "running_for" in status:
                    print(f"   ⏱️  Running for: {status['running_for']}")

                if status["status"] == "completed":
                    print("🎉 SUCCESS! Browser search completed!")
                    print(f"📤 Result: {status['result']}")
                    print(f"⏱️  Total time: {status['total_time']}")
                    break
                elif status["status"] == "failed":
                    print("❌ FAILED!")
                    print(f"💥 Error: {status['error']}")
                    break

            print("\n✅ Background job pattern test complete!")

    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_local_background_jobs())
