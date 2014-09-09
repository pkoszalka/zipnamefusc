#-*- coding: utf-8 -*-

import argparse
import os
import zipfile


IWONKA_DESC_STR = u"Tworzy archiwa ZIP dla plikow o zgodnych nazwach"
PATH_DESC_STR = u"Scieżka do plików"


class FilePacker(object):

    def __init__(self, dir_path=None, output_dir=None):
        self.dir_path = dir_path or os.getcwd()
        self.output_dir = output_dir or os.path.join(os.getcwd(), 'output')
        #FIXME po pierwszych testach produkcyjnych ;)
        self.output_mode = True
        self.not_allowed_ext = ['.zip', ]
        self.archive_format = 'zip'
        self.archive_map = {
            'zip': self.create_zip_archive
        }

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

                if any((ext in filename) for ext in self.not_allowed_ext):
                    continue

                pattern = self._extract_filename_pattern(filename)

                if last_file_pattern is None or last_file_pattern != pattern:
                    last_file_pattern = pattern
                    dir_map[subdir][pattern] = [filename, ]
                else:
                    dir_map[subdir][pattern].append(filename)

        return dir_map

    def create_zip_archive(self, archive_name, dest_path, source_path, file_names):
        archive_name = '%s.zip' % archive_name
        archive_path = os.path.join(dest_path, archive_name)

        if not os.path.exists(dest_path):
            os.makedirs(dest_path)

        if not os.path.exists(archive_path):
            print '* Creating zip archive - %s' % archive_name

            with zipfile.ZipFile(archive_path, 'w') as myzip:
                [myzip.write(os.path.join(source_path, include_file), include_file)
                 for include_file in file_names]

            return myzip.filename
        else:
            print '* Archive already exists - %s' % archive_name

    def create_archives(self):
        created_files = []

        for dir_path, patterns in self._create_files_map().iteritems():
            for pattern, files in patterns.iteritems():

                if self.output_mode:
                    dest_path = dir_path.replace(self.dir_path, self.output_dir)
                else:
                    dest_path = dir_path

                created_files.append(self.create_zip_archive(pattern, dest_path, dir_path, files))

        return [created for created in created_files if created is not None]

    def run(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        return self.create_archives()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=IWONKA_DESC_STR)
    parser.add_argument("--path", help=PATH_DESC_STR)

    args = parser.parse_args()

    packer = FilePacker(dir_path=args.path)
    packer.run()
