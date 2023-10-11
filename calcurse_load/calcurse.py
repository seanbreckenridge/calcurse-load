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
            "XDG_DATA_HOME", os.path.join(os.path.expanduser("~"), ".local", "share")
        )
    )
    calcurse_dir: Path = xdg_data / "calcurse"
    if "CALCURSE_DIR" in os.environ:
        calcurse_dir = Path(os.environ["CALCURSE_DIR"])
    calcurse_load_dir: Path = xdg_data / "calcurse_load"
    if not calcurse_dir.exists():
        warnings.warn(
            "Calcurse data directory at {} doesn't exist.".format(str(calcurse_dir))
        )
    if not calcurse_load_dir.exists():
        os.makedirs(str(calcurse_load_dir))
    return Configuration(
        calcurse_dir=calcurse_dir,
        calcurse_load_dir=calcurse_load_dir,
    )
