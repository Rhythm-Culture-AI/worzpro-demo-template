# Quick Start

## 1. Install & Run

```bash
# Install dependencies
uv sync

# Run the demo
uv run demo_template.py --port 8080
```

Visit `http://localhost:8080`

## 2. Try It

1. Upload an audio file or paste a YouTube URL
2. Select analysis options
3. Click "Analyze Audio"
4. Listen to results with click tracks

## 3. Customize

Edit `demo_template.py`:
- Replace madmom imports with your library
- Update the `analyze_audio()` function
- Change the UI text and options

## Options

```bash
--port 8080    # Custom port
--share         # Get public URL
--help          # Show all options
```

That's it! 🎉