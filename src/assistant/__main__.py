"""Run the starter assistant with a question, or interactively without arguments."""
import argparse

from assistant import __version__, reply


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="assistant", description="Starter study assistant.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("question", nargs="*", help="Question to ask; omit for interactive mode.")
    args = parser.parse_args(argv)
    if args.question:
        print(reply(" ".join(args.question)))
        return 0
    print("Study assistant (starter). Type 'quit' to exit.")
    while True:
        try:
            msg = input("> ")
        except EOFError:
            break
        if msg.strip().lower() in {"quit", "exit"}:
            break
        print(reply(msg))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
