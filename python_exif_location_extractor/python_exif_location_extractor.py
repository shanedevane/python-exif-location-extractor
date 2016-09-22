# -*- coding: utf-8 -*-

import os
import exifread
from PIL import Image, ImageStat, ImageChops, ImageEnhance
from PIL.ExifTags import TAGS, GPSTAGS
import json


class PythonExifLocationExtractor:

    def __init__(self, file_path):
        self._file_path = file_path
        self._json_data = dict()
        self._image = None
        self._pil_tags = dict()

    @property
    def json(self):
        return json.dumps(self._json_data)

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

    def _convert_to_degress(self, value):
        """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
        d0 = value[0][0]
        d1 = value[0][1]
        d = float(d0) / float(d1)

        m0 = value[1][0]
        m1 = value[1][1]
        m = float(m0) / float(m1)

        s0 = value[2][0]
        s1 = value[2][1]
        s = float(s0) / float(s1)
        return d + (m / 60.0) + (s / 3600.0)

    def _store_gps_data(self):
        if self._gps_data:
            gps_latitude = self._gps_data.get("GPSLatitude", None)
            gps_latitude_ref = self._gps_data.get("GPSLatitudeRef", None)
            gps_longitude = self._gps_data.get("GPSLongitude", None)
            gps_longitude_ref = self._gps_data.get("GPSLongitudeRef", None)

            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                lat = self._convert_to_degress(gps_latitude)
                if gps_latitude_ref != "N":
                    lat = 0 - lat

                lon = self._convert_to_degress(gps_longitude)
                if gps_longitude_ref != "E":
                    lon = 0 - lon

            self._json_data['latitude'] = lat
            self._json_data['longitude'] = lon

    def execute(self):
        self._image = Image.open(self._file_path)
        self._get_exif_data()
        self._get_gps_data()
        self._store_gps_data()


if __name__ == "__main__":
    extractor = PythonExifLocationExtractor('../Resources/pacers.jpg')
    extractor.execute()
    print(extractor.json)
