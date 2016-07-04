from importlib import import_module

if __name__ == "__main__":
    try:
        # noinspection PyUnresolvedReferences
        import pybioas.config
        # noinspection PyUnresolvedReferences
        import pybioas.command
    except ImportError:
        raise ImportError(
            "Couldn't import pybioas. Make sure it's installed corectly "
            "and available on you PYTHONPATH environment variable. "
            "Check if you activated virtual environment."
        )
    try:
        settings_module = import_module("settings")
    except ImportError:
        raise ImportError(
            "Couldn't find settings module. Make sure there is a settings.py "
            "file in the project root directory."
        )
    pybioas.settings = pybioas.config.Settings(settings_module)
    pybioas.command.admin()
