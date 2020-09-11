import os
import warnings
from pathlib import Path
from typing import NamedTuple
from functools import lru_cache


class Configuration(NamedTuple):
    calcurse_dir: Path
    calcurse_load_dir: Path


@lru_cache(1)
def get_configuration() -> Configuration:
    xdg_data: Path = Path(
        os.environ.get(
            "XDG_DATA_HOME", os.path.join(os.environ["HOME"], ".local", "share")
        )
    )
    calcurse_dir: Path = xdg_data / "calcurse"
    calcurse_load_dir: Path = xdg_data / "calcurse_load"
    if not calcurse_dir.exists():
        warnings.warn(
            "Calcurse data directory at {} doesnt exist.".format(str(calcurse_dir))
        )
    if not calcurse_load_dir.exists():
        os.makedirs(str(calcurse_load_dir))
    return Configuration(
        calcurse_dir=calcurse_dir,
        calcurse_load_dir=calcurse_load_dir,
    )


# so that eval "$(calcurse_load --shell)" can be called,
# to get the config values from the hooks
def eval_shell_configuration() -> str:
    conf = get_configuration()
    return "\n".join(
        [
            f'{envvar}="{val}"'
            for envvar, val in zip(
                ("CALCURSE_DIR", "CALCURSE_LOAD_DIR"),
                (conf.calcurse_dir, conf.calcurse_load_dir),
            )
        ]
    )
