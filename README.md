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

## Features

- Audio file upload
- YouTube URL download
- Multiple analysis options
- Audio visualization with click tracks
- Clean, professional UI

## Customization

Replace the `analyze_audio()` function in `demo_template.py` with your own audio processing logic.

## Requirements

- Python 3.8+
- UV package manager
- Audio processing library (madmom example included)

## License

MIT License