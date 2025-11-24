from __future__ import annotations
import string
import secrets
from dataclasses import dataclass

AMBIGUOUS = set("O0oIl1|S5B8")

@dataclass
class Options:
    """Options for password generation.

    Attributes:
        length: desired password length.
        use_lower/use_upper/use_digits/use_symbols: enable character classes.
        exclude_ambiguous: remove visually ambiguous characters from pools.
        no_duplicates: avoid repeating characters in the password.
    """
    length: int = 16
    use_lower: bool = True
    use_upper: bool = True
    use_digits: bool = True
    use_symbols: bool = True
    exclude_ambiguous: bool = False
    no_duplicates: bool = False

def build_pool(opts: Options) -> dict[str, str]:
    """Build character classes based on the provided `Options`.

    Returns a mapping from class-name to the string of characters to use.

    Raises:
        ValueError: if no character classes are enabled.
    """
    classes: dict[str, str] = {}
    if opts.use_lower:
        classes["lower"] = string.ascii_lowercase
    if opts.use_upper:
        classes["upper"] = string.ascii_uppercase
    if opts.use_digits:
        classes["digits"] = string.digits
    if opts.use_symbols:
        # Keep symbols conservative for easier pasting
        classes["symbols"] = "!@#$%^&*()-_=+[]{};:,<.>/?"
    if not classes:
        raise ValueError("At least one character class must be enabled.")
    if opts.exclude_ambiguous:
        classes = {name: "".join(ch for ch in s if ch not in AMBIGUOUS) for name, s in classes.items()}
    return classes

def generate_password(opts: Options) -> str:
    """Generate a secure password according to `opts`.

    Guarantees at least one character from each enabled class is present.
    Raises `ValueError` when options are invalid (too-short length, not
    enough unique characters for `no_duplicates`, or no classes enabled).
    """
    classes = build_pool(opts)
    class_list = list(classes.values())

    if opts.length < len(class_list):
        raise ValueError(f"length must be at least {len(class_list)} to include one of each selected class")

    pool = "".join(class_list)
    if opts.no_duplicates and opts.length > len(set(pool)):
        raise ValueError(f"length {opts.length} exceeds unique characters available ({len(set(pool))}) with current options")

    # Ensure at least one char from each class
    password_chars = [secrets.choice(c) for c in class_list]

    # Fill the rest
    remaining = opts.length - len(password_chars)
    if opts.no_duplicates:
        # Remove already chosen to avoid duplicates
        available = list(set(pool) - set(password_chars))
        for _ in range(remaining):
            ch = secrets.choice(available)
            password_chars.append(ch)
            available.remove(ch)
    else:
        for _ in range(remaining):
            password_chars.append(secrets.choice(pool))

    # Shuffle securely
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars)


__all__ = ["Options", "build_pool", "generate_password", "AMBIGUOUS"]
