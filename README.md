# Worzpro Demo Template

A simple template for creating Gradio audio analysis demos.

## Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run the demo:**
   ```bash
   uv run demo_template.py --port 8080
   ```

3. **Open your browser:**
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