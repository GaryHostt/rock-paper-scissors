# MCP Server Setup for Claude Desktop

This guide shows how to add the Rock Paper Scissors game as an MCP server in Claude Desktop.

## 📋 What is MCP?

Model Context Protocol (MCP) allows Claude to interact directly with external applications. By setting up this game as an MCP server, Claude can play Rock Paper Scissors programmatically via the `/mcp/play` API endpoint.

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
        "-m",
        "flask",
        "run",
        "--host=0.0.0.0",
        "--port=5000"
      ],
      "cwd": "/path/to/cursor-11242025",
      "env": {
        "FLASK_APP": "app.py",
        "FLASK_ENV": "production",
        "PYTHONPATH": "/path/to/cursor-11242025"
      }
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
        "-m",
        "flask",
        "run",
        "--host=0.0.0.0",
        "--port=5000"
      ],
      "cwd": "/path/to/cursor-11242025",
      "env": {
        "FLASK_APP": "app.py",
        "FLASK_ENV": "production",
        "PYTHONPATH": "/path/to/cursor-11242025"
      }
    }
  }
}
```

### Step 3: Update the Path

⚠️ **Important**: Replace `/path/to/cursor-11242025` with the actual path to your project directory.

To find your project path, run:
```bash
cd /path/to/cursor-11242025
pwd
```

### Step 4: Restart Claude Desktop

Close and reopen Claude Desktop for the changes to take effect.

## 🎮 Using the MCP Server

Once configured, Claude can interact with the game by making requests to `http://localhost:5000/mcp/play`.

### Example Interaction

You can ask Claude:
```
"Play a game of rock paper scissors with me using the MCP server. 
You choose rock, paper, or scissors, and I'll play against the hard AI."
```

Claude will:
1. Start the Flask server automatically
2. Make API calls to `/mcp/play`
3. Track game history
4. Provide analysis and strategy

### API Endpoint Details

**Endpoint:** `POST http://localhost:5000/mcp/play`

**Request Body:**
```json
{
  "agent_id": "claude_agent",
  "choice": "rock",
  "opponent_difficulty": "hard",
  "session_history": []
}
```

**Response:**
```json
{
  "agent_choice": "rock",
  "opponent_choice": "paper",
  "result": "opponent_win",
  "agent_id": "claude_agent",
  "game_number": 1,
  "session_stats": {
    "agent_wins": 0,
    "opponent_wins": 1,
    "ties": 0
  },
  "message": "Agent chose rock, opponent chose paper. Result: opponent_win!"
}
```

## 🔧 Advanced Configuration

### Using a Virtual Environment

If you're using a virtual environment, update the config to use the venv's Python:

```json
{
  "mcpServers": {
    "rock-paper-scissors": {
      "command": "/path/to/cursor-11242025/venv/bin/python3",
      "args": [
        "-m",
        "flask",
        "run",
        "--host=0.0.0.0",
        "--port=5000"
      ],
      "cwd": "/path/to/cursor-11242025",
      "env": {
        "FLASK_APP": "app.py",
        "FLASK_ENV": "production"
      }
    }
  }
}
```

### Using a Different Port

If port 5000 is already in use, change it in the args:

```json
"args": [
  "-m",
  "flask",
  "run",
  "--host=0.0.0.0",
  "--port=5001"
]
```

Then update your API calls to use `http://localhost:5001/mcp/play`.

### Adding OpenAI API Key

If you want Claude to access the OpenAI commentary feature, add your API key to the env:

```json
"env": {
  "FLASK_APP": "app.py",
  "FLASK_ENV": "production",
  "OPENAI_API_KEY": "sk-your-api-key-here",
  "PYTHONPATH": "/path/to/cursor-11242025"
}
```

## 🧪 Testing the Setup

### Method 1: Test with Python Script

Run the included test script:

```bash
cd /path/to/cursor-11242025
python3 test_mcp.py medium 10
```

This will play 10 games against the medium AI.

### Method 2: Test with cURL

```bash
curl -X POST http://localhost:5000/mcp/play \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "test_agent",
    "choice": "rock",
    "opponent_difficulty": "easy"
  }'
```

### Method 3: Test in Claude Desktop

After restarting Claude Desktop, ask:
```
"Can you access the rock-paper-scissors MCP server? 
Play a game choosing paper against the medium difficulty."
```

## 🐛 Troubleshooting

### Port Already in Use

If you see "Port 5000 is in use":

1. **On macOS**: Disable AirPlay Receiver in System Preferences → General → AirDrop & Handoff
2. **Or kill the process**:
   ```bash
   lsof -ti:5000 | xargs kill -9
   ```
3. **Or use a different port** (see Advanced Configuration above)

### Server Won't Start

Check that:
- Python 3 is installed: `python3 --version`
- Dependencies are installed: `pip3 install -r requirements.txt`
- The path in the config is correct
- You have write permissions in the project directory

### Claude Can't Connect

Verify:
- The server is running: `curl http://localhost:5000/`
- The config file has correct JSON syntax
- You've restarted Claude Desktop after changing the config

## 📊 Game Statistics

The MCP endpoint tracks:
- Total games played
- Agent wins, losses, and ties
- Session history for pattern analysis
- AI difficulty performance

## 🎯 Difficulty Levels

- **Easy**: Random play (~33% win rate for both sides)
- **Medium**: Learns patterns, counters most common play (up to 78% win rate vs. predictable patterns)
- **Hard**: Advanced pattern recognition (up to 63% win rate vs. predictable patterns)
- **Very Hard**: Master-level psychology-based AI

## 📚 Additional Resources

- See `README.md` for complete game documentation
- See `STRATEGIES.md` for AI algorithm details
- See `testing/README.md` for testing framework
- See `OPENAI_SETUP.md` for AI commentary setup

## 🎉 Have Fun!

Now Claude can play Rock Paper Scissors programmatically! Try asking Claude to:
- Play multiple games and track statistics
- Test different strategies
- Analyze patterns in gameplay
- Compare performance across difficulty levels

