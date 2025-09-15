#!/usr/bin/env python3
import asyncio
from fastmcp import Client


async def test_basic_tools():
    print("🧪 Testing basic MCP tools (no browser automation)...")

    try:
        client = Client("https://fastmcp-server-wf77.onrender.com/mcp")

        async with client:
            print("✅ Connected to production MCP server!")

            # Test greet tool
            print("\n👋 Testing greet tool...")
            greet_result = await client.call_tool("greet", {"name": "Krish"})
            print(f"📤 Greet result: {greet_result.data}")

            # Test get_server_info tool
            print("\n📊 Testing get_server_info tool...")
            info_result = await client.call_tool("get_server_info", {})
            print(f"📤 Server info: {info_result.data}")

            print("\n✅ Basic tools working perfectly!")

    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_basic_tools())
