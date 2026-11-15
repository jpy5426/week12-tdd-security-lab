from datetime import date

import pytest

from tdd_lab.promo import PromoError, apply_promo

TODAY = date(2026, 11, 9)


def test_save10_takes_ten_percent_off():
    assert apply_promo(10_000, "SAVE10", TODAY) == 9_000


def test_rounds_discount_down():
    assert apply_promo(1_005, "SAVE10", TODAY) == 905


@pytest.mark.parametrize("code", ["SAVE20", "", "SAVE 10"])
def test_unknown_code_raises(code):
    with pytest.raises(PromoError):
        apply_promo(10_000, code, TODAY)


def test_code_is_case_and_whitespace_insensitive():
    assert apply_promo(10_000, "\tsAvE10\n", TODAY) == 9_000


def test_flat5_minimum_boundary():
    assert apply_promo(2_000, "FLAT5", TODAY) == 1_500
    with pytest.raises(PromoError):
        apply_promo(1_999, "FLAT5", TODAY)


def test_welcome_expiry_boundary():
    assert apply_promo(10_000, "WELCOME", date(2026, 12, 31)) == 8_500
    with pytest.raises(PromoError):
        apply_promo(10_000, "WELCOME", date(2027, 1, 1))


def test_total_never_negative():
    assert apply_promo(-100, "SAVE10", TODAY) == 0
