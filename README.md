# Worzpro Demo Template

A simple template for creating Gradio audio analysis demos.

## Quick Start

### Option 1: UV (Recommended)
```bash
# Install UV if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Run the demo
uv run demo_template.py --port 8080 --auto-port
```

### Option 2: Conda
```bash
# Create conda environment
conda create -n worzpro-demo python=3.10
conda activate worzpro-demo

# Install dependencies
conda install -c conda-forge gradio numpy soundfile librosa python-dotenv
pip install madmom yt-dlp

# Run the demo
python demo_template.py --port 8080 --auto-port
```

### Option 3: Pip
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the demo
python demo_template.py --port 8080 --auto-port
```

### Open your browser:
Visit `http://localhost:8080`

### Create a Public URL (Optional)

Share your demo with others using the `--share` flag:

```bash
# UV
uv run demo_template.py --share

# Python
python demo_template.py --share
```

This creates a temporary public URL (valid for 72 hours) that you can share with anyone.

**Example output:**
```
Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://abc123xyz.gradio.live
```

**Use cases:**
- Share demos with colleagues/clients
- Test on mobile devices
- Demo from behind a firewall
- Quick prototyping without deployment

## Features

- Audio file upload
- YouTube URL download
- Multiple analysis options
- Audio visualization with click tracks
- Clean, professional UI

## Customization

**See [CUSTOMIZATION_GUIDE.md](CUSTOMIZATION_GUIDE.md)** for detailed instructions on adapting this template for your audio processing needs.

Quick summary:
1. Replace library imports (madmom → your library)
2. Update configuration (title, description)
3. Rewrite `analyze_audio()` function with your logic
4. Update analysis options in the UI

## Requirements

- Python 3.8+
- UV package manager
- Audio processing library (madmom example included)

## License

MIT License