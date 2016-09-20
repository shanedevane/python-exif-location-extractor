# -*- coding: utf-8 -*-

import os
import exifread
from PIL import Image, ImageStat, ImageChops, ImageEnhance
from PIL.ExifTags import TAGS, GPSTAGS


class PythonExifLocationExtractor:

    def __init__(self, file_path):
        self._file_path = file_path
        self.json = None
        self._json_data = dict()
        self._image = None
        self._pil_tags = dict()

    def _get_exif_data(self):
        if self._image._getexif():
            for tag in self._image._getexif():
                try:
                    decoded = TAGS.get(tag, tag)
                    self._pil_tags[decoded] = self._image._getexif().get(tag)
                except AttributeError as e:
                    # print("AttributeError" + str(e))
                    pass

        try:
            exif = exifread.process_file(self._image, details=True)
            self._exif_read_tags = exif
        except AttributeError as e:
            # print("AttributeError" + str(e))
            pass
        except MemoryError as e:
            # print("MemoryError" + str(e))
            pass

    def _get_gps_data(self):
        gps_exif_data = self._pil_tags.get('GPSInfo', None)
        if gps_exif_data:
            gps_data = {}
            for t in gps_exif_data:
                sub_decoded = GPSTAGS.get(t, t)
                gps_data[sub_decoded] = gps_exif_data[t]
            self._gps_data = gps_data

    def _store_gps_data(self):
        if self._get_gps_data:
            # self._json_data
            pass

    def execute(self):
        self._image = Image.open(self._file_path)
        self._get_exif_data()
        self._get_gps_data()
        self._store_gps_data()


if __name__ == "__main__":
    extractor = PythonExifLocationExtractor('../Resources/pacers.jpg')
    extractor.execute()
    print(extractor.json)




