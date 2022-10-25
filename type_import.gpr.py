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

# ------------------------------------------------------------------------
#
# TypeImportTool
#
# ------------------------------------------------------------------------

register(
    TOOL,
    id="typeimport",
    name=_("Type Import Tool"),
    description=_("Import custom types and attributes"),
    version="1.0.0",
    gramps_target_version="5.1",
    status=STABLE,
    fname="type_import.py",
    authors=["Christopher Horn"],
    authors_email=[],
    category=TOOL_UTILS,
    toolclass="TypeImportTool",
    optionclass="TypeImportToolOptions",
    tool_modes=[TOOL_MODE_GUI],
)
