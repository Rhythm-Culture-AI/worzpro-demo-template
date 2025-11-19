
#!/usr/bin/env python3
"""
Worzpro Demo Template - Standalone Gradio Audio Analysis Demo

Features:
- Sample audio library with automatic discovery
- YouTube download integration (yt-dlp)
- Multiple analysis options
- Audio visualization with click tracks
- Professional UI with Gradio Soft theme
- Command-line arguments (--share, --port, --auto-port)

Structure:
1. Configuration - Customize for your project
2. UI Helpers - Reusable across demos
3. YouTube Download - Keep as-is
4. Core Analysis - Replace with your audio processing
5. Demo Interface - Customize UI and options
"""

import os
import argparse
import gradio as gr
from pathlib import Path
import time
import numpy as np
import soundfile as sf
import librosa
import socket
import tempfile
from dotenv import load_dotenv

# === EXAMPLE: Madmom-specific imports (replace with your library) ===
try:
    from madmom.features.downbeats import DBNDownBeatTrackingProcessor, RNNDownBeatProcessor
    from madmom.features.onsets import OnsetPeakPickingProcessor, RNNOnsetProcessor
    from madmom.features.beats import RNNBeatProcessor
    from madmom.features.tempo import TempoEstimationProcessor
    MADMOM_AVAILABLE = True
except ImportError:
    MADMOM_AVAILABLE = False
    print("⚠️ Madmom not available. Install with: uv add madmom")

# === CONFIGURATION ===
load_dotenv()

# Directories (use absolute paths for file serving)
SAMPLES_DIR = Path(os.getenv('SAMPLES_DIR', 'assets/audio_samples')).resolve()
TEMP_DIR = Path(os.getenv('TEMP_DIR', 'outputs/demo_analysis')).resolve()

# Audio configuration
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac'}

# Ensure directories exist
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# UI Configuration
APP_TITLE = "Audio Analysis Demo"
APP_DESCRIPTION = """
# 🎵 Audio Analysis Demo Template

Comprehensive music information retrieval using madmom.
Replace this with your own audio processing library!
"""

# Custom CSS (optional)
CUSTOM_CSS = ""

# === UI HELPERS ===

def get_audio_samples():
    """
    Dynamically discover audio samples from the configured directory.

    Returns:
        List of dicts with sample metadata (name, path, emoji, filename)
    """
    samples = []

    if SAMPLES_DIR.exists():
        print(f"📁 Scanning samples directory: {SAMPLES_DIR}")
        for audio_file in SAMPLES_DIR.iterdir():
            if audio_file.is_file() and audio_file.suffix.lower() in AUDIO_EXTENSIONS:
                # Create friendly name
                friendly_name = audio_file.stem.replace('_', ' ').replace('-', ' - ')

                # Assign emoji based on filename
                filename_lower = friendly_name.lower()
                emoji_map = {'guitar': '🎸', 'drum': '🥁', 'beat': '🥁', 'piano': '🎹',
                            'keyboard': '🎹', 'vocal': '🎤', 'voice': '🎤', 'bass': '🎸'}
                emoji = next((v for k, v in emoji_map.items() if k in filename_lower), '🎵')

                samples.append({
                    'name': friendly_name,
                    'path': str(audio_file),
                    'emoji': emoji,
                    'filename': audio_file.name
                })
    else:
        print(f"⚠️ Samples directory not found: {SAMPLES_DIR}")
        print(f"💡 Create it with: mkdir -p {SAMPLES_DIR}")

    # Sort alphabetically
    samples.sort(key=lambda x: x['name'])
    return samples

def load_sample_audio(sample_path):
    """Load a sample audio file path for the audio input component."""
    if sample_path:
        # Ensure absolute path for proper file serving
        return str(Path(sample_path).resolve())
    return None

# === YOUTUBE DOWNLOAD ===

