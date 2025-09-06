__version__ = '3.8.0'

def get_version():
    return __version__

def get_full_version():
    return f"MatelasApp v{__version__}"

def get_version_info():
    return {
        "version": __version__,
        "full_version": get_full_version()
    }

def get_changelog():
    import os
    changelog_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "CHANGELOG.md")
    try:
        with open(changelog_path, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return "Changelog non disponible." 