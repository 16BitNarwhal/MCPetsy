# Mijiji 🛍️

**Sell anything online with just a text.** Twitter video demo [here](https://x.com/_krishchopra/status/1968570513078300938) (Winner of 2025 [Poke MCP Challenge](https://interaction.co/HackMIT) - Most Technically Impressive MCP Automation 🏆)

Mijiji is an AI-powered marketplace automation tool that lets you post items for sale with minimal effort. Simply send a photo or describe what you want to sell via text message, and Mijiji handles the rest - from generating compelling listings, to posting them on marketplaces like Kijiji, and even negotiating with potential buyers.

## ✨ Features

- **Text-to-Listing**: Describe your item in plain text (via text message or photo) and get a fully formatted marketplace listing
- **AI-Powered Analysis**: Automatically categorizes products and generates optimized titles and descriptions
- **Browser Automation**: Handles the entire posting process automatically using AI browser-use agents
- **Real-time Notifications**: Get notified via Poke when your listings are posted
- **MCP Server Integration**: Works seamlessly with Claude and other AI assistants through MCP protocol

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Node.js (for testing)
- Ngrok account (for exposing local server)
- Anthropic API key
- Poke API key
- Kijiji account credentials (username and password)

### Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd MCPetsy
   ```

2. **Set up Python environment**

   ```bash
   cd mcp
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the `mcp/` directory:

   ```env
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   POKE_API_KEY=your_poke_api_key_here
   KIJIJI_USERNAME=your_kijiji_username
   KIJIJI_PASSWORD=your_kijiji_password
   PORT=8000
   ```

4. **Start the MCP server**

   ```bash
   cd mcp/src
   python server.py
   ```

5. **Expose server via Ngrok**
   In a new terminal:
   ```bash
   ngrok http 8000
   ```
   Copy the HTTPS URL (e.g., `https://abc123.ngrok-free.app`)

### Connecting to Claude via MCP

1. **Add to Claude Desktop configuration**

   Add this to your Claude Desktop MCP settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

   ```json
   {
     "mcpServers": {
       "mijiji": {
         "command": "node",
         "args": [
           "-e",
           "console.log('MCP server running at https://your-ngrok-url.ngrok-free.app')"
         ],
         "transport": {
           "type": "http",
           "url": "https://your-ngrok-url.ngrok-free.app"
         }
       }
     }
   }
   ```

2. **Restart Claude Desktop**

3. **Start using Mijiji!**

   In Claude, you can now say things like:

   - "Help me sell my vintage guitar - it's a 1970s Fender Stratocaster in excellent condition, asking $1200"
   - "Post this laptop for sale: MacBook Pro 2021, 16GB RAM, some wear on corners, $800"

## 🔧 Available Tools

### Core Functions

- **`post_to_kijiji(title, description, price)`**: Post an item directly to Kijiji
- **`search_web(query)`**: Perform web searches with browser automation
- **`get_server_info()`**: Get information about the server status
- **`greet(name)`**: Test the connection with a greeting

### Background Processing

All posting operations run in the background and send notifications via Poke when complete. You can continue using Claude while Mijiji handles the posting process.

## 📱 Poke Integration

Mijiji integrates with [Poke](https://poke.com) to send you real-time notifications when:

- Your item has been successfully posted
- There's an error during posting
- Browser automation tasks complete

To set up Poke notifications:

1. Get your Poke API key
2. Add it to your `.env` file as `POKE_API_KEY`
3. You'll receive notifications directly through Poke when tasks complete

## 🛠️ Development

### Project Structure

```
MCPetsy/
├── mcp/                    # MCP server implementation
│   ├── src/
│   │   ├── server.py      # Main MCP server
│   │   ├── endpoints.py   # Kijiji posting logic
│   │   ├── handleImage.py # Image analysis (future feature)
│   │   └── agent_to_integrate.py # Browser automation agent
│   ├── requirements.txt   # Python dependencies
├── agent.py              # Standalone agent runner
├── test-*.py            # Testing utilities
└── README.md            # This file
```

### Testing

Run the test scripts to verify functionality:

```bash
# Test basic MCP tools
python test-basic-tools.py

# Test local job processing
python test-local-jobs.py

# Test production connection
python test-prod-connection.py
```

---

**Happy selling with Mijiji! 🎉**
