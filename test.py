#-*- coding: utf-8 -*-

import unittest
from iwonka import FilePacker


class IwonkaTest(unittest.TestCase):

    def setUp(self):
        self.packer = FilePacker()

    def test_filename(self):
        filename = "NMT-M-34-63-A-a-3_s.asc"
        assert self.packer._extract_filename(filename) == 'M-34-63-A-a-3'
        filename = "M-24-233-A-b-3_s.asc"
        assert self.packer._extract_filename(filename) == 'M-24-233-A-b-3'
