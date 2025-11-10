#!/usr/bin/env python3
"""
Audio Sharing Tools for AudioTools

This script demonstrates various methods for sharing and comparing audio files:
1. Generate HTML audio tables for web sharing
2. Create audio comparison reports
3. Export audio with metadata
4. Batch audio processing and sharing

Usage:
    python audio_sharing_tools.py --mode [table|report|export|batch]
"""

import argparse
import tempfile
from pathlib import Path
from typing import List, Dict
import os

from audiotools import AudioSignal, post, util


def create_audio_table(audio_paths: List[str], output_html: str = "audio_table.html"):
    """
    Create an HTML table comparing multiple audio files.

    Args:
        audio_paths: List of paths to audio files
        output_html: Output HTML file path
    """
    print("=" * 60)
    print("CREATING AUDIO COMPARISON TABLE")
    print("=" * 60)

    audio_dict = {}

    for i, path in enumerate(audio_paths):
        signal = AudioSignal(path)
        audio_dict[f"Audio {i+1}: {Path(path).name}"] = {
            "signal": signal,
            "duration": f"{signal.duration:.2f}s",
            "sample_rate": f"{signal.sample_rate} Hz",
            "channels": signal.num_channels,
        }

    # Generate HTML table
    html_content = post.audio_table(audio_dict, first_column="File")

    # Wrap in complete HTML document
    full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Audio Comparison Table</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 20px auto;
            padding: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 10px;
            border: 1px solid #ddd;
            text-align: left;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        audio {{
            width: 100%;
        }}
    </style>
</head>
<body>
    <h1>Audio Comparison Table</h1>
    {html_content}
