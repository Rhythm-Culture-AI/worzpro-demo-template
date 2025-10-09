# Customization Guide

Quick guide to adapt this template for your own audio processing demo.

---

## 🎯 What to Modify

**Must Change:**
- Section 1: Configuration (lines 45-69)
- Section 4: Core Analysis Function (lines 201-382)
- Section 5: Demo Interface (lines 384-521)

**Keep As-Is:**
- Section 2: UI Helpers (sample discovery, file loading)
- Section 3: YouTube Download (yt-dlp integration)
- Sections 6-8: Port utilities, CLI args, main setup

---

## 📝 Step-by-Step Customization

### Step 1: Replace Library Imports (Lines 34-43)

**Remove madmom imports:**
```python
# === EXAMPLE: Madmom-specific imports (replace with your library) ===
try:
    from madmom.features.downbeats import DBNDownBeatTrackingProcessor, RNNDownBeatProcessor
    # ... more madmom imports
    MADMOM_AVAILABLE = True
except ImportError:
    MADMOM_AVAILABLE = False
    print("⚠️ Madmom not available. Install with: uv add madmom")
```

**Replace with your library:**
```python
# === YOUR LIBRARY IMPORTS ===
try:
    # Example: Using librosa
    import librosa
    from librosa import feature, onset
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    print("⚠️ Librosa not available. Install with: pip install librosa")
```

---

### Step 2: Update Configuration (Lines 45-69)

**Update app title and description:**
```python
# UI Configuration
APP_TITLE = "Your Audio Analysis Tool"  # ← Change this
APP_DESCRIPTION = """
# 🎵 Your Custom Audio Analyzer

Your description here...
"""  # ← Change this
```

**Optional: Customize directories:**
```python
SAMPLES_DIR = Path(os.getenv('SAMPLES_DIR', 'my_samples')).resolve()
OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR', 'my_outputs')).resolve()
```

---

### Step 3: Rewrite Analysis Function (Lines 201-382)

This is the **core** - replace the entire `analyze_audio()` function.

#### Basic Template:

```python
def analyze_audio(audio_file, analysis_options):
    """Your audio analysis logic."""

    # 1. Validation
    if audio_file is None:
        return "❌ Please upload an audio file first.", None, None, None

    if not YOUR_LIBRARY_AVAILABLE:
        return "# ❌ Error\n\nYour library not available.", None, None, None

    try:
        # 2. Load audio
        audio, sr = sf.read(audio_file)
        file_path = Path(audio_file)
        duration = len(audio) / sr

        # 3. Initialize results
        results = {}
        audio_outputs = {}

        # 4. YOUR ANALYSIS LOGIC HERE
        if "Your Feature 1" in analysis_options:
            # Run your analysis
            result = your_analysis_function(audio, sr)
            results['feature1'] = result

            # Optional: Create audio output
            output_path = OUTPUT_DIR / f"feature1_{int(time.time())}.wav"
            # ... save modified audio
            audio_outputs['feature1'] = str(output_path)

        if "Your Feature 2" in analysis_options:
            # Another analysis
            pass

        # 5. Format results as markdown
        result_text = f"""
# 🎵 Analysis Results

## 📁 File Info
- **File:** `{file_path.name}`
- **Duration:** `{duration:.2f}s`
- **Sample Rate:** `{sr} Hz`

## Your Results Section
- **Your Metric:** `{results['feature1']['value']}`

---
✅ **Analysis complete!**
        """

        # 6. Return: (markdown, audio1, audio2, audio3)
        return (
            result_text,
            audio_outputs.get('feature1'),
            audio_outputs.get('feature2'),
            None
        )

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return f"# ❌ Error\n\n**Failed:** `{str(e)}`", None, None, None
```

---

### Step 4: Update Demo Interface (Lines 489-501)

**Change analysis options:**
```python
# Configuration Options
gr.Markdown("### ⚙️ Analysis Options")

analysis_options = gr.CheckboxGroup(
    label="Select Features to Extract",
    choices=[
        "Your Feature 1",      # ← Change these
        "Your Feature 2",      # ← Change these
        "Your Feature 3"       # ← Change these
    ],
    value=["Your Feature 1"],  # ← Default selection
    info="Choose which analysis to perform"
)
```

**Optional: Update audio output labels (lines 514-526):**
```python
with gr.Row():
    audio_output_1 = gr.Audio(
        label="Your Output 1",  # ← Change label
        type="filepath"
    )
    audio_output_2 = gr.Audio(
        label="Your Output 2",  # ← Change label
        type="filepath"
    )
    audio_output_3 = gr.Audio(
        label="Your Output 3",  # ← Change label
        type="filepath"
    )
```

**Optional: Update help text (lines 528-537):**
```python
with gr.Accordion("ℹ️ Help", open=False):
    gr.Markdown("""
        **Features:**
        - 🎵 **Your Feature 1:** Description here
        - 🎤 **Your Feature 2:** Description here

        **Supported:** WAV, MP3, FLAC, OGG, M4A, AAC
    """)
```

---

## 🔥 Common Patterns

### Pattern 1: Single Feature, No Options

Remove the checkbox, analyze directly:

```python
# Remove analysis_options checkbox group

# In analyze_audio():
def analyze_audio(audio_file):  # ← Remove analysis_options param
    # Just run your analysis
    result = your_function(audio, sr)
    # ...

# Update event handler:
analyze_btn.click(
    fn=analyze_audio,
    inputs=[audio_input],  # ← No analysis_options
    outputs=[results_text, audio_output_1, audio_output_2, audio_output_3]
)
```

