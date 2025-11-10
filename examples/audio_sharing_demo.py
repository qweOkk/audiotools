#!/usr/bin/env python3
"""
Audio Sharing Demo

Simple examples demonstrating the audio sharing capabilities of AudioTools.
"""

from audiotools import AudioSignal, post, util
from pathlib import Path


def demo_1_html_audio_table():
    """Demo 1: Create an HTML table for comparing audio files."""
    print("\n" + "=" * 60)
    print("DEMO 1: HTML Audio Comparison Table")
    print("=" * 60)

    # Load multiple audio files
    audio_files = util.find_audio("tests/audio/spk", ext=["wav"])[:1]

    if not audio_files:
        print("No audio files found!")
        return

    # Load original
    original = AudioSignal(audio_files[0])

    # Create variations
    audio_dict = {
        "Original": original.excerpt(duration=3.0),
        "Low-passed (4kHz)": original.clone().low_pass(4000).excerpt(duration=3.0),
        "High-passed (500Hz)": original.clone().high_pass(500).excerpt(duration=3.0),
        "Normalized (-20 LUFS)": original.clone().normalize(db=-20).excerpt(duration=3.0),
    }

    # Generate HTML table
    table_html = post.audio_table(audio_dict, first_column="Version")

    # Save to file
    output_file = "/tmp/audio_comparison.html"
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Audio Comparison</title>
    <style>
        body {{ font-family: Arial; max-width: 1200px; margin: 20px auto; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 10px; border: 1px solid #ddd; }}
        th {{ background-color: #4CAF50; color: white; }}
    </style>
</head>
<body>
    <h1>Audio Processing Comparison</h1>
    {table_html}
</body>
</html>"""

    with open(output_file, 'w') as f:
        f.write(full_html)

    print(f"\n✓ Created HTML table: {output_file}")
    print(f"  Variations: {len(audio_dict)}")
    print(f"  Open in browser to listen and compare!")


def demo_2_audio_with_stats():
    """Demo 2: Share audio with detailed statistics."""
    print("\n" + "=" * 60)
    print("DEMO 2: Audio with Statistics")
    print("=" * 60)

    # Load audio
    audio_path = "tests/audio/spk/f10_script4_produced.wav"
    signal = AudioSignal(audio_path, duration=5.0)

    # Calculate statistics
    stats = {
        "Duration": f"{signal.duration:.3f}s",
        "Sample Rate": f"{signal.sample_rate} Hz",
        "Channels": signal.num_channels,
        "Signal Length": f"{signal.signal_length:,} samples",
        "Loudness": f"{signal.loudness().item():.2f} LUFS",
        "Max Amplitude": f"{signal.audio_data.abs().max().item():.4f}",
        "Mean Amplitude": f"{signal.audio_data.abs().mean().item():.4f}",
        "Min Value": f"{signal.audio_data.min().item():.4f}",
        "Max Value": f"{signal.audio_data.max().item():.4f}",
    }

    print("\nAudio Statistics:")
    print("-" * 60)
    for key, value in stats.items():
        print(f"  {key:.<30} {value}")

    # Export with metadata
    output_dir = Path("/tmp/audio_export")
    output_dir.mkdir(exist_ok=True)

    # Save audio
    output_wav = output_dir / "audio_sample.wav"
    signal.write(output_wav)

    # Save metadata
    metadata_file = output_dir / "metadata.txt"
    with open(metadata_file, 'w') as f:
        f.write("Audio File Metadata\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Source: {audio_path}\n\n")
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")

    print(f"\n✓ Audio exported: {output_wav}")
    print(f"✓ Metadata saved: {metadata_file}")


def demo_3_batch_comparison():
    """Demo 3: Batch compare multiple processing methods."""
    print("\n" + "=" * 60)
    print("DEMO 3: Batch Processing Comparison")
    print("=" * 60)

    # Load original
    audio_path = "tests/audio/spk/f10_script4_produced.wav"
    original = AudioSignal(audio_path, offset=10, duration=3.0)

    # Define processing methods
    processing_methods = {
        "Original": lambda s: s,
        "Normalize -20dB": lambda s: s.normalize(db=-20),
        "Low-pass 4kHz": lambda s: s.low_pass(4000),
        "High-pass 200Hz": lambda s: s.high_pass(200),
        "Volume +6dB": lambda s: s.volume_change(db=6),
        "Pitch +3 semitones": lambda s: s.pitch_shift(n_semitones=3),
    }

    # Process and collect results
    results = []
    for name, process_fn in processing_methods.items():
        processed = process_fn(original.clone())
        loudness = processed.loudness().item()
        max_amp = processed.audio_data.abs().max().item()

        results.append({
            "Method": name,
            "Loudness (LUFS)": f"{loudness:.2f}",
            "Max Amplitude": f"{max_amp:.4f}",
            "Duration (s)": f"{processed.duration:.3f}",
        })

    # Print comparison table
    print("\nProcessing Comparison:")
    print("-" * 80)
    print(f"{'Method':<25} {'Loudness (LUFS)':<20} {'Max Amplitude':<20} {'Duration (s)':<15}")
    print("-" * 80)

    for result in results:
        print(f"{result['Method']:<25} {result['Loudness (LUFS)']:<20} "
              f"{result['Max Amplitude']:<20} {result['Duration (s)']:<15}")

    print("-" * 80)
    print(f"\n✓ Compared {len(processing_methods)} processing methods")


def demo_4_export_multiple_formats():
    """Demo 4: Export audio in multiple formats."""
    print("\n" + "=" * 60)
    print("DEMO 4: Multi-Format Export")
    print("=" * 60)

    # Load and process audio
    audio_path = "tests/audio/spk/f10_script4_produced.wav"
    signal = AudioSignal(audio_path, duration=3.0)
    signal = signal.normalize(db=-20)

    # Export in multiple formats
    output_dir = Path("/tmp/multi_format_export")
    output_dir.mkdir(exist_ok=True)

    formats = {
        "wav": "Uncompressed WAV",
        "mp3": "MP3 (compressed)",
    }

    exported_files = []
    for fmt, description in formats.items():
        output_file = output_dir / f"audio_sample.{fmt}"
        signal.write(output_file)
        file_size = output_file.stat().st_size / 1024  # KB

        exported_files.append({
            "Format": fmt.upper(),
            "Description": description,
            "File": output_file.name,
            "Size": f"{file_size:.1f} KB",
        })

        print(f"  ✓ Exported {fmt.upper()}: {output_file} ({file_size:.1f} KB)")

    print(f"\n✓ Total files exported: {len(exported_files)}")
    print(f"  Output directory: {output_dir}")


def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print("AudioTools - Audio Sharing Demos")
    print("=" * 60)

    demos = [
        demo_1_html_audio_table,
        demo_2_audio_with_stats,
        demo_3_batch_comparison,
        demo_4_export_multiple_formats,
    ]

    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"\n✗ Error in {demo.__name__}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print("All demos completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
