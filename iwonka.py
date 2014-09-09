#-*- coding: utf-8 -*-

import argparse
import os
import zipfile


IWONKA_DESC_STR = u"Tworzy archiwa ZIP dla plikow o zgodnych nazwach"
PATH_DESC_STR = u"Scieżka do plików"


class FilePacker(object):

    def __init__(self, dir_path=None):
        self.dir_path = dir_path or os.getcwd()
        #TODO
        self.output_dir = None

    def _extract_filename_pattern(self, filename):
        """
        Wyliczamy nazwe finalnego pliku

        ex. NMT-M-34-63-A-a-3_s.asc => M-34-63-A-a-3
        """
        filename_str = filename.replace('NMT-', '').replace('-', '')
        name_str = filename_str[:filename_str.index('_')]
        ext_str = filename_str.split('.')[-1]

        try:
            int(name_str[3:6])
            n = 3
        except ValueError:
            n = 2

        rejoin_array = [name_str[:1], name_str[1:3], name_str[3:3+n]]
        rejoin_array.extend(list(name_str[3+n:]))

        return '_'.join(['-'.join(rejoin_array), ext_str])

    def _create_files_map(self):
        dir_map = {}

        for subdir, dirs, files in os.walk(self.dir_path):

            if files:
                dir_map[subdir] = {}
                last_file_pattern = None

            for filename in files:

                if '.zip' in filename:
                    continue

                pattern = self._extract_filename_pattern(filename)

                if last_file_pattern is None or last_file_pattern != pattern:
                    last_file_pattern = pattern
                    dir_map[subdir][pattern] = [filename, ]
                else:
                    dir_map[subdir][pattern].append(filename)

        return dir_map

    def create_zip_archive(self, archive_path, file_path, include_files):
        print '* Creating zip archive - %s' % archive_path

        with zipfile.ZipFile(archive_path, 'w') as myzip:
            [myzip.write(os.path.join(file_path, include_file), include_file)
             for include_file in include_files]

        return myzip.filename

    def create_zip_archives(self):
        created_files = []

        for dir_path, patterns in self._create_files_map().iteritems():
            for pattern, files in patterns.iteritems():
                archive_name = os.path.join(dir_path, '%s.zip' % pattern)

                if not os.path.exists(archive_name):
                    created_files.append(self.create_zip_archive(archive_name, dir_path, files))
                else:
                    print '* Archive already exists - %s' % archive_name

        return created_files

    def run(self):
        return self.create_zip_archives()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=IWONKA_DESC_STR)
    parser.add_argument("--path", help=PATH_DESC_STR)

    args = parser.parse_args()

    packer = FilePacker(dir_path=args.path)
    packer.run()
