# Mijiji 🛍️

**Sell anything online with just a text.**

_Twitter video demo [here](https://x.com/_krishchopra/status/1968570513078300938) (Winner of 2025 [Poke MCP Challenge](https://interaction.co/HackMIT) - Most Technically Impressive MCP Automation 🏆)_

Mijiji is an AI-powered marketplace automation tool that lets you post items for sale with minimal effort. Simply send a text message to [Poke](https://poke.com/) with a photo or description of what you want to sell, and Mijiji handles the rest - from generating compelling listings, to posting them on marketplaces like Kijiji, and even negotiating with potential buyers.

## ✨ Features

- **Text-to-Listing**: Describe your item in plain text or send a photo via Poke and get a fully formatted marketplace listing
- **AI-Powered Analysis**: Automatically categorizes products and generates optimized titles and descriptions
- **Browser Automation**: Handles the entire posting process automatically using AI browser-use agents
- **Real-time Notifications**: Get notified via Poke when your listings are posted
- **Automated Negotiation**: AI handles buyer inquiries and negotiations on your behalf
- **Poke MCP Server Integration**: Simple text-based interface through Poke - just text what you want to sell!

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

### Connecting to Poke

1. **Set up Poke Integration**

   Make sure your `POKE_API_KEY` is configured in your `.env` file.

2. **Configure Poke MCP Integration**

   In your Poke dashboard, add the Mijiji MCP server:

   - Go to your Poke MCP integration settings
   - Add your ngrok URL (e.g., `https://abc123.ngrok-free.app`) as the server endpoint
   - This allows Poke to communicate with your running Mijiji server

3. **Start using Mijiji!**

   Simply text Poke on your phone with messages like:

   - "Sell my vintage guitar - 1970s Fender Stratocaster in excellent condition, asking $1200"
   - "Post this laptop for sale: MacBook Pro 2021, 16GB RAM, some wear on corners, $800"
   - Send a photo of your item with a brief description

   Mijiji will handle everything from there - creating the listing, posting it to Kijiji, and even negotiating with potential buyers!

## 🔧 Available Tools

### Core Functions

- **`post_to_kijiji(title, description, price)`**: Post an item directly to Kijiji
- **`search_web(query)`**: Perform web searches with browser automation
- **`get_server_info()`**: Get information about the server status
- **`greet(name)`**: Test the connection with a greeting

### Background Processing

All posting operations run in the background and send notifications via Poke when complete. You can continue with your day while Mijiji handles the entire selling process.

## 📱 Poke Integration

Mijiji integrates with [Poke](https://poke.com) by The Interaction Company as your primary interface. Simply text Poke on your phone to:

- **Sell items**: Text descriptions or send photos of what you want to sell
- **Get updates**: Receive notifications when your items are posted
- **Handle negotiations**: AI manages buyer conversations automatically
- **Track progress**: Get real-time updates on posting status

To set up Poke integration:

1. Get your Poke API key from [poke.com](https://poke.com)
2. Add it to your `.env` file as `POKE_API_KEY`
3. Start texting Poke to sell your items!

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
