from src.password_generator.core import Options, generate_password, build_pool

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
