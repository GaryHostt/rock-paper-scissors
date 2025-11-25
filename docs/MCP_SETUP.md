# MCP Server Setup for Claude Desktop

This guide shows how to add the Rock Paper Scissors game as an MCP server in Claude Desktop.

## 📋 What is MCP?

Model Context Protocol (MCP) is a standardized protocol that allows Claude to discover and use tools. This implementation provides two tools:
- `play_rps` - Play a game of Rock Paper Scissors
- `get_stats` - Get current game statistics

The MCP server communicates via stdio (standard input/output) using JSON-RPC messages, allowing Claude to interact with the game programmatically.

## 🚀 Quick Setup

### Step 1: Locate Claude Desktop Config

The Claude Desktop configuration file is located at:

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Step 2: Add the MCP Server

Open the `claude_desktop_config.json` file and add the Rock Paper Scissors server configuration.

If the file is empty or has just `{}`, replace it with:

```json
{
  "mcpServers": {
    "rock-paper-scissors": {
      "command": "python3",
      "args": [
        "/absolute/path/to/cursor-11242025/mcp_server.py"
      ]
    }
  }
}
```

If you already have other MCP servers configured, add the `rock-paper-scissors` entry to the existing `mcpServers` object:

```json
{
  "mcpServers": {
    "existing-server": {
      ...existing config...
    },
    "rock-paper-scissors": {
      "command": "python3",
      "args": [
        "/absolute/path/to/cursor-11242025/mcp_server.py"
      ]
    }
  }
}
```

### Step 3: Update the Path

⚠️ **Important**: Replace `/absolute/path/to/cursor-11242025/mcp_server.py` with the actual **absolute path** to the `mcp_server.py` file.

To find your project path, run:
```bash
cd /path/to/cursor-11242025
realpath mcp_server.py
```

Or on macOS:
```bash
cd /path/to/cursor-11242025
echo "$(pwd)/mcp_server.py"
```

Copy the output and paste it into the config file.

### Step 4: Restart Claude Desktop

Close and reopen Claude Desktop for the changes to take effect.

## 🎮 Using the MCP Server

Once configured, Claude will automatically discover two tools:

### Available Tools

1. **`play_rps`** - Play a game of Rock Paper Scissors
   - Parameters:
     - `choice` (required): "rock", "paper", or "scissors"
     - `difficulty` (optional): "easy", "medium", or "hard" (default: "medium")

2. **`get_stats`** - Get current game statistics
   - No parameters required

### Example Interactions

You can ask Claude:
```
"Use the play_rps tool to play rock against the hard AI"
```

```
"Play 5 games of rock paper scissors and tell me my win rate"
```

```
"Get my current game statistics"
```

Claude will:
1. Automatically start the MCP server
2. Use the `play_rps` tool to play games
3. Use the `get_stats` tool to check statistics
4. Track game history across the session
5. Provide analysis and strategy

### Tool Response Format

**play_rps Response:**
```json
{
  "player_choice": "rock",
  "computer_choice": "paper",
  "result": "computer",
  "message": "You lose! Paper beats rock.",
  "stats": {
    "wins": 0,
    "losses": 1,
    "ties": 0
  },
  "total_games": 1
}
```

**get_stats Response:**
```json
{
  "stats": {
    "wins": 5,
    "losses": 3,
    "ties": 2
  },
  "total_games": 10,
  "win_rate": 50.0,
  "recent_games": [
    {"player": "rock", "computer": "scissors", "result": "player"},
    {"player": "paper", "computer": "rock", "result": "player"}
  ]
}
```

## 🔧 Advanced Configuration

### Using a Virtual Environment

If you're using a virtual environment, use the venv's Python executable:

```json
{
  "mcpServers": {
    "rock-paper-scissors": {
      "command": "/absolute/path/to/cursor-11242025/venv/bin/python3",
      "args": [
        "/absolute/path/to/cursor-11242025/mcp_server.py"
      ]
    }
  }
}
```

### How MCP Protocol Works

The MCP server communicates via **stdio** (standard input/output):

1. **Claude sends JSON-RPC requests** to the server's stdin
2. **Server processes** the request and executes the tool
3. **Server sends JSON-RPC responses** back via stdout
4. **Claude receives** the results and displays them

