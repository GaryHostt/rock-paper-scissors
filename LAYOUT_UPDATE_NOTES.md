Complete update in progress. I need to restart the Flask server with the virtual environment. Let me guide you through a simpler approach:

**To get your app working properly and test the new layout:**

1. First, stop any running Flask instances:
```bash
pkill -f "python.*app.py"
```

2. Start the server with the virtual environment:
```bash
cd /path/to/cursor-11242025
source venv/bin/activate
python app.py
```

3. Open http://localhost:5000 in your browser

**What I've Changed:**

✅ **Layout Changes:**
- Stats panel now opens as a bottom panel (not a sidebar)
- Trend graph now opens as a bottom panel (not a modal overlay)
- Game container expands width when panels are open
- Body gets `.stats-open` and `.trends-open` classes to manage layout

✅ **CSS Updates:**
- Changed stats panel from `position: fixed` sidebar to bottom expandable panel
- Changed trend modal from overlay to bottom expandable panel  
- Both use `max-height` transitions for smooth opening/closing
- Grid layout for stats cards when open

✅ **JavaScript Updates:**
- `toggleStatsPanel()` now adds/removes `.stats-open` class on body
- `showTrendGraph()` now adds `.trends-open` class on body
- Removed click-outside-to-close for bottom panels

**The new flow:**
1. Game box: centered, 600px max width
2. Click "View Hand Statistics" → game box expands to 1100px, stats panel slides up from bottom
3. Click "Show Trend Graph" → trend panel slides up below stats (if open) or below game box
4. Both can be open simultaneously with the menu

Let me know if you'd like me to create a complete working demo or if you want to test what we have so far!

