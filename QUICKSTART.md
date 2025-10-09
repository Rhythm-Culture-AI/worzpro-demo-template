# Quick Start

## 1. Install & Run

### UV (Recommended)
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Run the demo
uv run demo_template.py --port 8080 --auto-port
```

### Conda
```bash
# Create environment
conda create -n worzpro-demo python=3.10
conda activate worzpro-demo

# Install dependencies
conda install -c conda-forge gradio numpy soundfile librosa python-dotenv
pip install madmom yt-dlp

# Run the demo
python demo_template.py --port 8080 --auto-port
```

### Pip
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the demo
python demo_template.py --port 8080 --auto-port
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

## Command-Line Options

```bash
--port 8080     # Use custom port
--auto-port     # Automatically find available port if occupied
--share         # Create public URL (valid for 72 hours)
--debug         # Enable debug mode with auto-reload
--help          # Show all options
```

### Examples

```bash
# Local only
python demo_template.py

# Custom port with auto-fallback
python demo_template.py --port 8080 --auto-port

# Public URL for sharing
python demo_template.py --share

# Public URL on custom port
python demo_template.py --share --port 8080
```

### Using --share Flag

The `--share` flag creates a **temporary public URL** using Gradio's sharing service:

```bash
python demo_template.py --share
```

**You'll see:**
```
🔐 GRADIO_ALLOWED_PATHS configured: 4 directories
Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://abc123xyz.gradio.live  ← Share this!
```

**Benefits:**
- ✅ Share demos instantly (no deployment needed)
- ✅ Test on mobile devices
- ✅ Demo to clients/colleagues remotely
- ✅ Works behind firewalls

**Note:** Public URLs expire after 72 hours.

---

That's it! 🎉