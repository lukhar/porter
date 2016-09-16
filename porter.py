from __future__ import print_function
import sys
import os
import subprocess
import arrow
import shutil


def fetch_creation_date(path):
    date_positon = 3
    raw_output = subprocess.check_output(['exiftool', '-EXIF:CreateDate', path])
    raw_date = raw_output.split()[date_positon]

    return arrow.get(raw_date, 'YYYY:MM:DD').date()


if __name__ == '__main__':
    source, destination = sys.argv[1], sys.argv[2]

    for dirpath, _, filenames in os.walk(source):
        for filename in filenames:
            if filename[-3:] not in {'PEF', 'pef'}:
                continue

            source_photo_path = os.path.join(dirpath, filename)
            creation_date = fetch_creation_date(source_photo_path)
            destination_photo_path = os.path.join(destination,
                                                  str(creation_date.year),
                                                  str(creation_date.month),
                                                  str(creation_date.day),
                                                  filename)
            try:
                os.makedirs(os.path.dirname(destination_photo_path))
            except OSError:
                pass

            print('Copying {} to {}'.format(source_photo_path, destination_photo_path))

            shutil.copy(source_photo_path, destination_photo_path)
