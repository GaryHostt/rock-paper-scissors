#!/usr/bin/env python3
"""
Test script for MCP server
Sends JSON-RPC requests and verifies responses
"""

import subprocess
import json
import sys

def test_mcp_server():
    """Test the MCP server with various requests."""
    
    print("🧪 Testing MCP Server for Rock Paper Scissors\n")
    print("=" * 60)
    
    # Start the MCP server
    process = subprocess.Popen(
        ['python3', 'mcp_server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    def send_request(request):
        """Send a JSON-RPC request and get response."""
        process.stdin.write(json.dumps(request) + '\n')
        process.stdin.flush()
        response_line = process.stdout.readline()
        return json.loads(response_line)
    
    try:
        # Test 1: Initialize
        print("\n1️⃣  Testing initialize...")
        response = send_request({
            "jsonrpc": "2.0",
            "method": "initialize",
            "id": 1
        })
        assert response.get("result", {}).get("serverInfo", {}).get("name") == "rock-paper-scissors"
        print("   ✅ Initialize successful")
        print(f"   Server: {response['result']['serverInfo']['name']} v{response['result']['serverInfo']['version']}")
        
        # Test 2: List tools
        print("\n2️⃣  Testing tools/list...")
        response = send_request({
            "jsonrpc": "2.0",
            "method": "tools/list",
            "id": 2
        })
        tools = response.get("result", {}).get("tools", [])
        assert len(tools) == 2
        tool_names = [t["name"] for t in tools]
        assert "play_rps" in tool_names
        assert "get_stats" in tool_names
        print("   ✅ Tools listed successfully")
        print(f"   Found tools: {', '.join(tool_names)}")
        
        # Test 3: Play a game
        print("\n3️⃣  Testing play_rps tool...")
        response = send_request({
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "play_rps",
                "arguments": {
                    "choice": "rock",
                    "difficulty": "easy"
                }
            },
            "id": 3
        })
        result = json.loads(response["result"]["content"][0]["text"])
        assert result["player_choice"] == "rock"
        assert result["computer_choice"] in ["rock", "paper", "scissors"]
        assert result["result"] in ["player", "computer", "tie"]
        print("   ✅ Game played successfully")
        print(f"   Player: {result['player_choice']}, Computer: {result['computer_choice']}")
        print(f"   Result: {result['message']}")
        
        # Test 4: Play more games
        print("\n4️⃣  Playing 5 more games...")
        for i in range(5):
            choice = ["rock", "paper", "scissors"][i % 3]
            response = send_request({
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "play_rps",
                    "arguments": {
                        "choice": choice,
                        "difficulty": "medium"
                    }
                },
                "id": 4 + i
            })
            result = json.loads(response["result"]["content"][0]["text"])
            print(f"   Game {i+1}: {choice} vs {result['computer_choice']} → {result['result']}")
        
        # Test 5: Get statistics
        print("\n5️⃣  Testing get_stats tool...")
        response = send_request({
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "get_stats",
                "arguments": {}
            },
            "id": 10
        })
        stats = json.loads(response["result"]["content"][0]["text"])
        assert stats["total_games"] == 6  # 1 from test 3 + 5 from test 4
        print("   ✅ Statistics retrieved successfully")
        print(f"   Total games: {stats['total_games']}")
        print(f"   Wins: {stats['stats']['wins']}, Losses: {stats['stats']['losses']}, Ties: {stats['stats']['ties']}")
        print(f"   Win rate: {stats['win_rate']}%")
        
        # Test 6: Test invalid tool
        print("\n6️⃣  Testing error handling...")
        response = send_request({
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "invalid_tool",
                "arguments": {}
            },
            "id": 11
        })
        assert "error" in response
        print("   ✅ Error handling works correctly")
        print(f"   Error message: {response['error']['message']}")
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("\nThe MCP server is working correctly and ready for Claude Desktop.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up
        process.terminate()
        process.wait()
    
    return True

if __name__ == "__main__":
    success = test_mcp_server()
    sys.exit(0 if success else 1)

