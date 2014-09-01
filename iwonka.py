#-*- coding: utf-8 -*-

import argparse
import os
import zipfile


IWONKA_DESC_STR = u"Tworzy archiwa ZIP dla plikow o zgodnych nazwach"
PATH_DESC_STR = u"Scieżka do plików"


class FilePacker(object):

    def __init__(self, dir_path=None):
        self.dir_path = dir_path or os.getcwd()

    def _extract_filename(self, filename):
        """
        ex. NMT-M-34-63-A-a-3_s.asc
        """
        filename_str = filename.replace('NMT-', '').replace('-', '')
        name_str = filename_str[:filename_str.index('_')]

        try:
            int(name_str[3:6])
            n = 3
        except ValueError:
            n = 2

        rejoin_array = [name_str[:1], name_str[1:3], name_str[3:3+n]]
        rejoin_array.extend(list(name_str[3+n:]))

        return '-'.join(rejoin_array)


    def run(self):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=IWONKA_DESC_STR)
    parser.add_argument("--path", help=PATH_DESC_STR)

    args = parser.parse_args()

    packer = FilePacker(dir_path=args.path)
    packer.run()