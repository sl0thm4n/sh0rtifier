"""
sh0rtifier - Core Logic (MVP)

This module handles video conversion from 16:9 to 9:16 with 60-second limit.
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

import cv2
import numpy as np
from moviepy.editor import VideoFileClip, vfx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ShortsError(Exception):
    """Base exception for Shorts Maker"""

    pass


class ValidationError(ShortsError):
    """Validation error"""

    pass


class ProcessingError(ShortsError):
    """Video processing error"""

    pass


@dataclass
class VideoInfo:
    """Video file information"""

    path: Path
    duration: float
    width: int
    height: int
    fps: float
    has_audio: bool

    @property
    def is_short(self) -> bool:
        """Check if video is under 60 seconds"""
        return self.duration < 60.0

    @property
    def aspect_ratio(self) -> float:
        """Calculate aspect ratio"""
        return self.width / self.height if self.height > 0 else 0

    @property
    def is_landscape(self) -> bool:
        """Check if video is landscape (16:9-ish)"""
        return self.width > self.height


@dataclass
class ConversionOptions:
    """Options for video conversion"""

    # Segment selection (for videos over 60 seconds)
    start_time: float = 0.0
    duration: Optional[float] = None  # None means until the end

    # Speed multiplier (alternative to segment selection)
    speed: float = 1.0

    # Output settings
    target_width: int = 1080
    target_height: int = 1920
    output_bitrate: str = "8000k"
    output_fps: int = 30

    # Visual effects
    blur_kernel: int = 99
    blur_sigma: int = 80
    blur_brightness: float = 0.6
    blur_darken: int = -50

    video_fadeout: float = 1.0
    audio_fadeout: float = 3.0

    def calculate_output_duration(self, original_duration: float) -> float:
        """
        Calculate the final output duration

        Args:
            original_duration: Original video duration in seconds

        Returns:
            Expected output duration in seconds
        """
        if self.duration is not None:
            # Segment mode: use specified duration
            actual_duration = min(self.duration, original_duration - self.start_time)
        else:
            # Speed mode: use full duration from start_time
            actual_duration = original_duration - self.start_time

        # Apply speed
        return actual_duration / self.speed

    def validate(self, video_info: VideoInfo) -> tuple[bool, Optional[str]]:
        """
        Validate conversion options

        Args:
            video_info: Video information

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Videos under 60 seconds are always OK
        if video_info.is_short:
            return True, None

        # For videos over 60 seconds
        if self.start_time < 0:
            return False, "Start time must be 0 or greater"

        if self.start_time >= video_info.duration:
            return False, f"Start time exceeds video duration ({video_info.duration:.1f}s)"

        if self.speed <= 0:
            return False, "Speed must be greater than 0"

        # Check segment duration if specified
        if self.duration is not None:
            if self.duration <= 0:
                return False, "Duration must be greater than 0"

            if self.start_time + self.duration > video_info.duration:
                return False, "Selected segment exceeds video duration"

        # Check final output duration
        output_duration = self.calculate_output_duration(video_info.duration)
        if output_duration > 60.0:
            return False, f"Output duration ({output_duration:.1f}s) exceeds 60 seconds limit"

        return True, None


def get_video_info(video_path: Path) -> VideoInfo:
    """
    Extract video information

    Args:
        video_path: Path to video file

    Returns:
        VideoInfo object

    Raises:
        ProcessingError: If video cannot be read
    """
    try:
        clip = VideoFileClip(str(video_path))
        info = VideoInfo(
            path=video_path,
            duration=clip.duration,
            width=clip.w,
            height=clip.h,
            fps=clip.fps,
            has_audio=clip.audio is not None,
        )
        clip.close()
        return info
    except (OSError, RuntimeError) as e:
        raise ProcessingError(f"Failed to read video info: {str(e)}") from e


def create_blur_background(
    frame: np.ndarray,
    target_width: int,
    target_height: int,
    blur_kernel: int,
    blur_sigma: int,
    brightness: float,
    darken: int,
) -> np.ndarray:
    """
    Create blurred background for vertical video

    Args:
        frame: Input frame
        target_width: Target width (1080)
        target_height: Target height (1920)
        blur_kernel: Gaussian blur kernel size
        blur_sigma: Gaussian blur sigma
        brightness: Brightness multiplier
        darken: Brightness offset

    Returns:
        Blurred background frame
    """
    # Resize to target size (stretched)
    bg = cv2.resize(frame, (target_width, target_height))

    # Apply Gaussian blur
    if blur_kernel > 0:
        kernel_size = blur_kernel if blur_kernel % 2 == 1 else blur_kernel + 1
        bg = cv2.GaussianBlur(bg, (kernel_size, kernel_size), blur_sigma)

    # Adjust brightness
    bg = cv2.convertScaleAbs(bg, alpha=brightness, beta=darken)

    return bg


def apply_vertical_layout(
    frame: np.ndarray,
    target_width: int,
    target_height: int,
    blur_kernel: int,
    blur_sigma: int,
    brightness: float,
    darken: int,
) -> np.ndarray:
    """
    Apply 9:16 vertical layout with blurred background

    Args:
        frame: Input frame
        target_width: Target width
        target_height: Target height
        blur_kernel: Blur kernel size
        blur_sigma: Blur sigma
        brightness: Background brightness
        darken: Background darken amount

    Returns:
        Processed frame in 9:16 format
    """
    h, w = frame.shape[:2]

    # Create blurred background
    result = create_blur_background(
        frame, target_width, target_height, blur_kernel, blur_sigma, brightness, darken
    )

    # Resize main video (fit width, maintain aspect ratio)
    scale = target_width / w
    new_width = target_width
    new_height = int(h * scale)
    resized = cv2.resize(frame, (new_width, new_height))

    # Center vertically
    if new_height <= target_height:
        y_offset = (target_height - new_height) // 2
        result[y_offset : y_offset + new_height, 0:target_width] = resized
    else:
        # If taller than target, crop from center
        crop_y = (new_height - target_height) // 2
        result[:, :] = resized[crop_y : crop_y + target_height, :]

    return result


