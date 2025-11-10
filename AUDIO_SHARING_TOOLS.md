# Audio Sharing Tools for AudioTools

This document describes the audio sharing capabilities in AudioTools.

## Overview

AudioTools provides several methods for sharing and comparing audio files:

1. **HTML Audio Tables** - Interactive web-based audio comparisons
2. **Audio Reports** - Detailed analysis with statistics and visualizations
3. **Multi-format Export** - Export audio with metadata in various formats
4. **Batch Processing** - Process and share multiple files

## Quick Start

### 1. HTML Audio Comparison Table

Create an interactive HTML table to compare different audio versions:

```python
from audiotools import AudioSignal, post

# Load audio and create variations
original = AudioSignal("audio.wav")
audio_dict = {
    "Original": original,
    "Low-passed": original.clone().low_pass(4000),
    "Normalized": original.clone().normalize(db=-20),
}

# Generate HTML table
table_html = post.audio_table(audio_dict, first_column="Version")

# Save to file
with open("comparison.html", 'w') as f:
    f.write(f"<html><body>{table_html}</body></html>")
```

### 2. Using the Command-Line Tool

```bash
# Compare multiple files
python audio_sharing_tools.py --mode table --input file1.wav file2.wav file3.wav

# Create detailed report
python audio_sharing_tools.py --mode report --input original.wav processed.wav --output report_dir

# Export with metadata
python audio_sharing_tools.py --mode export --input audio.wav --output export_dir

# Batch process directory
python audio_sharing_tools.py --mode batch --input audio_folder/ --output batch_results
```

## Features

### HTML Audio Tables

Generate interactive HTML tables with embedded audio players:

```python
from audiotools import post, AudioSignal

audio_dict = {
    "Version 1": AudioSignal("v1.wav"),
    "Version 2": AudioSignal("v2.wav"),
}

# Create table with custom column header
html = post.audio_table(audio_dict, first_column="Version")
```

**Features:**
- Embedded HTML5 audio players
- Side-by-side comparison
- Supports any AudioSignal object
- Automatic formatting

### Audio Reports

Create comprehensive analysis reports:

```python
from audio_sharing_tools import create_audio_report

original = "original.wav"
processed = {
    "Version A": "processed_a.wav",
    "Version B": "processed_b.wav",
}

create_audio_report(original, processed, output_dir="report")
```

**Report includes:**
- Audio statistics table
- Loudness measurements (LUFS)
- Sample rate and duration info
- Max amplitude analysis
- Embedded audio players

### Multi-Format Export

Export audio with comprehensive metadata:

```python
from audio_sharing_tools import export_with_metadata

export_with_metadata(
    "input.wav",
    output_dir="exports",
    formats=["wav", "mp3"]
)
```

**Exports include:**
- Audio in specified formats
- Metadata text file with:
  - Duration
  - Sample rate
  - Loudness (LUFS)
  - Amplitude statistics
  - Signal properties

### Batch Processing

Process multiple files and create a sharing package:

```python
from audio_sharing_tools import batch_process_and_share

batch_process_and_share(
    input_dir="audio_files/",
    output_dir="batch_results/",
    transforms=["normalize", "lowpass"]
)
```

**Features:**
- Process multiple files at once
- Apply consistent transforms
- Generate comparison HTML
- Statistics for all files

## Examples

See `examples/audio_sharing_demo.py` for complete working examples:

```bash
python examples/audio_sharing_demo.py
```

This runs 4 demos:
1. HTML audio table creation
2. Audio with detailed statistics
3. Batch processing comparison
4. Multi-format export

## Use Cases

### 1. Audio Processing Comparison

Compare different processing methods:

```python
original = AudioSignal("speech.wav", duration=5.0)

comparisons = {
    "Original": original,
    "Normalized": original.clone().normalize(db=-20),
    "De-noised": original.clone().low_pass(4000),
    "Enhanced": original.clone().normalize(-20).low_pass(8000),
}

html = post.audio_table(comparisons)
```

### 2. A/B Testing

Create A/B tests for audio quality:

```python
# Create test files
test_dict = {
    "Model A": AudioSignal("model_a_output.wav"),
    "Model B": AudioSignal("model_b_output.wav"),
    "Ground Truth": AudioSignal("reference.wav"),
}

# Generate comparison page
html = post.audio_table(test_dict, first_column="System")
```

### 3. Dataset Sharing

Share processed datasets with documentation:

```python
from audio_sharing_tools import batch_process_and_share

# Process entire dataset
batch_process_and_share(
    input_dir="dataset/",
    output_dir="processed_dataset/",
    transforms=["normalize", "resample"]
)
```

### 4. Audio Quality Reports

Generate quality reports for audio files:

```python
signal = AudioSignal("audio.wav")

stats = {
    "Duration": f"{signal.duration:.2f}s",
    "Sample Rate": f"{signal.sample_rate} Hz",
    "Loudness": f"{signal.loudness().item():.2f} LUFS",
    "Max Amplitude": f"{signal.audio_data.abs().max().item():.4f}",
}

# Save stats with audio
```

## API Reference

### `post.audio_table(audio_dict, first_column=None, format_fn=None)`

Create HTML table from audio dictionary.

**Parameters:**
- `audio_dict`: Dict of {name: AudioSignal} or {name: dict} with audio and metadata
- `first_column`: Label for first column (default: ".")
- `format_fn`: Custom formatting function for cells

**Returns:** HTML string with markdown table

### `post.disp(obj, **kwargs)`

Display audio in notebooks or terminal.

**Parameters:**
- `obj`: AudioSignal, dict, or matplotlib Figure
- `**kwargs`: Additional arguments for formatting

### Utility Functions

```python
from audiotools.core import util

# Find audio files
files = util.find_audio("folder/", ext=["wav", "mp3"])

# Convert Hz to FFT bins
bins = util.hz_to_bin(frequencies, n_fft, sample_rate)

# Sample from distribution
value = util.sample_from_dist(("uniform", 0, 1), state=42)

# Set random seed
util.seed(42)
```

## Tips and Best Practices

1. **Keep audio short for web sharing** - Use `.excerpt(duration=3.0)` to create shorter clips
2. **Normalize before comparison** - Use `.normalize(db=-20)` for fair comparisons
3. **Use consistent sample rates** - Resample all files to the same rate
4. **Include metadata** - Always export with statistics and descriptions
5. **Test in browser** - Check HTML output in multiple browsers

## Advanced Usage

### Custom Audio Table Formatting

```python
def custom_format(label, audio_signal):
    if isinstance(audio_signal, AudioSignal):
        loudness = audio_signal.loudness().item()
        return f"{audio_signal.embed()} (Loudness: {loudness:.1f} LUFS)"
    return str(audio_signal)

html = post.audio_table(audio_dict, format_fn=custom_format)
```

### Creating Shareable Packages

```python
import zipfile
from pathlib import Path

# Process and export
output_dir = Path("audio_package")
output_dir.mkdir(exist_ok=True)

# Add audio files
for name, signal in audio_dict.items():
    signal.write(output_dir / f"{name}.wav")

# Add metadata
with open(output_dir / "README.txt", 'w') as f:
    f.write("Audio Package Contents\n")
    # Add descriptions

# Create zip
with zipfile.ZipFile("audio_package.zip", 'w') as zf:
    for file in output_dir.glob("*"):
        zf.write(file, file.name)
```

## Requirements

- audiotools
- torch
- numpy
- matplotlib (for visualizations)

## License

Same as AudioTools main license.

## Contributing

Contributions welcome! Please see main AudioTools contributing guidelines.
