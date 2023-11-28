import os.path

from pathlib import Path

from split_settings.tools import include, optional


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


ENVVAR_SETTINGS_PREFIX = "BACKENDSETTINGS_"

# 1) This will be false
LOCAL_SETTINGS_PATH = os.getenv(f"{ENVVAR_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH")

if not LOCAL_SETTINGS_PATH:
    # 2) that is why this will be true. What means assigne dev settings
    LOCAL_SETTINGS_PATH = "local/settings.dev.py"


if not os.path.isabs(LOCAL_SETTINGS_PATH):
    # 3) if LOCAL_SETTINGS_PATH is not absolute path, then join it with BASE_DIR
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)


# 4) include all settings files
include(
    # base settings
    "base.py",
    # application settings
    "custom.py",
    # dev settings (overwrite if any)
    optional(LOCAL_SETTINGS_PATH),
    # environment settings (overwrite if any)
    "envvars.py",
    # docker settings
    "docker.py",
)
