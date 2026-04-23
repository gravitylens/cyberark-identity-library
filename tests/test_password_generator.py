import string
import pytest

from cyberark_identity_library.identity import generate_unique_password


def count_chars(s, predicate):
    return sum(1 for c in s if predicate(c))


def test_default_password_length():
    pwd = generate_unique_password()
    assert len(pwd) == 12


def test_minimum_requirements():
    pwd = generate_unique_password(length=16, min_lowercase=3, min_uppercase=3, min_digits=2, min_special=1)
    assert len(pwd) == 16
    assert count_chars(pwd, str.islower) >= 3
    assert count_chars(pwd, str.isupper) >= 3
    assert count_chars(pwd, str.isdigit) >= 2
    assert count_chars(pwd, lambda c: c in string.punctuation) >= 1


def test_disallowed_characters_excluded():
    disallowed = 'abcABC123!'
    pwd = generate_unique_password(disallowed_chars=disallowed)
    for ch in disallowed:
        assert ch not in pwd


def test_invalid_length_raises():
    with pytest.raises(ValueError):
        generate_unique_password(length=3, min_lowercase=2, min_uppercase=2, min_digits=0)
