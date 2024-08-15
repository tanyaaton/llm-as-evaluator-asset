import os

from dynaconf import Dynaconf

CONFIG_FILES = [
    "configs/settings.yaml",
]

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[C for C in CONFIG_FILES if os.path.isfile(C)],
    environments=True,
)
