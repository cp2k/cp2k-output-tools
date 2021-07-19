from cp2k_output_tools.blocks.common import merged_spans


def test_merged_spans():
    spans = [
        (20, 30),
        (7, 10),
        (35, 45),
        (10, 11),
        (3, 5),
        (25, 35),
        (46, 47),
    ]

    assert merged_spans(spans) == [(3, 5), (7, 11), (20, 45), (46, 47)]
