"""
Tests for markpdfdown.cli module
"""

import argparse
import sys
from unittest.mock import patch

import pytest

from markpdfdown.cli import create_parser, main, validate_args


class TestCreateParser:
    """Tests for create_parser function"""

    def test_parser_creation(self):
        """Test parser is created successfully"""
        parser = create_parser()
        assert isinstance(parser, argparse.ArgumentParser)

    def test_parser_prog_name(self):
        """Test parser program name"""
        parser = create_parser()
        assert parser.prog == "markpdfdown"

    def test_input_argument(self):
        """Test --input argument parsing"""
        parser = create_parser()
        args = parser.parse_args(["--input", "test.pdf"])
        assert args.input == "test.pdf"

    def test_input_short_argument(self):
        """Test -i argument parsing"""
        parser = create_parser()
        args = parser.parse_args(["-i", "test.pdf"])
        assert args.input == "test.pdf"

    def test_output_argument(self):
        """Test --output argument parsing"""
        parser = create_parser()
        args = parser.parse_args(["--output", "output.md"])
        assert args.output == "output.md"

    def test_output_short_argument(self):
        """Test -o argument parsing"""
        parser = create_parser()
        args = parser.parse_args(["-o", "output.md"])
        assert args.output == "output.md"

    def test_start_argument(self):
        """Test --start argument parsing"""
        parser = create_parser()
        args = parser.parse_args(["--start", "5"])
        assert args.start == 5

    def test_start_default(self):
        """Test --start default value"""
        parser = create_parser()
        args = parser.parse_args([])
        assert args.start == 1

    def test_end_argument(self):
        """Test --end argument parsing"""
        parser = create_parser()
        args = parser.parse_args(["--end", "10"])
        assert args.end == 10

    def test_end_default(self):
        """Test --end default value"""
        parser = create_parser()
        args = parser.parse_args([])
        assert args.end == 0

    def test_full_arguments(self):
        """Test parsing all arguments together"""
        parser = create_parser()
        args = parser.parse_args(
            [
                "--input",
                "input.pdf",
                "--output",
                "output.md",
                "--start",
                "2",
                "--end",
                "5",
            ]
        )
        assert args.input == "input.pdf"
        assert args.output == "output.md"
        assert args.start == 2
        assert args.end == 5

    def test_no_arguments(self):
        """Test parsing with no arguments (pipe mode)"""
        parser = create_parser()
        args = parser.parse_args([])
        assert args.input is None
        assert args.output is None
        assert args.start == 1
        assert args.end == 0


class TestValidateArgs:
    """Tests for validate_args function"""

    def test_valid_file_mode_args(self):
        """Test valid file mode arguments"""
        args = argparse.Namespace(
            input="test.pdf",
            output="output.md",
            start=1,
            end=10,
        )
        # Should not raise
        validate_args(args)

    def test_valid_pipe_mode_args(self):
        """Test valid pipe mode arguments (no input/output)"""
        args = argparse.Namespace(
            input=None,
            output=None,
            start=1,
            end=0,
        )
        # Should not raise
        validate_args(args)

    def test_input_without_output_exits(self):
        """Test input without output causes exit"""
        args = argparse.Namespace(
            input="test.pdf",
            output=None,
            start=1,
            end=0,
        )
        with pytest.raises(SystemExit) as exc_info:
            validate_args(args)
        assert exc_info.value.code == 1

    def test_output_without_input_exits(self):
        """Test output without input causes exit"""
        args = argparse.Namespace(
            input=None,
            output="output.md",
            start=1,
            end=0,
        )
        with pytest.raises(SystemExit) as exc_info:
            validate_args(args)
        assert exc_info.value.code == 1

    def test_start_less_than_one_exits(self):
        """Test start page < 1 causes exit"""
        args = argparse.Namespace(
            input="test.pdf",
            output="output.md",
            start=0,
            end=10,
        )
        with pytest.raises(SystemExit) as exc_info:
            validate_args(args)
        assert exc_info.value.code == 1

    def test_end_less_than_start_exits(self):
        """Test end page < start page causes exit"""
        args = argparse.Namespace(
            input="test.pdf",
            output="output.md",
            start=10,
            end=5,
        )
        with pytest.raises(SystemExit) as exc_info:
            validate_args(args)
        assert exc_info.value.code == 1

    def test_end_zero_is_valid(self):
        """Test end=0 (last page) is valid"""
        args = argparse.Namespace(
            input="test.pdf",
            output="output.md",
            start=5,
            end=0,
        )
        # Should not raise
        validate_args(args)

    def test_same_start_end_is_valid(self):
        """Test same start and end page is valid"""
        args = argparse.Namespace(
            input="test.pdf",
            output="output.md",
            start=5,
            end=5,
        )
        # Should not raise
        validate_args(args)


class TestMain:
    """Tests for main function"""

    @patch("markpdfdown.cli.convert_from_file")
    def test_file_mode_success(self, mock_convert, tmp_path):
        """Test successful file mode conversion"""
        input_file = tmp_path / "input.pdf"
        output_file = tmp_path / "output.md"
        input_file.write_bytes(b"%PDF-1.4")

        mock_convert.return_value = "# Converted Content"

        with patch.object(
            sys, "argv", ["markpdfdown", "-i", str(input_file), "-o", str(output_file)]
        ):
            main()

        assert output_file.exists()
        assert output_file.read_text() == "# Converted Content"

    @patch("markpdfdown.cli.convert_from_file")
    def test_file_mode_with_page_range(self, mock_convert, tmp_path):
        """Test file mode with page range"""
        input_file = tmp_path / "input.pdf"
        output_file = tmp_path / "output.md"
        input_file.write_bytes(b"%PDF-1.4")

        mock_convert.return_value = "# Page Content"

        with patch.object(
            sys,
            "argv",
            [
                "markpdfdown",
                "-i",
                str(input_file),
                "-o",
                str(output_file),
                "--start",
                "2",
                "--end",
                "5",
            ],
        ):
            main()

        mock_convert.assert_called_once_with(
            input_path=str(input_file), start_page=2, end_page=5
        )

    @patch("markpdfdown.cli.convert_from_stdin")
    def test_pipe_mode_success(self, mock_convert, capsys):
        """Test successful pipe mode conversion"""
        mock_convert.return_value = "# Pipe Content"

        with patch.object(sys, "argv", ["markpdfdown"]):
            main()

        captured = capsys.readouterr()
        assert "# Pipe Content" in captured.out

    @patch("markpdfdown.cli.convert_from_file")
    def test_conversion_exception_exits(self, mock_convert, tmp_path):
        """Test conversion exception causes exit"""
        input_file = tmp_path / "input.pdf"
        output_file = tmp_path / "output.md"
        input_file.write_bytes(b"%PDF-1.4")

        mock_convert.side_effect = Exception("Conversion error")

        with patch.object(
            sys, "argv", ["markpdfdown", "-i", str(input_file), "-o", str(output_file)]
        ):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    @patch("markpdfdown.cli.convert_from_file")
    def test_keyboard_interrupt_exits(self, mock_convert, tmp_path):
        """Test KeyboardInterrupt causes exit"""
        input_file = tmp_path / "input.pdf"
        output_file = tmp_path / "output.md"
        input_file.write_bytes(b"%PDF-1.4")

        mock_convert.side_effect = KeyboardInterrupt()

        with patch.object(
            sys, "argv", ["markpdfdown", "-i", str(input_file), "-o", str(output_file)]
        ):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