def download_youtube_audio_ytdlp(youtube_url, audio_format="wav", audio_quality="128"):
    """
    Download audio from YouTube URL using yt-dlp.

    Args:
        youtube_url: YouTube video URL
        audio_format: Output format ('wav' or 'mp3')
        audio_quality: Quality in kbps for lossy formats

    Returns:
        Tuple of (audio_path, result_message)
    """
    if not youtube_url or youtube_url.strip() == "":
        return None, "❌ Please enter a YouTube URL first."

    try:
        import yt_dlp

        # Create output directory
        output_folder = TEMP_DIR / "youtube_downloads"
        output_folder.mkdir(parents=True, exist_ok=True)

        # Configure output path
        timestamp = int(time.time())
        output_template = str(output_folder / f"youtube_audio_{timestamp}.%(ext)s")

        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
            'extract_audio': True,
        }

        # Format-specific postprocessing
        if audio_format == "wav":
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }]
        elif audio_format == "mp3":
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': audio_quality,
            }]

        # Download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            video_title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)

        # Find downloaded file
        expected_path = output_folder / f"youtube_audio_{timestamp}.{audio_format}"

        if expected_path.exists():
            result_text = f"""
# 🎉 YouTube Audio Downloaded!

## 📺 Video Information
- **Title:** `{video_title}`
- **Duration:** `{duration}s` ({duration/60:.1f} minutes)

## 🎵 Download Details
- **Format:** `{audio_format.upper()}`
- **Quality:** `{audio_quality} kbps`
- **File:** `{expected_path.name}`
- **Location:** `{expected_path}`

---
✅ **Ready for analysis!**
            """
            return str(expected_path), result_text
        else:
            return None, f"# ❌ Error\n\nFile not found: {expected_path}"

    except ImportError:
        return None, "# ❌ Error\n\n**yt-dlp not available.**\n\nInstall with: `uv add yt-dlp` or `pip install yt-dlp`"
    except Exception as e:
        return None, f"# ❌ Error\n\n**Download failed:** `{str(e)}`"

# === CORE ANALYSIS (REPLACE WITH YOUR PROCESSING) ===

