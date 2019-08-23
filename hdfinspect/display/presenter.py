from logging import getLogger
from typing import TYPE_CHECKING

import h5py
from PyQt5.QtWidgets import QFileDialog

from hdfinspect.display.model import HDFInspectMainModel
from hdfinspect.h5traverser.traverse import iterate_nxs

if TYPE_CHECKING:
    from hdfinspect.display.view import HDFInspectMain


class HDFInspectMainPresenter:
    file: h5py.File

    def __init__(self, view=None):
        self.view: HDFInspectMain = view
        self.model = HDFInspectMainModel()
        self.log = getLogger(__name__)

    def action_populate(self):
        self.view.setWindowTitle(self.file.filename)
        for parent, group in iterate_nxs(self.file):
            if parent is None:
                widget = self.view.make_top_level_widget(group)
            else:
                widget = self.view.make_child_widget(self.view.find_parent_widget(parent), group)
            self.view.add_new_widget_to_all(group, widget)

    def action_open_file(self):
        file, _ = QFileDialog.getOpenFileName(self.view, "Select NXS file to open", filter="NXS (*.nxs)")
        if file == "":
            self.log.info("No file selected, not changing anything.")
            return
        else:
            self.log.info(f"File {file} selected. Proceeding to load.")
        self.load_file(file)

    def close_file(self):
        if hasattr(self, "file"):
            self.file.close()
            self.view.clear()

    def load_file(self, file):
        self.close_file()
        self.file = h5py.File(file, 'r')
        self.model.add_recent_file(file)
        self.view.display_recent_files(self.model.recent_files)
        self.action_populate()

    def closing(self):
        self.close_file()
        self.model.save_recent_files()
