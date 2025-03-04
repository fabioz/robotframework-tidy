import pytest

from .. import TransformerAcceptanceTest


class TestAlignTestCases(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "AlignTestCases"

    @pytest.mark.parametrize(
        "source",
        [
            "test.robot",
            "no_header_col.robot",
            "with_settings.robot",
            "templated_for_loops.robot",
            "templated_for_loops_and_without.robot",
            "templated_for_loops_header_cols.robot",
        ],
    )
    def test_transformer(self, source):
        self.compare(source=source, expected=source)

    @pytest.mark.parametrize("source", ["for_loops.robot", "empty_line.robot"])
    def test_should_not_modify(self, source):
        self.compare(source=source, not_modified=True)

    def test_only_with_headers(self):
        self.compare(
            source="no_header_col.robot",
            not_modified=True,
            config=":only_with_headers=True",
        )

    def test_fixed(self):
        self.compare(source="test.robot", expected="test_fixed.robot", config=":min_width=30")

    def test_for_fixed(self):
        self.compare(
            source="templated_for_loops_and_without.robot",
            expected="templated_for_loops_and_without_fixed.robot",
            config=":min_width=25",
        )