</body>
</html>
"""

    with open(output_html, 'w') as f:
        f.write(full_html)

    print(f"\n✓ HTML table created: {output_html}")
    print(f"  Files compared: {len(audio_paths)}")
    print(f"  Open in browser to view")

    return output_html


def create_audio_report(
    original_path: str,
    processed_paths: Dict[str, str],
    output_dir: str = "audio_report"
):
    """
    Create a comprehensive audio comparison report.

    Args:
        original_path: Path to original audio
        processed_paths: Dict of {name: path} for processed versions
        output_dir: Output directory for report
    """
    print("=" * 60)
    print("CREATING AUDIO COMPARISON REPORT")
    print("=" * 60)

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Load original
    original = AudioSignal(original_path)

    # Process and analyze
    results = {
        "Original": {
            "signal": original,
            "duration": original.duration,
            "sample_rate": original.sample_rate,
            "loudness": original.loudness().item(),
            "max_amplitude": original.audio_data.abs().max().item(),
        }
    }

    for name, path in processed_paths.items():
        signal = AudioSignal(path)
        results[name] = {
            "signal": signal,
            "duration": signal.duration,
            "sample_rate": signal.sample_rate,
            "loudness": signal.loudness().item(),
            "max_amplitude": signal.audio_data.abs().max().item(),
        }

    # Generate report HTML
    html_lines = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "    <title>Audio Analysis Report</title>",
        "    <style>",
        "        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 20px auto; padding: 20px; }",
        "        h1 { color: #333; }",
        "        h2 { color: #666; margin-top: 30px; }",
        "        table { width: 100%; border-collapse: collapse; margin: 20px 0; }",
        "        th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }",
        "        th { background-color: #4CAF50; color: white; }",
        "        .metric { font-weight: bold; }",
        "        audio { width: 100%; margin: 10px 0; }",
        "    </style>",
        "</head>",
        "<body>",
        "    <h1>Audio Analysis Report</h1>",
        f"    <p>Generated: {util.find_audio.__module__}</p>",
    ]

    # Add statistics table
    html_lines.extend([
        "    <h2>Audio Statistics</h2>",
        "    <table>",
        "        <tr>",
        "            <th>Version</th>",
        "            <th>Duration (s)</th>",
        "            <th>Sample Rate (Hz)</th>",
        "            <th>Loudness (LUFS)</th>",
        "            <th>Max Amplitude</th>",
        "        </tr>",
    ])

    for name, data in results.items():
        html_lines.append("        <tr>")
        html_lines.append(f"            <td class='metric'>{name}</td>")
        html_lines.append(f"            <td>{data['duration']:.3f}</td>")
        html_lines.append(f"            <td>{data['sample_rate']}</td>")
        html_lines.append(f"            <td>{data['loudness']:.2f}</td>")
        html_lines.append(f"            <td>{data['max_amplitude']:.4f}</td>")
        html_lines.append("        </tr>")

    html_lines.extend([
        "    </table>",
        "    <h2>Audio Players</h2>",
    ])

    # Add audio players
    for name, data in results.items():
        audio_path = output_dir / f"{name.lower().replace(' ', '_')}.wav"
        data['signal'].write(audio_path)
        html_lines.extend([
            f"    <h3>{name}</h3>",
            f"    <audio controls src='{audio_path.name}'></audio>",
        ])

    html_lines.extend([
        "</body>",
        "</html>",
    ])

    # Write report
    report_path = output_dir / "report.html"
    with open(report_path, 'w') as f:
        f.write('\n'.join(html_lines))

    print(f"\n✓ Report created: {report_path}")
    print(f"  Versions analyzed: {len(results)}")
    print(f"  Audio files exported: {len(results)}")

    return report_path


def export_with_metadata(
    audio_path: str,
    output_dir: str = "audio_export",
    formats: List[str] = ["wav", "mp3"]
):
    """
    Export audio in multiple formats with metadata.

    Args:
        audio_path: Input audio path
        output_dir: Output directory
        formats: List of formats to export
    """
    print("=" * 60)
    print("EXPORTING AUDIO WITH METADATA")
    print("=" * 60)

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Load signal
    signal = AudioSignal(audio_path)

    # Get metadata
    metadata = {
        "source": audio_path,
        "duration": f"{signal.duration:.3f}s",
        "sample_rate": f"{signal.sample_rate} Hz",
        "channels": signal.num_channels,
        "loudness": f"{signal.loudness().item():.2f} LUFS",
        "max_amplitude": f"{signal.audio_data.abs().max().item():.4f}",
        "signal_length": signal.signal_length,
    }

    # Export in different formats
    base_name = Path(audio_path).stem
    exported_files = []

    for fmt in formats:
        output_path = output_dir / f"{base_name}.{fmt}"
        signal.write(output_path)
        exported_files.append(output_path)
        print(f"  ✓ Exported: {output_path}")

    # Write metadata file
    metadata_path = output_dir / f"{base_name}_metadata.txt"
    with open(metadata_path, 'w') as f:
        f.write("Audio Metadata\n")
        f.write("=" * 40 + "\n\n")
        for key, value in metadata.items():
            f.write(f"{key.replace('_', ' ').title()}: {value}\n")

    print(f"\n✓ Metadata saved: {metadata_path}")
    print(f"\nExport Summary:")
    print(f"  Formats: {', '.join(formats)}")
    print(f"  Files created: {len(exported_files) + 1}")

    return exported_files, metadata_path


def batch_process_and_share(
    input_dir: str,
    output_dir: str = "batch_output",
    transforms: List[str] = ["normalize", "lowpass"]
):
    """
    Batch process multiple audio files and create sharing package.

    Args:
        input_dir: Directory containing audio files
        output_dir: Output directory
        transforms: List of transforms to apply
    """
    print("=" * 60)
    print("BATCH PROCESSING AUDIO FILES")
    print("=" * 60)

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Find audio files
    audio_files = util.find_audio(input_dir, ext=["wav", "mp3"])

    if not audio_files:
        print(f"No audio files found in {input_dir}")
        return

    print(f"\nFound {len(audio_files)} audio files")

    results = {}

    for audio_file in audio_files[:5]:  # Process first 5 files
        print(f"\nProcessing: {audio_file.name}")

        signal = AudioSignal(audio_file)
        original = signal.clone()

        # Apply transforms
        if "normalize" in transforms:
            signal = signal.normalize(db=-20)
            print(f"  ✓ Normalized to -20 LUFS")

        if "lowpass" in transforms:
            signal = signal.low_pass(8000)
            print(f"  ✓ Low-pass filtered at 8kHz")

        if "resample" in transforms:
            signal = signal.resample(44100)
            print(f"  ✓ Resampled to 44.1kHz")

        # Save processed version
        output_path = output_dir / f"processed_{audio_file.name}"
        signal.write(output_path)

        results[audio_file.stem] = {
            "original": original,
            "processed": signal,
            "transforms": transforms,
        }

    # Create comparison HTML
    html_lines = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "    <title>Batch Processing Results</title>",
        "    <style>",
        "        body { font-family: Arial, sans-serif; max-width: 1400px; margin: 20px auto; padding: 20px; }",
        "        .file-block { border: 1px solid #ddd; padding: 20px; margin: 20px 0; }",
        "        .file-block h2 { color: #333; }",
        "        audio { width: 100%; margin: 10px 0; }",
        "        .transforms { background: #f0f0f0; padding: 10px; margin: 10px 0; }",
        "    </style>",
        "</head>",
        "<body>",
        "    <h1>Batch Processing Results</h1>",
        f"    <p>Processed {len(results)} files with transforms: {', '.join(transforms)}</p>",
    ]

    for name, data in results.items():
        html_lines.extend([
            f"    <div class='file-block'>",
            f"        <h2>{name}</h2>",
            f"        <div class='transforms'>Transforms: {', '.join(data['transforms'])}</div>",
            f"        <h3>Original</h3>",
            f"        <p>Duration: {data['original'].duration:.2f}s | Loudness: {data['original'].loudness().item():.2f} LUFS</p>",
            f"        <h3>Processed</h3>",
            f"        <p>Duration: {data['processed'].duration:.2f}s | Loudness: {data['processed'].loudness().item():.2f} LUFS</p>",
            f"        <audio controls src='processed_{name}.wav'></audio>",
            f"    </div>",
        ])

    html_lines.extend([
        "</body>",
        "</html>",
    ])

    index_path = output_dir / "index.html"
    with open(index_path, 'w') as f:
        f.write('\n'.join(html_lines))

    print(f"\n✓ Batch processing complete!")
    print(f"  Output directory: {output_dir}")
    print(f"  Index file: {index_path}")
    print(f"  Files processed: {len(results)}")

    return index_path


def main():
    parser = argparse.ArgumentParser(description="Audio Sharing Tools for AudioTools")
    parser.add_argument(
        "--mode",
        choices=["table", "report", "export", "batch"],
        default="table",
        help="Sharing mode to use"
    )
    parser.add_argument(
        "--input",
        nargs="+",
        help="Input audio file(s) or directory"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output path/directory"
    )

    args = parser.parse_args()

    # Use example files if no input provided
    if not args.input:
        print("No input provided, using example files from tests/")
        example_files = util.find_audio("tests/audio/spk", ext=["wav"])[:3]
        args.input = [str(f) for f in example_files]

    if args.mode == "table":
        output = args.output or "audio_comparison_table.html"
        create_audio_table(args.input, output)

    elif args.mode == "report":
        if len(args.input) < 2:
            print("Report mode requires at least 2 files (original + processed)")
            return

        original = args.input[0]
        processed = {f"Version {i}": path for i, path in enumerate(args.input[1:], 1)}
        output = args.output or "audio_report"
        create_audio_report(original, processed, output)

    elif args.mode == "export":
        for audio_file in args.input:
            output = args.output or "audio_export"
            export_with_metadata(audio_file, output)

    elif args.mode == "batch":
        input_dir = args.input[0] if len(args.input) == 1 else "tests/audio/spk"
        output = args.output or "batch_output"
        batch_process_and_share(input_dir, output)


if __name__ == "__main__":
    main()
