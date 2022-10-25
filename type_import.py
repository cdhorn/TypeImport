#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2022      Christopher Horn
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

"""
TypeImportTool
"""

# -------------------------------------------------------------------------
#
# Python modules
#
# -------------------------------------------------------------------------
import json
import os

# -------------------------------------------------------------------------
#
# Gtk modules
#
# -------------------------------------------------------------------------
from gi.repository import Gtk

# -------------------------------------------------------------------------
#
# Gramps modules
#
# -------------------------------------------------------------------------
from gramps.gen.config import config as configman
from gramps.gen.const import GRAMPS_LOCALE as glocale
from gramps.gui.dialog import ErrorDialog
from gramps.gui.managedwindow import ManagedWindow
from gramps.gui.plug import tool


try:
    _trans = glocale.get_addon_translator(__file__)
except ValueError:
    _trans = glocale.translation
_ = _trans.gettext


KEYS = [
    "individual_attributes",
    "name_types",
    "origin_types",
    "family_attributes",
    "family_rel_types",
    "child_ref_types",
    "event_attributes",
    "event_names",
    "event_role_names",
    "media_attributes",
    "note_types",
    "place_types",
    "repository_types",
    "source_attributes",
    "source_media_types",
    "url_types",
]


# -------------------------------------------------------------------------
#
# TypeImportTool
#
# -------------------------------------------------------------------------
class TypeImportTool(tool.Tool, ManagedWindow):
    """
    Tool to import all the custom types in the database.
    """

    def __init__(self, dbstate, user, options_class, name, callback=None):
        self.title = _("Type Import Tool")
        self.dbstate = dbstate
        ManagedWindow.__init__(self, user.uistate, [], self.__class__)
        tool.Tool.__init__(self, dbstate, options_class, name)

        filename = self.get_file_name()
        if filename:
            with open(filename, "r", encoding="utf-8") as file_handle:
                data = json.load(file_handle)
            for key in KEYS:
                load_type(self.dbstate.db, key, data)

    def build_menu_names(self, _dummy_obj):
        """
        Return menu name.
        """
        return (self.title, None)

    def get_file_name(self):
        """
        Get the name of the file to save the types to.
        """
        import_dialog = Gtk.FileChooserDialog(
            title="Type Import File",
            transient_for=self.uistate.window,
            action=Gtk.FileChooserAction.OPEN,
        )
        import_dialog.add_buttons(
            _("_Cancel"),
            Gtk.ResponseType.CANCEL,
            _("Import"),
            Gtk.ResponseType.OK,
        )
        self.set_window(import_dialog, None, self.title)
        self.setup_configs("interface.type-import-dialog", 780, 630)
        import_dialog.set_local_only(False)

        file_filter = Gtk.FileFilter()
        file_filter.add_pattern("*.%s" % icase("json"))
        import_dialog.add_filter(file_filter)

        import_dialog.set_current_folder(
            configman.get("paths.recent-import-dir")
        )
        import_dialog.set_current_name(
            "gramps_type_import_%s.json"
            % self.dbstate.db.get_dbname().replace(" ", "_")
        )
        while True:
            response = import_dialog.run()
            if response == Gtk.ResponseType.CANCEL:
                self.close()
                return None
            if response == Gtk.ResponseType.DELETE_EVENT:
                self.close()
                return None
            if response == Gtk.ResponseType.OK:
                filename = import_dialog.get_filename()
                if self.check_errors(filename):
                    continue
                self.close()
                return filename

    def check_errors(self, filename):
        """
        Perform some sanity checks and return True if any found.
        """
        if not isinstance(filename, str):
            return True

        filename = os.path.normpath(os.path.abspath(filename))
        if len(filename) == 0:
            return True

        with open(filename, "r", encoding="utf-8") as file_handle:
            try:
                data = json.load(file_handle)
            except:
                ErrorDialog(
                    _("Error parsing file"),
                    _("File does not appear to be in valid json format."),
                    parent=self.uistate.window,
                )
                return True

        if "type_export_version" not in data:
            ErrorDialog(
                _("Error parsing file"),
                _("File does not appear to be a type export file."),
                parent=self.uistate.window,
            )
            return True

        for key in KEYS:
            if key in data:
                return False

        ErrorDialog(
            _("Error parsing file"),
            _("File does not appear to contain any valid keys."),
            parent=self.uistate.window,
        )
        return True


def icase(ext):
    """
    Return a glob reresenting a case insensitive file extension.
    """
    return "".join(["[{}{}]".format(s.lower(), s.upper()) for s in ext])


def load_type(db, key, data):
    if key in data:
        type_list = getattr(db, key)
        for item in data[key]:
            type_list.add(item)


# ------------------------------------------------------------------------
#
# TypeImportToolOptions
#
# ------------------------------------------------------------------------
class TypeImportToolOptions(tool.ToolOptions):
    """
    Defines options and provides handling interface.
    """

    def __init__(self, name, person_id=None):
        tool.ToolOptions.__init__(self, name, person_id)
