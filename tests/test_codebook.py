import pytest

from prectg.codebook import CODE_LABELS, code_to_label, label_to_code


@pytest.mark.parametrize("field", CODE_LABELS)
def test_code_labels_round_trip(field: str) -> None:
    for code in CODE_LABELS[field]:
        assert label_to_code(field, code_to_label(field, code)) == code


def test_unknown_code_is_rejected() -> None:
    with pytest.raises(ValueError, match="지원하지 않는 코드"):
        code_to_label("Acceleration", "9")