def analyze_audio(audio_file, analysis_options):
    """
    EXAMPLE: Madmom-based audio analysis.

    **REPLACE THIS FUNCTION** with your own processing logic!

    Args:
        audio_file: Path to audio file
        analysis_options: List of selected analysis types

    Returns:
        Tuple of (result_markdown, audio_output_1, audio_output_2, audio_output_3)
    """
    if audio_file is None:
        return "❌ Please upload an audio file first.", None, None, None

    if not MADMOM_AVAILABLE:
        return "# ❌ Error\n\n**Madmom not available.**\n\nInstall with: `uv add madmom`", None, None, None

    try:
        # Load audio
        audio, sr = sf.read(audio_file)
        file_path = Path(audio_file)
        file_size = file_path.stat().st_size / 1024  # KB
        duration = len(audio) / sr

        results = {}
        audio_outputs = {}

        # EXAMPLE 1: Beat Tracking
        if "Beat Tracking" in analysis_options:
            print("🥁 Running beat tracking...")
            proc = DBNDownBeatTrackingProcessor(beats_per_bar=[3, 4], fps=100)
            act = RNNDownBeatProcessor()(audio)
            beat_result = proc(act)

            beats = beat_result[:, 0]
            downbeats = beat_result[beat_result[:, 1] == 1, 0]

            # Calculate BPM
            if len(beats) > 1:
                bpm = 60 / np.mean(np.diff(beats))
            else:
                bpm = 0

            results['beats'] = {
                'beats': beats,
                'downbeats': downbeats,
                'bpm': bpm,
                'total_beats': len(beats),
                'total_downbeats': len(downbeats)
            }

            # Create audio with click tracks
            click_track = librosa.clicks(times=beats, sr=sr, click_freq=800,
                                        click_duration=0.1, length=len(audio))
            downbeat_clicks = librosa.clicks(times=downbeats, sr=sr, click_freq=1200,
                                           click_duration=0.15, length=len(audio))

            # Handle stereo
            if len(audio.shape) > 1 and audio.shape[1] == 2:
                click_track = np.column_stack([click_track, click_track])
                downbeat_clicks = np.column_stack([downbeat_clicks, downbeat_clicks])

            # Mix audio + clicks
            mixed_audio = audio + (click_track * 0.3) + (downbeat_clicks * 0.3)
            if np.max(np.abs(mixed_audio)) > 0:
                mixed_audio = mixed_audio / np.max(np.abs(mixed_audio)) * 0.8

            # Save
            timestamp = int(time.time())
            beat_path = TEMP_DIR / f"beats_{timestamp}.wav"
            sf.write(beat_path, mixed_audio, sr)
            audio_outputs['beats'] = str(beat_path)

        # EXAMPLE 2: Onset Detection
        if "Onset Detection" in analysis_options:
            print("🎯 Running onset detection...")
            onset_proc = OnsetPeakPickingProcessor(threshold=0.5, fps=100)
            onset_act = RNNOnsetProcessor()(audio)
            onsets = onset_proc(onset_act)

            results['onsets'] = {
                'onset_times': onsets,
                'total_onsets': len(onsets),
            }

            # Create audio with onset clicks
            onset_clicks = librosa.clicks(times=onsets, sr=sr, click_freq=1500,
                                         click_duration=0.08, length=len(audio))

            if len(audio.shape) > 1 and audio.shape[1] == 2:
                onset_clicks = np.column_stack([onset_clicks, onset_clicks])

            mixed_onset = audio + (onset_clicks * 0.3)
            if np.max(np.abs(mixed_onset)) > 0:
                mixed_onset = mixed_onset / np.max(np.abs(mixed_onset)) * 0.8

            timestamp = int(time.time())
            onset_path = TEMP_DIR / f"onsets_{timestamp}.wav"
            sf.write(onset_path, mixed_onset, sr)
            audio_outputs['onsets'] = str(onset_path)

        # EXAMPLE 3: Tempo Estimation
        if "Tempo Estimation" in analysis_options:
            print("⏱️ Running tempo estimation...")
            tempo_proc = TempoEstimationProcessor(fps=100)
            beat_proc = RNNBeatProcessor()(audio)
            tempo_result = tempo_proc(beat_proc)

            if len(tempo_result) > 0:
                primary_tempo = tempo_result[0][0] if isinstance(tempo_result[0], (list, tuple, np.ndarray)) else tempo_result[0]
                results['tempo'] = {
                    'primary_tempo': float(primary_tempo),
                }
            else:
                results['tempo'] = {'primary_tempo': 0.0}

        # Generate formatted results
        result_text = f"""
# 🎵 Analysis Results

## 📁 File Information
- **Filename:** `{file_path.name}`
- **Size:** `{file_size:.1f} KB`
- **Duration:** `{duration:.2f}s` ({duration/60:.1f} minutes)
- **Sample Rate:** `{sr} Hz`

"""

        if 'beats' in results:
            data = results['beats']
            result_text += f"""
## 🥁 Beat Tracking
- **BPM:** `{data['bpm']:.1f}`
- **Total Beats:** `{data['total_beats']}`
- **Total Downbeats:** `{data['total_downbeats']}`
- **First Beat:** `{data['beats'][0]:.2f}s`
- **Last Beat:** `{data['beats'][-1]:.2f}s`

"""

        if 'onsets' in results:
            data = results['onsets']
            result_text += f"""
## 🎯 Onset Detection
- **Total Onsets:** `{data['total_onsets']}`
- **Density:** `{data['total_onsets']/duration:.1f} onsets/second`
- **First Onset:** `{data['onset_times'][0]:.2f}s`
- **Last Onset:** `{data['onset_times'][-1]:.2f}s`

"""

        if 'tempo' in results:
            data = results['tempo']
            result_text += f"""
## ⏱️ Tempo Estimation
- **Primary Tempo:** `{data['primary_tempo']:.1f} BPM`

"""

        result_text += """
---
✅ **Analysis completed!**

💡 **Tip:** Play audio outputs below to hear detected features.
        """

        return (
            result_text,
            audio_outputs.get('beats'),
            audio_outputs.get('onsets'),
            None  # Placeholder for third output
        )

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error during analysis:\n{error_details}")
        return f"# ❌ Error\n\n**Analysis failed:** `{str(e)}`\n\nCheck console for details.", None, None, None

# === DEMO INTERFACE ===

