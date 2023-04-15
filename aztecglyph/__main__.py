import aztecglyph.core as aztecglyph
import argparse


def main():
    parser = argparse.ArgumentParser(description="Instances of the AztecGlyph class represent 64-bit UUIDs.")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-s",
        "--string",
        help="base58 encoded string",
        type=str,
    )

    group.add_argument(
        "-b",
        "--bytes",
        help="bytes object",
        type=bytes.fromhex,
        metavar="HEX",
    )

    group.add_argument(
        "-i",
        "--int",
        help="integer",
        type=int,
    )

    group.add_argument(
        "-h",
        "--hex",
        help="hexadecimal string",
        type=str,
    )

    group.add_argument(
        "-n",
        "--now",
        help="timestamp in milliseconds",
        type=int,
    )

    group.add_argument(
        "-c",
        "--counter",
        help="counter",
        type=int,
    )

    parser.add_argument(
        "-t",
        "--content_type",
        help="content_type",
        type=int,
        default=None,
    )

    args = parser.parse_args()

    if args.string is not None:
        glyph = aztecglyph.AztecGlyph(s=args.string)
    elif args.bytes is not None:
        glyph = aztecglyph.AztecGlyph(b=args.bytes)
    elif args.int is not None:
        glyph = aztecglyph.AztecGlyph(i=args.int)
    elif args.counter is not None and args.content_type is not None and args.timestamp is not None:
        glyph = aztecglyph.AztecGlyph(counter=args.counter, content_type=args.content_type, now=args.now)
    else:
        raise TypeError("AztecGlyph constructor requires one of the following: str or bytes or int or counter, "
                        "content_type, and now.")
    print("AztecGlyph: ", glyph.str)


if __name__ == "__main__":
    main()
