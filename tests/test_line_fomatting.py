import pytest
from ionex_formatter.formatter import (
    IonexFile,
    NumericTokenTooBig,
    UnknownFormatSpecifier,
    UnknownFormatingError
)

class TestLineFormating():

    @pytest.fixture
    def formatter(self):
        return IonexFile()

    def test_format_line_basic(self, formatter):
        data = [1, 2, '3']
        format_spec = "I3, 2X, F7.3, 3X, A2, 10X"
        formatted_line = formatter.format_header_line(data, format_spec)
        expected = "  1    2.000   3           "
        assert formatted_line == expected

    def test_format_line_basic_str(self, formatter):
        data = ['1', '2.0', '3']
        format_spec = "I3, 2X, F7.3, 3X, A2, 10X"
        formatted_line = formatter.format_header_line(data, format_spec)
        expected = "  1    2.000   3           "
        assert formatted_line == expected

    def test_format_line_blank(self, formatter):
        data = []
        format_spec = "3X, 7X"
        formatted_line = formatter.format_header_line(data, format_spec)
        expected = "          "
        assert formatted_line == expected

    def test_format_line_decimal_digits(self, formatter):
        data = [1.23, 12.3456, 123.45678, 123.45678]
        format_spec = "F5.2, F8.4, F10.6, F11.6"
        formatted_line = formatter.format_header_line(data, format_spec)
        expected = " 1.23 12.3456123.456780 123.456780"
        assert formatted_line == expected

    def test_format_line_missing_data(self, formatter):
        data = [1, 2]
        format_spec = "I3, F6.1"
        formatted_line = formatter.format_header_line(data, format_spec)
        expected = "  1   2.0"
        assert formatted_line == expected

    def test_format_line_long_string(self, formatter):
        data = ['12345678901234567890', 42, 'XYZ']
        format_spec = "A10, I2, A3"
        with pytest.raises(NumericTokenTooBig):
            formatted_line = formatter.format_header_line(data, format_spec)

    def test_format_line_extra_data(self, formatter):
        data = ['1', '2', '3', '4']
        format_spec = "I3, F6.1, A2"
        with pytest.raises(ValueError):
            formatter.format_header_line(data, format_spec)

    def test_format_line_too_few_data(self, formatter):
        data = ['1', '2']
        format_spec = "I3, F6.1, A2"
        with pytest.raises(ValueError):
            formatter.format_header_line(data, format_spec)

    def test_format_line_unknown_specifier(self, formatter):
        data = [2/3,'-1','1.0']
        format_spec = "F9.2, F7.1, F8.3"
        with pytest.raises(UnknownFormatingError):
            formatter.format_header_line(data, format_spec)


    def test_format_line_invalid_(self, formatter):
        data = ['1', '2', 'V']
        format_spec = "Z3J, G6.1, O2.2"
        with pytest.raises(UnknownFormatSpecifier):
             formatter.format_header_line(data, format_spec)

    def test_format_line_ivalid_other(self, formatter):
        data = [1, 2, '3']
        format_spec = "X3, 2X, F7.3, 3X, A2, 1A"
        with pytest.raises(UnknownFormatSpecifier):
            formatter.format_header_line(data, format_spec)

    def test_format_line_invalid_verify(self, formatter):
        data = "1"
        formatted_data="a"
        width=1
        fmt="U"
        precision=1
        with pytest.raises(UnknownFormatSpecifier):
             formatter._verify_formatted(data,fmt,formatted_data,width,precision)
