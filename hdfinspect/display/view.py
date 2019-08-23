import json
import os
from functools import partial
from logging import getLogger
from typing import Any, List, Tuple

from PyQt5 import uic
from PyQt5.QtWidgets import QAction, QGridLayout, QHBoxLayout, QLabel, QMainWindow, QMenu, QTableWidget, \
    QTableWidgetItem, QTextEdit, QTreeView, QTreeWidget, QTreeWidgetItem

from hdfinspect.display.presenter import HDFInspectMainPresenter
from hdfinspect.display.qjsonmodel import QJsonModel


class HDFInspectMain(QMainWindow):
    tree: QTreeWidget
    layout: QGridLayout
    value: QLabel
    table: QTableWidget
    menuOpen: QMenu
    menuRecent_Files: QMenu
    value_display_layout: QHBoxLayout

    def __init__(self, parent=None):
        super().__init__(parent)
        ui_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../ui/main.ui'))
        self.log = getLogger(__name__)
        self.log.debug(f"Looking for UI file at {ui_file}")
        uic.loadUi(os.path.abspath(ui_file), self)

        close_on_ctrl_q = QAction("Close window", self)
        close_on_ctrl_q.triggered.connect(self.close)
        close_on_ctrl_q.setShortcut("Ctrl+q")
        self.addAction(close_on_ctrl_q)

        self.tree.itemSelectionChanged.connect(self.visualise_item)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Class", "Value"])

        self.all_tree_widgets: List[Tuple[QTreeWidgetItem, Any]] = []
        # presenter needs to be made after the view is correctly initialised - it will try to open a file
        # and if the view is not ready, there will be a segfault
        self.presenter = HDFInspectMainPresenter(self)
        self.display_recent_files(self.presenter.model.recent_files)

        self.actionOpen.triggered.connect(self.presenter.action_open_file)

    def closeEvent(self, *args, **kwargs):
        self.presenter.closing()

    def visualise_item(self):
        selected = self.tree.selectedItems()
        if len(selected) == 1:
            item = selected[0]
        else:
            return
        print(item, " clicked, nxs group:", item.nxsref)
        self.table.setRowCount(0)
        for attr in item.nxsref.attrs.items():
            nrows = self.table.rowCount()
            self.table.insertRow(nrows)
            self.table.setItem(nrows, 0, QTableWidgetItem(str(attr[0])))
            self.table.setItem(nrows, 1, QTableWidgetItem(str(attr[1])))

        if hasattr(item.nxsref, "value"):
            self.display_value(item)

    def display_value(self, item):
        val = item.nxsref[()]
        self.value_display_layout.takeAt(0)

        json_widget = self.try_making_json_widget(item, val)
        if json_widget:
            self.value_display_layout.addWidget(json_widget)
        else:
            widget = QTextEdit(self)
            widget.setText(str(val))
            self.value_display_layout.addWidget(widget)

    def try_making_json_widget(self, item, val):
        try:
            val = json.loads(val)
        except Exception as e:
            getLogger(__name__).info(f"Could not parse item {item.nxsref.name} as json. Error: {e}")
            if len(val) == 1:
                try:
                    val = json.loads(val[0])
                    json_widget = QTreeView(self)
                    model = QJsonModel(json_widget)
                    model.load(val)
                    json_widget.setModel(model)
                    return json_widget
                except Exception as e:
                    getLogger(__name__).info(f"Could not parse first item from list as JSON. Error: {e}")
        return None

    def make_tree_widget(self, widget_parent, group):
        widget = QTreeWidgetItem(widget_parent)
        widget.nxsref = group
        widget.setText(0, group.name)
        return widget

    def make_top_level_widget(self, group):
        # top level widget
        widget = self.make_tree_widget(self.tree, group)
        self.tree.addTopLevelItem(widget)
        return widget

    def make_child_widget(self, widget, group):
        child = self.make_tree_widget(widget, group)
        widget.addChild(child)
        return child

    def add_new_widget_to_all(self, group, widget):
        self.all_tree_widgets.append((group, widget))

    def find_parent_widget(self, parent):
        return [parent_widget for parent_group, parent_widget in self.all_tree_widgets if
                parent_group == parent][0]

    def clear(self):
        self.table.setRowCount(0)
        self.tree.clear()

    def display_recent_files(self, recent_files):
        if len(recent_files) > 0:
            self.menuRecent_Files.clear()
            for file in recent_files:
                action = QAction(file, self.menuRecent_Files)
                action.triggered.connect(partial(self.presenter.load_file, file))
                self.menuRecent_Files.addAction(action)
