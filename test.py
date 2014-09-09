#-*- coding: utf-8 -*-

import os
import shutil
import string
import unittest

from iwonka import FilePacker


class IwonkaTest(unittest.TestCase):

    def _create_test_files_in_dir(self):
        for dir_part in xrange(0, 3):
            directory = os.path.join(self.tmp_dir, str(dir_part))
            os.mkdir(directory)

            for file_part in string.ascii_lowercase[:3]:
                open(os.path.join(directory, "NMT-M-34-63-A-a-1_%s.asc" % file_part), 'w+')
                open(os.path.join(directory, "M-24-233-A-b-1_%s.asc" % file_part), 'w+')
                open(os.path.join(directory, 'existing_archive.zip'), 'w+')

    def _build_test_dir_map(self):
        dir_map = {}

        for dir_part in xrange(0, 3):
            directory = os.path.join(self.tmp_dir, str(dir_part))
            dir_map[directory] = {}

            files_one = ["NMT-M-34-63-A-a-1_%s.asc" % file_part for file_part in string.ascii_lowercase[:3]]
            files_two = ["M-24-233-A-b-1_%s.asc" % file_part for file_part in string.ascii_lowercase[:3]]

            dir_map[directory][self._get_filename_pattern(files_one[0])] = files_one
            dir_map[directory][self._get_filename_pattern(files_two[0])] = files_two

        return dir_map

    def _get_filename_pattern(self, filename):
        return self.packer._extract_filename_pattern(filename)

    def _delete_temporary_directory(self):
        shutil.rmtree(self.tmp_dir)

    def setUp(self):
        self.tmp_dir = os.getcwd() + '/tmp'
        self.packer = FilePacker(dir_path=self.tmp_dir)

        if os.path.exists(self.tmp_dir):
            self._delete_temporary_directory()

        os.mkdir(self.tmp_dir)
        self._create_test_files_in_dir()

    def tearDown(self):
        self._delete_temporary_directory()

    def test_filename(self):
        """
        Testujemy metode okreslająca nazwe pliku
        """

        filename = "NMT-M-34-63-A-a-3_s.asc"
        self.assertEqual(self._get_filename_pattern(filename), 'M-34-63-A-a-3_asc')

        filename = "M-24-233-A-b-3_s.asc"
        self.assertEqual(self._get_filename_pattern(filename), 'M-24-233-A-b-3_asc')

    def test_walker(self):
        """
        Testujemy glowna funkcjonalnosc

        1. Poprawnosc tworzenia mapy przeskanowanych plikow
        2. Poprawnosc tworzenia archiwów
        3. W przypadku gdy archiwum istnieje - nie jest ono nadpisywane
        """

        dir_map = self.packer._create_files_map()
        test_dir_map = self._build_test_dir_map()
        self.assertDictEqual(dir_map, test_dir_map)

        self.packer.run()
        self.assertListEqual(self.packer.run(), [])


if __name__ == "__main__":
    unittest.main()
