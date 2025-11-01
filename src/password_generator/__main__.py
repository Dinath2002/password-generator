from __future__ import annotations
import argparse, json, sys
from .core import Options, generate_password

def parse_args(argv=None):
    p = argparse.ArgumentParser(prog="password-generator", description="Secure password generator (CLI)")
    p.add_argument("-l", "--length", type=int, default=16, help="password length (default: 16)")
    p.add_argument("-n", "--count", type=int, default=1, help="number of passwords to generate (default: 1)")

    group = p.add_argument_group("character classes")
    group.add_argument("--no-lower", action="store_true", help="disable lowercase letters")
    group.add_argument("--no-upper", action="store_true", help="disable uppercase letters")
    group.add_argument("--no-digits", action="store_true", help="disable digits")
    group.add_argument("--no-symbols", action="store_true", help="disable symbols")

    p.add_argument("--exclude-ambiguous", action="store_true", help="exclude ambiguous characters like O,0,l,1,|")
    p.add_argument("--no-duplicates", action="store_true", help="avoid repeating characters")
    p.add_argument("--json", dest="as_json", action="store_true", help="output JSON list")

    return p.parse_args(argv)

def main(argv=None):
    args = parse_args(argv)
    opts = Options(
        length=args.length,
        use_lower=not args.no_lower,
        use_upper=not args.no_upper,
        use_digits=not args.no_digits,
        use_symbols=not args.no_symbols,
        exclude_ambiguous=args.exclude_ambiguous,
        no_duplicates=args.no_duplicates,
    )
    try:
        passwords = [generate_password(opts) for _ in range(args.count)]
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if args.as_json:
        print(json.dumps(passwords, ensure_ascii=False))
    else:
        print("\n".join(passwords))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
