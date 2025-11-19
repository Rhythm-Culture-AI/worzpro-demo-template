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

## Configuration

### Directory Configuration

The demo uses two directories:

1. **`SAMPLES_DIR`** - Sample audio files (can be overridden with `--samples-dir` CLI argument)
2. **`TEMP_DIR`** - Temporary files and downloads (config-only via `.env`)

### TEMP_DIR (Infrastructure Setting)

`TEMP_DIR` is where the demo stores:
- Generated audio files with click tracks
- YouTube downloads
- Analysis outputs

**This is a deployment/infrastructure setting** - configure it once in `.env` for your environment:

```bash
# Create .env file
cp .env.example .env

# Edit .env file
# Development: Use system temp (cleared on reboot)
TEMP_DIR=/tmp/demo_temp

# Production: Use persistent directory
TEMP_DIR=/var/app/demo_temp

# Local: Use project directory (default)
TEMP_DIR=outputs/demo_analysis
```

**Why config-only?** Temporary file location is an infrastructure concern that should be set once during deployment, not changed with each run.

### SAMPLES_DIR (Runtime Setting)

You can override the samples directory at runtime for quick testing:

```bash
# Use custom samples directory
python demo_template.py --samples-dir ~/Music/samples

# Test different sample sets
python demo_template.py --samples-dir /path/to/test/audio
```

Or configure it in `.env`:
```bash
SAMPLES_DIR=/home/user/Music/samples
```

### Configuration Priority

**For SAMPLES_DIR:**
1. Command-line `--samples-dir` (highest)
2. Environment variable `SAMPLES_DIR`
3. Default: `assets/audio_samples/`

**For TEMP_DIR:**
1. Environment variable `TEMP_DIR`
2. Default: `outputs/demo_analysis/`

### Automatic Cleanup

Delete old temporary files automatically on startup:

```bash
# Delete files older than 7 days (default)
python demo_template.py

# Delete files older than 3 days
python demo_template.py --cleanup-days 3

# Disable cleanup
python demo_template.py --cleanup-days 0
```

### Complete Configuration Example

```bash
# .env file (infrastructure settings)
TEMP_DIR=/tmp/demo_temp
SAMPLES_DIR=~/Music/samples
PORT=8080
HOST=0.0.0.0

# Runtime with all CLI options
python demo_template.py \
  --samples-dir ~/Music/test_samples \
  --cleanup-days 3 \
  --port 8080 \
  --share
```

### View All Options

```bash
python demo_template.py --help
```

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