def convert_to_shorts(
    video_path: Path,
    output_path: Path,
    options: Optional[ConversionOptions] = None,
    progress_callback: Optional[Callable[[float], None]] = None,
) -> Path:
    """
    Convert 16:9 video to 9:16 YouTube Shorts format

    Args:
        video_path: Input video path
        output_path: Output video path
        options: Conversion options (uses defaults if None)
        progress_callback: Callback function for progress updates (0-100)

    Returns:
        Path to output video

    Raises:
        ValidationError: If options are invalid
        ProcessingError: If conversion fails
    """
    if options is None:
        options = ConversionOptions()

    def report_progress(value: float):
        """Report progress to callback"""
        if progress_callback:
            progress_callback(min(100.0, max(0.0, value)))

    try:
        report_progress(0)

        # Get video info
        logger.info("Loading video: %s", video_path.name)
        video_info = get_video_info(video_path)
        logger.info("Video: %.1fs, %dx%d", video_info.duration, video_info.width, video_info.height)

        # Validate options
        is_valid, error_msg = options.validate(video_info)
        if not is_valid:
            raise ValidationError(error_msg)

        report_progress(10)

        # Load video
        clip = VideoFileClip(str(video_path))

        # Apply segment selection if needed
        if not video_info.is_short:
            if options.duration is not None:
                # Segment mode
                end_time = min(options.start_time + options.duration, video_info.duration)
                logger.info("Using segment: %.1fs - %.1fs", options.start_time, end_time)
                clip = clip.subclip(options.start_time, end_time)
            elif options.start_time > 0:
                # Start from specific time
                logger.info("Starting from: %.1fs", options.start_time)
                clip = clip.subclip(options.start_time)

        report_progress(20)

        # Apply speed
        if options.speed != 1.0:
            logger.info("Applying speed: %.1fx", options.speed)
            video_clip = clip.without_audio().fx(vfx.speedx, options.speed)

            # Keep audio at original speed or adjust based on preference
            if clip.audio:
                audio_clip = clip.audio.fx(vfx.speedx, options.speed)
                if options.audio_fadeout > 0:
                    audio_clip = audio_clip.audio_fadeout(options.audio_fadeout)
            else:
                audio_clip = None
        else:
            video_clip = clip.without_audio()
            audio_clip = clip.audio
            if audio_clip and options.audio_fadeout > 0:
                audio_clip = audio_clip.audio_fadeout(options.audio_fadeout)

        report_progress(40)

        # Apply fade effects
        if options.video_fadeout > 0:
            logger.info("Applying video fadeout: %.1fs", options.video_fadeout)
            video_clip = video_clip.crossfadeout(options.video_fadeout)

        report_progress(50)

        # Apply vertical layout
        logger.info("Applying 9:16 layout with blurred background...")

        def frame_processor(frame):
            return apply_vertical_layout(
                frame,
                options.target_width,
                options.target_height,
                options.blur_kernel,
                options.blur_sigma,
                options.blur_brightness,
                options.blur_darken,
            )

        vertical_clip = video_clip.fl_image(frame_processor)

        # Add audio back
        if audio_clip:
            vertical_clip = vertical_clip.set_audio(audio_clip)

        report_progress(60)

        # Export
        logger.info("Exporting to: %s", output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        vertical_clip.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            fps=options.output_fps,
            bitrate=options.output_bitrate,
            preset="medium",
            threads=4,
            logger=None,  # Suppress moviepy logger
        )

        report_progress(100)

        # Cleanup
        clip.close()
        vertical_clip.close()

        logger.info("✓ Conversion complete: %s", output_path.name)
        return output_path

    except ValidationError:
        raise
    except (OSError, ValueError, RuntimeError) as e:
        logger.error("Conversion failed: %s", str(e))
        raise ProcessingError(f"Failed to convert video: {str(e)}") from e


# Helper functions for common use cases


def auto_convert(video_path: Path, output_path: Path) -> Path:
    """
    Auto-convert with smart defaults

    For videos under 60s: Convert as-is
    For videos over 60s: Use 1.5x speed to fit within 60s

    Args:
        video_path: Input video path
        output_path: Output video path

    Returns:
        Path to output video
    """
    video_info = get_video_info(video_path)

    if video_info.is_short:
        # Under 60 seconds: use as-is
        options = ConversionOptions()
    else:
        # Over 60 seconds: calculate speed needed
        required_speed = video_info.duration / 59.0  # Leave 1s margin
        options = ConversionOptions(speed=required_speed)
        logger.info("Video is %.1fs, using %.2fx speed", video_info.duration, required_speed)

    return convert_to_shorts(video_path, output_path, options)


def convert_segment(video_path: Path, output_path: Path, start: float, duration: float) -> Path:
    """
    Convert a specific segment of video

    Args:
        video_path: Input video path
        output_path: Output video path
        start: Start time in seconds
        duration: Duration in seconds

    Returns:
        Path to output video
    """
    options = ConversionOptions(start_time=start, duration=duration)
    return convert_to_shorts(video_path, output_path, options)


def convert_with_speed(video_path: Path, output_path: Path, speed: float) -> Path:
    """
    Convert video with specified speed

    Args:
        video_path: Input video path
        output_path: Output video path
        speed: Speed multiplier (e.g., 1.5 for 1.5x speed)

    Returns:
        Path to output video
    """
    options = ConversionOptions(speed=speed)
    return convert_to_shorts(video_path, output_path, options)
