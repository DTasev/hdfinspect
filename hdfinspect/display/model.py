import json
from logging import getLogger
from pathlib import Path


class HDFInspectMainModel:
    RECENT_FILES_FILE = Path("~/.config/hdfinspect.json").expanduser()
    RECENT_FILES_KEY = "recent_files"

    def __init__(self):
        self.recent_files = set()
        self.log = getLogger(__name__)
        self.log.debug(f"Using recent file at {self.RECENT_FILES_FILE.absolute()}")
        self._load_recent_files()

    def add_recent_file(self, filepath):
        self.log.debug(f"Adding '{filepath}' to recent files.")
        self.recent_files.add(filepath)
        if len(self.recent_files) > 10:
            self.recent_files.remove(0)

    def _load_recent_files(self):
        if self.RECENT_FILES_FILE.exists():
            with self.RECENT_FILES_FILE.open('r') as f:
                try:
                    recent = json.load(f)
                    self.log.debug(f"Loaded {recent} from recent files.")
                    self.recent_files = set(recent[self.RECENT_FILES_KEY])
                except json.decoder.JSONDecodeError as e:
                    self.log.debug(f"Could not parse JSON file. Error: {e}")
                    self.recent_files = set()

    def save_recent_files(self):
        with self.RECENT_FILES_FILE.open('w') as f:
            json.dump({self.RECENT_FILES_KEY: list(self.recent_files)}, f)
            self.log.debug(f"Saved recent files.")
