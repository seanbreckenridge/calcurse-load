import sys
import argparse

from .ext import EXTENSIONS
from .calcurse import get_configuration

from typing import Tuple, List, Callable


def parse_args() -> Tuple[argparse.Namespace, List[str]]:
    parser = argparse.ArgumentParser(
        description="Load extra data into calcurse",
        # manually write out usage
        usage="calcurse_load (--pre-load|--post-save) ({})...".format(
            "|".join(EXTENSIONS.keys())
        ),
    )
    required_args = parser.add_argument_group("required options")
    hook_choice = required_args.add_mutually_exclusive_group(required=True)
    hook_choice.add_argument(
        "--pre-load",
        help="Execute the preload action for the extension",
        action="store_true",
        default=False,
    )
    hook_choice.add_argument(
        "--post-save",
        help="Execute the postsave action for the extension",
        action="store_true",
        default=False,
    )
    extensions = []
    args, extra = parser.parse_known_args()
    for arg in map(str.lower, extra):
        if arg not in EXTENSIONS:
            print(
                f"Unexpected argument: {arg}, currently loaded extensions: '{','.join(EXTENSIONS)}'"
            )
        else:
            extensions.append(arg)
    return args, extensions


def cli() -> None:
    args, extensions = parse_args()
    configuration = get_configuration()
    if len(extensions) == 0:
        print(
            "No extensions passed!\nPossible extensions:\n{}".format(
                "\n".join(EXTENSIONS)
            ),
            file=sys.stderr,
        )
        sys.exit(1)
    for ext in extensions:
        ext_class: Callable = EXTENSIONS[ext]  # type: ignore[type-arg]
        load_hook = ext_class(config=configuration)
        if args.pre_load:
            load_hook.pre_load()
        else:
            load_hook.post_save()


if __name__ == "__main__":
    cli()
