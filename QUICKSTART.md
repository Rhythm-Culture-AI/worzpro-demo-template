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

## Options

```bash
--port 8080    # Custom port
--share         # Get public URL
--help          # Show all options
```

That's it! 🎉