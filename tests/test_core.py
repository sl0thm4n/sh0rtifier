"""
Unit tests for sh0rtifier core functionality
"""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core import (
    ConversionOptions,
    ProcessingError,
    ValidationError,
    VideoInfo,
)

TEST_CLIP = "data/test.mp4"


class TestVideoInfo:
    """Test VideoInfo dataclass"""

    def test_is_short_under_60(self):
        """Test is_short property for videos under 60 seconds"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=45.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        assert video.is_short is True

    def test_is_short_over_60(self):
        """Test is_short property for videos over 60 seconds"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=90.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        assert video.is_short is False

    def test_is_short_exactly_60(self):
        """Test is_short property for videos exactly 60 seconds"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=60.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        assert video.is_short is False

    def test_aspect_ratio(self):
        """Test aspect ratio calculation"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=45.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        assert video.aspect_ratio == pytest.approx(16 / 9, rel=0.01)

    def test_is_landscape(self):
        """Test landscape detection"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=45.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        assert video.is_landscape is True

        portrait_video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=45.0,
            width=1080,
            height=1920,
            fps=30.0,
            has_audio=True,
        )
        assert portrait_video.is_landscape is False


class TestConversionOptions:
    """Test ConversionOptions dataclass"""

    def test_calculate_output_duration_with_speed(self):
        """Test output duration calculation with speed adjustment"""
        options = ConversionOptions(speed=2.0)
        output = options.calculate_output_duration(120.0)
        assert output == 60.0

    def test_calculate_output_duration_with_segment(self):
        """Test output duration calculation with segment"""
        options = ConversionOptions(duration=30.0)
        output = options.calculate_output_duration(120.0)
        assert output == 30.0

    def test_calculate_output_duration_segment_and_speed(self):
        """Test output duration with both segment and speed"""
        options = ConversionOptions(duration=60.0, speed=2.0)
        output = options.calculate_output_duration(120.0)
        assert output == 30.0

    def test_validate_short_video(self):
        """Test validation for videos under 60 seconds"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=45.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        options = ConversionOptions()
        is_valid, error = options.validate(video)
        assert is_valid is True
        assert error is None

    def test_validate_long_video_with_speed(self):
        """Test validation for long video with speed adjustment"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=120.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        options = ConversionOptions(speed=2.0)
        is_valid, error = options.validate(video)
        assert is_valid is True
        assert error is None

    def test_validate_long_video_with_segment(self):
        """Test validation for long video with segment"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=120.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        options = ConversionOptions(start_time=30.0, duration=40.0)
        is_valid, error = options.validate(video)
        assert is_valid is True
        assert error is None

    def test_validate_exceeds_60_seconds(self):
        """Test validation fails when output exceeds 60 seconds"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=120.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        options = ConversionOptions(speed=1.5)  # 120 / 1.5 = 80 seconds
        is_valid, error = options.validate(video)
        assert is_valid is False
        assert "exceeds 60 seconds" in error.lower()

    def test_validate_negative_start_time(self):
        """Test validation fails for negative start time"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=120.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        options = ConversionOptions(start_time=-10.0)
        is_valid, error = options.validate(video)
        assert is_valid is False
        assert "start time" in error.lower()

    def test_validate_start_exceeds_duration(self):
        """Test validation fails when start time exceeds video duration"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=60.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        options = ConversionOptions(start_time=70.0)
        is_valid, error = options.validate(video)
        assert is_valid is False
        assert "exceeds video duration" in error.lower()

    def test_validate_segment_exceeds_video(self):
        """Test validation fails when segment exceeds video duration"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=60.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        options = ConversionOptions(start_time=50.0, duration=20.0)
        is_valid, error = options.validate(video)
        assert is_valid is False
        assert "exceeds" in error.lower()

    def test_validate_invalid_speed(self):
        """Test validation fails for invalid speed"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=60.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        options = ConversionOptions(speed=0.0)
        is_valid, error = options.validate(video)
        assert is_valid is False
        assert "speed" in error.lower()

    def test_validate_negative_duration(self):
        """Test validation fails for negative duration"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=60.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        options = ConversionOptions(duration=-10.0)
        is_valid, error = options.validate(video)
        assert is_valid is False
        assert "duration" in error.lower()


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_exactly_60_seconds_with_1x_speed(self):
        """Test 60-second video at 1x speed"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=60.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        options = ConversionOptions(speed=1.0)
        is_valid, error = options.validate(video)
        assert is_valid is True  # 60 seconds exactly is valid for YouTube Shorts

    def test_59_seconds_is_valid(self):
        """Test 59-second video is valid"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=59.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        options = ConversionOptions()
        is_valid, error = options.validate(video)
        assert is_valid is True

    def test_very_short_video(self):
        """Test very short video (1 second)"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=1.0,
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        options = ConversionOptions()
        is_valid, error = options.validate(video)
        assert is_valid is True

    def test_extreme_speed(self):
        """Test with extreme speed values"""
        video = VideoInfo(
            path=Path(TEST_CLIP),
            duration=240.0,  # 4 minutes
            width=1920,
            height=1080,
            fps=30.0,
            has_audio=True,
        )
        options = ConversionOptions(speed=4.0)  # 240 / 4 = 60
        is_valid, error = options.validate(video)
        assert is_valid is True  # Exactly 60 seconds is valid

        options = ConversionOptions(speed=3.99)  # 240 / 3.99 = 60.15 seconds
        is_valid, error = options.validate(video)
        assert is_valid is False  # Over 60 seconds is not valid


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
