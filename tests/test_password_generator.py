import pytest

from src.password_generator.core import Options, generate_password, build_pool
from src.password_generator.__main__ import parse_args

def test_default_length():
    p = generate_password(Options())
    assert len(p) == 16

def test_includes_each_class():
    opts = Options(length=8)
    p = generate_password(opts)
    pool = build_pool(opts)
    assert any(c in p for c in pool["lower"])
    assert any(c in p for c in pool["upper"])
    assert any(c in p for c in pool["digits"])
    assert any(c in p for c in pool["symbols"])

def test_no_duplicates():
    opts = Options(length=12, no_duplicates=True)
    p = generate_password(opts)
    assert len(set(p)) == len(p)

def test_exclude_ambiguous():
    opts = Options(length=24, exclude_ambiguous=True)
    p = generate_password(opts)
    for ch in "O0oIl1|S5B8":
        assert ch not in p


def test_no_classes_selected_raises():
    opts = Options(use_lower=False, use_upper=False, use_digits=False, use_symbols=False)
    with pytest.raises(ValueError):
        build_pool(opts)


def test_length_too_short_raises():
    opts = Options(length=0)
    with pytest.raises(ValueError):
        generate_password(opts)


def test_no_duplicates_limit_raises():
    # Request a length larger than unique characters available with all classes
    opts = Options(length=100, no_duplicates=True)
    with pytest.raises(ValueError):
        generate_password(opts)


def test_parse_args_flags():
    args = parse_args(["-l", "12", "--no-upper", "--exclude-ambiguous", "--json"])
    assert args.length == 12
    assert args.no_upper is True
    assert args.exclude_ambiguous is True
    assert args.as_json is True
