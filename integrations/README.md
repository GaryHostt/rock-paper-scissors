# External Tool Integrations

This directory contains files for integrating the Rock Paper Scissors game with external tools and AI assistants.

## Files

### `mcp_server.py`
Model Context Protocol (MCP) server that allows Claude Desktop to play Rock Paper Scissors programmatically.

**Features:**
- Implements MCP protocol specification (2024-11-05)
- Communicates via stdio using JSON-RPC 2.0
- Provides two tools: `play_rps` and `get_stats`
- Maintains game state across session
- Includes all four AI difficulty levels

**Running directly:**
```bash
python3 integrations/mcp_server.py
```

Then interact via JSON-RPC messages on stdin/stdout.

---

### `claude_desktop_config.json`
Example configuration file for Claude Desktop to connect to the MCP server.

**Location:** Copy this to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

**Configuration:**
```json
{
  "mcpServers": {
    "rock-paper-scissors": {
      "command": "python3",
      "args": [
        "/absolute/path/to/cursor-11242025/integrations/mcp_server.py"
      ]
    }
  }
}
```

**Important:** Update the absolute path to match your system!

---

## Setup Guide

For detailed setup instructions, see:
- `../docs/MCP_SETUP.md` - Complete setup guide for Claude Desktop
- `../docs/MCP_IMPLEMENTATION.md` - Technical details of MCP protocol

### Quick Setup

1. **Get absolute path:**
   ```bash
   cd integrations
   echo "$(pwd)/mcp_server.py"
   ```

2. **Update Claude Desktop config** with the absolute path

3. **Restart Claude Desktop**

4. **Test:**
   Ask Claude: "What tools do you have available?"
   You should see `play_rps` and `get_stats`

## MCP Tools Available

### `play_rps`
Play a game of Rock Paper Scissors.

**Parameters:**
- `choice` (required): "rock", "paper", or "scissors"
- `difficulty` (optional): "easy", "medium", "hard", or "veryhard"

**Returns:**
- `player_choice`: Your choice
- `computer_choice`: AI's choice
- `result`: "player", "computer", or "tie"
- `message`: Descriptive result message
- `stats`: Current win/loss/tie statistics
- `total_games`: Total games played in session

### `get_stats`
Get current game statistics.

**Parameters:** None

**Returns:**
- `stats`: Win/loss/tie counts
- `total_games`: Total games played
- `win_rate`: Win percentage
- `recent_games`: Last 5 games

## Architecture

The MCP server is **separate** from the web application:

```
┌─────────────────────┐
│  Claude Desktop     │
│  (MCP Client)       │
└──────────┬──────────┘
           │ stdio/JSON-RPC
           │
┌──────────▼──────────┐
│  mcp_server.py      │
│  (MCP Server)       │
└─────────────────────┘

┌─────────────────────┐
│  Web Browser        │
└──────────┬──────────┘
           │ HTTP/REST
           │
┌──────────▼──────────┐
│  app.py             │
│  (Flask Server)     │
└─────────────────────┘
```

They run independently and don't interfere with each other!

## Future Integrations

Potential additions to this directory:
- API clients for other AI assistants
- Webhook integrations
- Discord bot integration
- Slack bot integration
- REST API client libraries
- GraphQL schema

## Related Documentation

- `../docs/MCP_SETUP.md` - Setup guide
- `../docs/MCP_IMPLEMENTATION.md` - Protocol details
- `../docs/STRATEGIES.md` - AI algorithm documentation
- `../README.md` - Main project documentation