def create_demo():
    """Create the Gradio demo interface."""

    with gr.Blocks(
        title=APP_TITLE,
        theme=gr.themes.Soft(
            primary_hue="blue",
            neutral_hue="gray",
            font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"]
        ),
        css=CUSTOM_CSS
    ) as demo:
        # Title and description
        gr.Markdown(APP_DESCRIPTION)

        # Sample Audio Section
        gr.Markdown("### 🎵 Sample Audio (Click to Load)")

        audio_samples = get_audio_samples()
        if audio_samples:
            with gr.Row():
                sample_buttons = []
                for sample in audio_samples:
                    btn = gr.Button(
                        f"{sample['emoji']} {sample['name']}",
                        variant="secondary",
                        size="sm"
                    )
                    sample['button'] = btn
                    sample_buttons.append((btn, sample['path']))
        else:
            gr.Markdown(f"*No audio samples found. Add files to: `{SAMPLES_DIR}`*")

        # Input Section
        gr.Markdown("### 🎯 Input Audio")

        with gr.Row():
            with gr.Column(scale=2):
                audio_input = gr.Audio(
                    label="Drop audio file here",
                    type="filepath"
                )

            with gr.Column(scale=1):
                youtube_url = gr.Textbox(
                    label="Or paste YouTube URL",
                    placeholder="https://youtube.com/watch?v=...",
                    lines=2
                )
                audio_format = gr.Dropdown(
                    label="Format",
                    choices=["wav", "mp3"],
                    value="wav"
                )
                audio_quality = gr.Dropdown(
                    label="Quality (MP3)",
                    choices=["320", "192", "128", "96"],
                    value="128"
                )

        # Connect sample buttons
        if audio_samples:
            for btn, path in sample_buttons:
                btn.click(
                    fn=lambda p=path: load_sample_audio(p),
                    outputs=[audio_input]
                )

        # YouTube download button
        yt_download_btn = gr.Button("📥 Download from YouTube", variant="secondary")

        # Configuration Options
        gr.Markdown("### ⚙️ Analysis Options")

        analysis_options = gr.CheckboxGroup(
            label="Select Features to Extract",
            choices=[
                "Beat Tracking",
                "Onset Detection",
                "Tempo Estimation"
            ],
            value=["Beat Tracking"],
            info="Choose which analysis to perform"
        )

        # Action Button
        analyze_btn = gr.Button("🔬 Analyze Audio", variant="primary", size="lg")

        # Results Section
        gr.Markdown("### 📊 Results")
        results_text = gr.Markdown()

        # Audio Outputs
        gr.Markdown("### 🎧 Audio Outputs")
        gr.Markdown("**Listen to detected features overlaid on original audio:**")

        with gr.Row():
            audio_output_1 = gr.Audio(
                label="Beats + Downbeats",
                type="filepath"
            )
            audio_output_2 = gr.Audio(
                label="Onsets",
                type="filepath"
            )
            audio_output_3 = gr.Audio(
                label="Additional Output",
                type="filepath"
            )

        # Help Section
        with gr.Accordion("ℹ️ Help", open=False):
            gr.Markdown("""
                **Features:**
                - 🥁 **Beat Tracking:** Detects beats/downbeats and estimates BPM
                - 🎯 **Onset Detection:** Identifies note onset events
                - ⏱️ **Tempo Estimation:** Estimates primary tempo

                **Supported:** WAV, MP3, FLAC, OGG, M4A, AAC
                **Temp files:** Check $TEMP_DIR in .env
            """)

        # Event Handlers
        yt_download_btn.click(
            fn=download_youtube_audio_ytdlp,
            inputs=[youtube_url, audio_format, audio_quality],
            outputs=[audio_input, results_text]
        )

        analyze_btn.click(
            fn=analyze_audio,
            inputs=[audio_input, analysis_options],
            outputs=[results_text, audio_output_1, audio_output_2, audio_output_3]
        )

    return demo

# === PORT UTILITIES ===

def is_port_available(port: int, host: str = "0.0.0.0") -> bool:
    """Check if a port is available."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            return True
    except OSError:
        return False

def find_available_port(start_port: int, host: str = "0.0.0.0", max_attempts: int = 100) -> int:
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(port, host):
            return port
    raise RuntimeError(f"Could not find an available port starting from {start_port}")

# === COMMAND-LINE ARGUMENTS ===

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Worzpro Demo Template - Audio Analysis Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python demo_template.py                          # Default: localhost:7860
  python demo_template.py --port 8080              # Custom port
  python demo_template.py --share                  # Public URL with Gradio share
  python demo_template.py --samples-dir ~/Music    # Custom samples directory
  python demo_template.py --cleanup-days 3         # Clean files older than 3 days
  python demo_template.py --cleanup-days 0         # Disable cleanup

Environment Variables:
  PORT           Default port (overridden by --port)
  HOST           Default host (default: 0.0.0.0)
  SAMPLES_DIR    Directory for audio samples (overridden by --samples-dir)
  TEMP_DIR       Directory for temporary files (configure in .env)
        """
    )

    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", 7860)),
        help="Port to run the server on (default: 7860 or $PORT). Must be >= 1024 (privileged ports require root)"
    )

    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("HOST", "0.0.0.0"),
        help="Host to bind to (default: 0.0.0.0 or $HOST)"
    )

    parser.add_argument(
        "--share",
        action="store_true",
        help="Create a public Gradio share link"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with auto-reload"
    )

    parser.add_argument(
        "--auto-port",
        action="store_true",
        help="Automatically find an available port if the specified port is occupied"
    )

    parser.add_argument(
        "--samples-dir",
        type=str,
        default=os.getenv("SAMPLES_DIR", "assets/audio_samples"),
        help="Directory containing audio samples (default: assets/audio_samples or $SAMPLES_DIR)"
    )

    parser.add_argument(
        "--cleanup-days",
        type=int,
        default=7,
        help="Delete temporary files older than N days (0 to disable cleanup, default: 7)"
    )

    return parser.parse_args()