This is different from HTTP/REST APIs - no ports or network communication needed!

### Protocol Messages

**Initialize:**
```json
{"jsonrpc": "2.0", "method": "initialize", "id": 1}
```

**List Tools:**
```json
{"jsonrpc": "2.0", "method": "tools/list", "id": 2}
```

**Call Tool:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "play_rps",
    "arguments": {
      "choice": "rock",
      "difficulty": "hard"
    }
  },
  "id": 3
}
```

## 🧪 Testing the Setup

### Method 1: Manual Testing (Command Line)

Test the MCP server directly:

```bash
cd /path/to/cursor-11242025
python3 mcp_server.py
```

Then type JSON-RPC requests (press Enter after each):

```json
{"jsonrpc": "2.0", "method": "initialize", "id": 1}
{"jsonrpc": "2.0", "method": "tools/list", "id": 2}
{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "play_rps", "arguments": {"choice": "rock", "difficulty": "easy"}}, "id": 3}
```

Press Ctrl+D or Ctrl+C to exit.

### Method 2: Test in Claude Desktop

After restarting Claude Desktop, ask:
```
"What tools do you have available?"
```

Claude should list the `play_rps` and `get_stats` tools.

Then ask:
```
"Use the play_rps tool to play rock against the medium difficulty"
```

### Method 3: Play Multiple Games

```
"Play 10 games of rock paper scissors, trying different strategies. 
After each 5 games, use get_stats to check my performance."
```

## 🐛 Troubleshooting

### MCP Server Not Showing in Claude

**Check:**
1. The path to `mcp_server.py` is absolute (starts with `/`)
2. The config file has valid JSON syntax
3. You've restarted Claude Desktop after changes
4. Python 3 is installed: `python3 --version`

**Test the server manually:**
```bash
python3 /absolute/path/to/mcp_server.py
```

If it runs without errors, type:
```json
{"jsonrpc": "2.0", "method": "initialize", "id": 1}
```

You should see a response. Press Ctrl+C to exit.

### Tools Not Showing

In Claude Desktop, click the tools icon (🔧) in the bottom-right to see available tools. If you don't see `play_rps` and `get_stats`, check the Claude Desktop logs.

**macOS Logs:**
```bash
tail -f ~/Library/Logs/Claude/mcp*.log
```

### Permission Denied

Make sure the script is executable:
```bash
chmod +x /path/to/cursor-11242025/mcp_server.py
```

### Import Errors

The MCP server uses only Python standard library, so no extra dependencies are needed. If you see import errors, ensure you're using Python 3.7+:
```bash
python3 --version
```

## 📊 Game Statistics

The MCP server maintains session state:
- Total games played
- Wins, losses, and ties
- Win rate percentage
- Recent game history (last 5 games)

Use the `get_stats` tool anytime to check your performance!

## 🎯 Difficulty Levels

- **Easy**: Random play (~33% win rate for both sides)
- **Medium**: Learns patterns, counters most common play (up to 78% win rate vs. predictable patterns)
- **Hard**: Advanced pattern recognition (up to 63% win rate vs. predictable patterns)

## 📚 Additional Resources

- See `README.md` for complete game documentation
- See `docs/STRATEGIES.md` for AI algorithm details
- See `TEST_RESULTS.md` for AI performance analysis

## 🔄 MCP vs HTTP API

This project includes **two different ways** to interact:

### MCP Protocol (for Claude Desktop)
- **File**: `mcp_server.py`
- **Protocol**: stdio, JSON-RPC
- **Use**: Claude Desktop integration
- **Tools**: `play_rps`, `get_stats`

### Web Interface (for humans)
- **File**: `app.py` (Flask server)
- **Protocol**: HTTP/REST
- **Endpoint**: `/api/play` (for web UI)
- **Use**: Web browser gameplay

Both work independently - use MCP for Claude Desktop, HTTP for the web interface!

## 🎉 Have Fun!

Now Claude can play Rock Paper Scissors using the proper MCP protocol! Try asking Claude to:
- Play multiple games and track statistics
- Test different strategies
- Analyze patterns in gameplay
- Compare performance across difficulty levels
- Use both tools together for comprehensive gameplay

The MCP server maintains all game state within each session, so statistics persist across multiple tool calls!