---

### Pattern 2: Additional Input Controls

Add custom controls (sliders, dropdowns, etc.):

```python
# Add after "Analysis Options" section:
with gr.Row():
    threshold = gr.Slider(
        label="Threshold",
        minimum=0.0,
        maximum=1.0,
        value=0.5,
        step=0.1
    )
    window_size = gr.Dropdown(
        label="Window Size",
        choices=["512", "1024", "2048"],
        value="1024"
    )

# Update analyze_audio signature:
def analyze_audio(audio_file, analysis_options, threshold, window_size):
    # Use threshold and window_size in your analysis
    pass

# Update event handler:
analyze_btn.click(
    fn=analyze_audio,
    inputs=[audio_input, analysis_options, threshold, window_size],
    outputs=[results_text, audio_output_1, audio_output_2, audio_output_3]
)
```

---

### Pattern 3: Visualization (Plot) Instead of Audio Output

Replace audio output with a plot:

```python
# Replace audio_output_1 with plot:
with gr.Row():
    plot_output = gr.Plot(label="Analysis Visualization")
    audio_output_2 = gr.Audio(label="Processed Audio", type="filepath")

# In analyze_audio():
import matplotlib.pyplot as plt

def analyze_audio(audio_file, analysis_options):
    # ... your analysis

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(your_data)
    ax.set_title("Your Analysis")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Value")

    # Return plot instead of audio
    return result_text, fig, audio_output, None

# Update outputs:
analyze_btn.click(
    fn=analyze_audio,
    inputs=[audio_input, analysis_options],
    outputs=[results_text, plot_output, audio_output_2, audio_output_3]
)
```

---

### Pattern 4: No Audio Outputs (Text Only)

Simplify for text-only results:

```python
# Remove all audio_output components (lines 510-526)

# Simplify return in analyze_audio():
def analyze_audio(audio_file, analysis_options):
    # ... analysis
    return result_text  # ← Return only markdown

# Simplify event handler:
analyze_btn.click(
    fn=analyze_audio,
    inputs=[audio_input, analysis_options],
    outputs=[results_text]  # ← Only one output
)
```

---

## 📦 Example: Complete Custom Demo

**Scenario:** Pitch detection with librosa

```python
# === LIBRARY IMPORTS ===
try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    print("⚠️ Librosa not available")

# === CONFIGURATION ===
APP_TITLE = "Pitch Detector"
APP_DESCRIPTION = """
# 🎵 Audio Pitch Detector

Detect the fundamental frequency (pitch) of audio signals.
"""

# === ANALYSIS FUNCTION ===
def analyze_audio(audio_file):
    if audio_file is None:
        return "❌ Please upload audio first."

    if not LIBROSA_AVAILABLE:
        return "# ❌ Error\n\nLibrosa not available."

    try:
        # Load audio
        audio, sr = librosa.load(audio_file)

        # Pitch detection
        pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
        pitch_values = []

        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)

        avg_pitch = sum(pitch_values) / len(pitch_values) if pitch_values else 0

        result = f"""
# 🎵 Pitch Analysis

- **Average Pitch:** `{avg_pitch:.2f} Hz`
- **Pitch Range:** `{min(pitch_values):.2f} - {max(pitch_values):.2f} Hz`
- **Frames Detected:** `{len(pitch_values)}`

✅ **Done!**
        """

        return result

    except Exception as e:
        return f"# ❌ Error\n\n`{str(e)}`"

# === DEMO INTERFACE ===
def create_demo():
    with gr.Blocks(title=APP_TITLE, theme=gr.themes.Soft()) as demo:
        gr.Markdown(APP_DESCRIPTION)

        audio_input = gr.Audio(label="Upload Audio", type="filepath")
        analyze_btn = gr.Button("🔬 Analyze Pitch", variant="primary")
        results_text = gr.Markdown()

        analyze_btn.click(
            fn=analyze_audio,
            inputs=[audio_input],
            outputs=[results_text]
        )

    return demo
```

---

## ✅ Testing Checklist

After customization, test:

- [ ] **Local:** `python demo_template.py`
  - Upload a file → Analyze → Check results
  - Sample buttons work (if you kept them)
  - YouTube download works (if you kept it)

- [ ] **Public URL (IMPORTANT):** `python demo_template.py --share`
  - **Why test with --share?** This catches file serving issues that only appear on public URLs
  - All features work on shared URL
  - Files load correctly (no 404 errors in browser console)
  - Open browser DevTools → Network tab and check for failed file requests

- [ ] **Error Handling:**
  - Upload invalid file
  - Click analyze with no file
  - Test with different audio formats

---

## 💡 Tips

1. **Start Simple:** Get basic analysis working first, then add features
2. **Keep Sample Discovery:** Users love being able to try examples
3. **Keep YouTube Download:** Very convenient for testing
4. **Test with --share:** Catches file serving issues early
5. **Use Absolute Paths:** Already configured in template (lines 48-49)

---

## 📚 Related Files

- `QUICKSTART.md` - How to run the template
- `README.md` - Project overview
- `.env.example` - Environment variables

---

**Need help?** Check the template comments or see example implementations in the worzpro-demo repository.