def cleanup_old_files(directory: Path, days: int):
    """
    Delete files older than specified days in the given directory.

    Args:
        directory: Path to the directory to clean
        days: Files older than this many days will be deleted
    """
    if days <= 0 or not directory.exists():
        return

    import time
    cutoff_time = time.time() - (days * 86400)  # 86400 seconds = 1 day
    deleted_count = 0
    deleted_size = 0

    try:
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                # Check file modification time
                if file_path.stat().st_mtime < cutoff_time:
                    file_size = file_path.stat().st_size
                    file_path.unlink()
                    deleted_count += 1
                    deleted_size += file_size

        if deleted_count > 0:
            print(f"🧹 Cleaned up {deleted_count} files ({deleted_size / 1024 / 1024:.2f} MB) older than {days} days")
    except Exception as e:
        print(f"⚠️ Warning: Cleanup failed: {e}")

# === MAIN ===

if __name__ == "__main__":
    # Parse arguments
    args = parse_args()

    # Update SAMPLES_DIR from command-line argument
    import sys
    current_module = sys.modules[__name__]
    current_module.SAMPLES_DIR = Path(args.samples_dir).resolve()

    # TEMP_DIR is config-only (not CLI argument), ensure it exists
    current_module.SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    current_module.TEMP_DIR.mkdir(parents=True, exist_ok=True)

    # Validate port number
    if args.port < 1024:
        print(f"❌ Error: Port {args.port} is a privileged port (requires root)")
        print(f"💡 Use a port >= 1024, for example: --port 8080")
        print(f"   Or run with sudo if you need to use port {args.port}")
        exit(1)

    # Handle port conflicts
    original_port = args.port
    if args.auto_port or not is_port_available(args.port, args.host):
        if not args.auto_port:
            print(f"⚠️ Port {args.port} is already in use!")
            print("💡 Tip: Use --auto-port flag to automatically find an available port")
            print("   Or specify a different port with --port <number>")
            exit(1)
        
        print(f"🔍 Port {args.port} is occupied, searching for available port...")
        try:
            args.port = find_available_port(args.port, args.host)
            if args.port != original_port:
                print(f"✅ Found available port: {args.port}")
        except RuntimeError as e:
            print(f"❌ {e}")
            exit(1)

    print("🎵 Starting Worzpro Demo Template...")
    print(f"\n📂 Directory Configuration:")
    print(f"  • Samples: {current_module.SAMPLES_DIR}")
    print(f"  • Temp:    {current_module.TEMP_DIR}")

    # Cleanup old temporary files
    if args.cleanup_days > 0:
        print(f"\n🧹 Cleanup Configuration:")
        print(f"  • Deleting files older than {args.cleanup_days} days...")
        cleanup_old_files(current_module.TEMP_DIR, args.cleanup_days)
    else:
        print(f"\n🧹 Cleanup: Disabled")

    print(f"\n🌐 Server Configuration:")
    print(f"  • Host: {args.host}")
    print(f"  • Port: {args.port}")

    if args.share:
        print("🌍 Share: Enabled (public URL will be generated)")
    else:
        print("🌍 Share: Disabled (local only)")

    if not MADMOM_AVAILABLE:
        print("\n⚠️ Warning: Madmom not available")
        print("   Install with: uv add madmom")
        print("   Or replace with your own audio library\n")

    # Configure allowed paths for file serving (CRITICAL for --share and public URLs)
    allowed_paths = [
        str(current_module.SAMPLES_DIR),
        str(current_module.TEMP_DIR),
        os.path.join(tempfile.gettempdir(), 'gradio'),
        tempfile.gettempdir()
    ]
    os.environ['GRADIO_ALLOWED_PATHS'] = ':'.join(allowed_paths)
    print(f"🔐 GRADIO_ALLOWED_PATHS configured: {len(allowed_paths)} directories")

    # Create demo
    demo = create_demo()

    # Launch with configuration
    demo.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        show_error=True,
        debug=args.debug
    )

    print(f"\n🎉 Demo running at: http://{args.host}:{args.port}")
    if args.share:
        print("📡 Public URL will appear above")
