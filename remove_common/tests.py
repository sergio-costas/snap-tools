#!/usr/bin/env python3

import os
import remove_common
import shutil
import unittest
import tempfile

ONLY_IN_INSTALL = 0
IN_BOTH = 1
ONLY_IN_BASE = 2

class base_system:
    def __init__(self):
        self._base_folder = tempfile.mkdtemp()
        self._snap_path = os.path.join(self._base_folder, "snaps")
        self._gtk_common_themes_path = os.path.join(self._snap_path, "gtk-common-themes")
        self._gnome_46_path = os.path.join(self._snap_path, "gnome-46")
        self._install_path = os.path.join(self._base_folder, "install")
        self._exclude = []
        for exclude in remove_common.global_excludes:
            self.add_exclude(exclude)

        os.makedirs(self._gtk_common_themes_path)
        os.makedirs(self._gnome_46_path)
        os.makedirs(self._install_path)

    def delete_folders(self):
        shutil.rmtree(self._base_folder)


    def create_icons_folder(self, name, mode):
        if (mode == ONLY_IN_INSTALL) or (mode == IN_BOTH):
            os.makedirs(os.path.join(self._gtk_common_themes_path, "share", "icons", name), exist_ok=True)
        if (mode == ONLY_IN_BASE) or (mode == IN_BOTH):
            os.makedirs(os.path.join(self._install_path, "usr", "share", "icons", name), exist_ok=True)

    def create_icon(self, theme, name, mode):
        self.create_icons_folder(theme, mode)
        if (mode == ONLY_IN_BASE) or (mode == IN_BOTH):
            self._create_empty_file(os.path.join(self._gtk_common_themes_path, "share", "icons", theme, name))
        if (mode == ONLY_IN_INSTALL) or (mode == IN_BOTH):
            self._create_empty_file(os.path.join(self._install_path, "usr", "share", "icons", theme, name))

    def create_folder(self, path, mode):
        if (mode == ONLY_IN_BASE) or (mode == IN_BOTH):
            os.makedirs(os.path.join(self._gnome_46_path, path), exist_ok=True)
        if (mode == ONLY_IN_INSTALL) or (mode == IN_BOTH):
            os.makedirs(os.path.join(self._install_path, path), exist_ok=True)

    def _create_empty_file(self, path):
        open(path, "w").close()

    def create_file(self, fullpath, mode):
        path, name = os.path.split(fullpath)
        self.create_folder(path, mode)
        if (mode == ONLY_IN_BASE) or (mode == IN_BOTH):
            self._create_empty_file(os.path.join(self._gnome_46_path, path, name))
        if (mode == ONLY_IN_INSTALL) or (mode == IN_BOTH):
            self._create_empty_file(os.path.join(self._install_path, path, name))

    def add_exclude(self, exclude):
        self._exclude.append(exclude)

    def remove_common(self):
        # maps must end in "/", like "usr/"
        maps = ((self._gnome_46_path, None), (self._gtk_common_themes_path, "usr/"))
        remove_common.main(self._install_path, maps, self._exclude)

    def file_exists(self, path):
        full_path = os.path.join(self._install_path, path)
        return os.path.exists(full_path)


class TestRemoveCommon(unittest.TestCase):

    def test_dups_are_removed(self):
        b = base_system()
        b.create_file("usr/bin/a1", ONLY_IN_BASE)
        b.create_file("usr/bin/a2", ONLY_IN_INSTALL)
        b.create_file("usr/bin/a3", IN_BOTH)
        b.remove_common()
        self.assertTrue(b.file_exists("usr/bin/a2"))
        self.assertFalse(b.file_exists("usr/bin/a3"))

    def test_theme_index_arent_removed(self):
        b = base_system()
        b.create_icon("hicolor", "icon1", IN_BOTH)
        b.create_icon("hicolor", "index.theme", IN_BOTH)
        b.remove_common()
        self.assertTrue(b.file_exists("usr/share/icons/hicolor/index.theme"))
        self.assertFalse(b.file_exists("usr/share/icons/hicolor/icon1"))
if __name__ == '__main__':
    unittest.main()
