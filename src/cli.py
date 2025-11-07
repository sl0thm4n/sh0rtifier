"""
sh0rtifier - CLI Interface

Command-line interface for converting videos to YouTube Shorts format.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

from core import (
    ConversionOptions,
    ProcessingError,
    ValidationError,
    convert_to_shorts,
    get_video_info,
)

# Supported video extensions
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm"}


def find_videos(folder: Path) -> list[Path]:
    """
    Find all video files in folder

    Args:
        folder: Folder path to search

    Returns:
        List of video file paths
    """
    if not folder.exists():
        return []

    videos = []
    for ext in VIDEO_EXTENSIONS:
        videos.extend(folder.glob(f"*{ext}"))
        videos.extend(folder.glob(f"*{ext.upper()}"))

    return sorted(videos)


def paginate_list(items: list, page_size: int = 10) -> list[list]:
    """
    Split list into pages

    Args:
        items: List of items
        page_size: Items per page

    Returns:
        List of pages
    """
    pages = []
    for i in range(0, len(items), page_size):
        pages.append(items[i : i + page_size])
    return pages


def select_video_interactive(input_folder: Path) -> Optional[Path]:
    """
    Interactive video selection with pagination

    Args:
        input_folder: Folder containing videos

    Returns:
        Selected video path or None
    """
    videos = find_videos(input_folder)

    if not videos:
        print(f"❌ No video files found in: {input_folder}")
        return None

    pages = paginate_list(videos, page_size=10)
    current_page = 0

    while True:
        print(f"\n{'='*60}")
        print(f"Videos in '{input_folder.name}' (Page {current_page + 1}/{len(pages)})")
        print(f"{'='*60}")

        page_videos = pages[current_page]
        for i, video in enumerate(page_videos, start=1):
            idx = current_page * 10 + i
            # Get video duration
            try:
                info = get_video_info(video)
                duration_str = f"{info.duration:.1f}s"
                size_str = f"{video.stat().st_size / 1024 / 1024:.1f}MB"
                print(f"[{idx:2d}] {video.name:<40} {duration_str:>8} {size_str:>10}")
            except (ValidationError, ProcessingError, OSError) as e:
                print(f"[{idx:2d}] {video.name:<40} (error: {e})")

        print(f"\n{'='*60}")
        if len(pages) > 1:
            print("[N] Next page  [P] Previous page  [Q] Quit")
        print("[1-10] Select video number  [Q] Quit")
        print(f"{'='*60}")

        choice = input("Select: ").strip().upper()

        if choice == "Q":
            return None
        elif choice == "N" and current_page < len(pages) - 1:
            current_page += 1
        elif choice == "P" and current_page > 0:
            current_page -= 1
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(videos):
                return videos[idx]
            else:
                print(f"❌ Invalid selection. Choose 1-{len(videos)}")
        else:
            print("❌ Invalid input")


def get_conversion_options_interactive(video_info) -> ConversionOptions:
    """
    Get conversion options interactively for videos over 60 seconds

    Args:
        video_info: Video information

    Returns:
        ConversionOptions object
    """
    print(f"\n{'='*60}")
    print(f"Video Duration: {video_info.duration:.1f} seconds")
    print(f"{'='*60}")

    if video_info.is_short:
        print("✓ Video is under 60 seconds, will convert as-is")
        return ConversionOptions()

    print(f"⚠️  Video is over 60 seconds ({video_info.duration:.1f}s)")
    print("\nOptions:")
    print("[1] Use speed adjustment (recommended)")
    print("[2] Select specific segment")
    print("[Q] Cancel")

    choice = input("\nSelect option: ").strip().upper()

    if choice == "Q":
        sys.exit(0)
    elif choice == "1":
        # Speed mode
        suggested_speed = video_info.duration / 59.0
        print(f"\nSuggested speed: {suggested_speed:.2f}x")

        while True:
            speed_input = input(
                f"Enter speed (1.0-4.0) or press Enter for {suggested_speed:.2f}x: "
            ).strip()

            if not speed_input:
                speed = suggested_speed
                break

            try:
                speed = float(speed_input)
                if 0 < speed <= 4.0:
                    break
                else:
                    print("❌ Speed must be between 0 and 4.0")
            except ValueError:
                print("❌ Invalid number")

        options = ConversionOptions(speed=speed)
        output_duration = options.calculate_output_duration(video_info.duration)
        print(f"✓ Output will be {output_duration:.1f} seconds")

        return options

    elif choice == "2":
        # Segment mode
        print(f"\nVideo duration: {video_info.duration:.1f} seconds")

        while True:
            try:
                start = float(input("Start time (seconds): ").strip())
                duration = float(input("Duration (seconds, max 60): ").strip())

                if start < 0 or start >= video_info.duration:
                    print(f"❌ Start time must be between 0 and {video_info.duration:.1f}")
                    continue

                if duration <= 0 or duration > 60:
                    print("❌ Duration must be between 0 and 60")
                    continue

                if start + duration > video_info.duration:
                    print("❌ Segment exceeds video length")
                    continue

                options = ConversionOptions(start_time=start, duration=duration)
                print(f"✓ Will extract {start:.1f}s - {start + duration:.1f}s")
                return options

            except ValueError:
                print("❌ Invalid number")
    else:
        print("❌ Invalid option")
        return get_conversion_options_interactive(video_info)


def progress_callback(progress: float):
    """Simple progress callback for non-tqdm mode"""
    bar_length = 40
    filled = int(bar_length * progress / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"\rProgress: [{bar}] {progress:.1f}%", end="", flush=True)
    if progress >= 100:
        print()  # New line when complete


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Convert videos to YouTube Shorts format (9:16, max 60s)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (default)
  python cli.py

  # Specify input and output folders
  python cli.py --input ./videos --output ./shorts

  # Convert specific file with auto speed
  python cli.py --file video.mp4 --output ./shorts

  # Convert with specific speed
  python cli.py --file video.mp4 --speed 1.5

  # Convert specific segment
  python cli.py --file video.mp4 --start 30 --duration 45
        """,
    )

    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default=".",
        help="Input folder containing videos (default: current folder)",
    )

    parser.add_argument("--output", "-o", type=str, help="Output folder (default: same as input)")

    parser.add_argument("--file", "-f", type=str, help="Specific video file to convert")

    parser.add_argument(
        "--speed", "-s", type=float, help="Speed multiplier (e.g., 1.5 for 1.5x speed)"
    )

    parser.add_argument("--start", type=float, help="Start time in seconds (for segment mode)")

    parser.add_argument(
        "--duration", "-d", type=float, help="Duration in seconds (for segment mode)"
    )

    parser.add_argument(
        "--auto",
        "-a",
        action="store_true",
        help="Auto mode: automatically determine speed for videos over 60s",
    )

    args = parser.parse_args()

    # Resolve paths
    input_path = Path(args.input).resolve()

    if args.output:
        output_folder = Path(args.output).resolve()
    else:
        output_folder = input_path if input_path.is_dir() else input_path.parent

    output_folder.mkdir(parents=True, exist_ok=True)

    try:
        # Determine input video
        if args.file:
            video_path = Path(args.file).resolve()
            if not video_path.exists():
                print(f"❌ File not found: {video_path}")
                return 1
        else:
            # Interactive selection
            if not input_path.is_dir():
                print(f"❌ Input path is not a folder: {input_path}")
                return 1

            video_path = select_video_interactive(input_path)
            if not video_path:
                print("\n👋 Cancelled")
                return 0

        # Get video info
        print(f"\n📹 Loading: {video_path.name}")
        video_info = get_video_info(video_path)
        print(f"   Duration: {video_info.duration:.1f}s")
        print(f"   Resolution: {video_info.width}x{video_info.height}")

        # Determine output path
        output_path = output_folder / f"{video_path.stem}_shorts.mp4"

        # Determine conversion options
        if args.auto:
            # Auto mode
            print("\n🤖 Auto mode: determining optimal settings...")
            if video_info.is_short:
                print("   → Video under 60s, converting as-is")
                options = ConversionOptions()
            else:
                speed = video_info.duration / 59.0
                print(f"   → Video over 60s, using {speed:.2f}x speed")
                options = ConversionOptions(speed=speed)

        elif args.speed or args.start is not None or args.duration is not None:
            # Command-line options
            options = ConversionOptions(
                speed=args.speed or 1.0,
                start_time=args.start or 0.0,
                duration=args.duration,
            )

            # Validate
            is_valid, error_msg = options.validate(video_info)
            if not is_valid:
                print(f"❌ Invalid options: {error_msg}")
                return 1
        else:
            # Interactive options
            options = get_conversion_options_interactive(video_info)

        # Convert
        print(f"\n🎬 Converting to: {output_path.name}")
        print(f"   Output folder: {output_folder}")

        if tqdm:
            # Use tqdm progress bar
            with tqdm(total=100, desc="Progress", unit="%") as pbar:
                last_progress = [0]

                def tqdm_callback(progress):
                    delta = progress - last_progress[0]
                    pbar.update(delta)
                    last_progress[0] = progress

                convert_to_shorts(video_path, output_path, options, tqdm_callback)
        else:
            # Use simple progress bar
            convert_to_shorts(video_path, output_path, options, progress_callback)

        print(f"\n✅ Success! Saved to: {output_path}")
        return 0

    except ValidationError as e:
        print(f"\n❌ Validation Error: {e}")
        return 1
    except ProcessingError as e:
        print(f"\n❌ Processing Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
