"""
    Pulls dengue cluster information from data.gov.sg
"""
import os
import json
import shutil
import zipfile

import requests

from ..models import Dengue
from django.core.serializers import serialize


class DengueAPI:

    """
        DengueAPI Class for dengue.py
    """
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    DENGUE_URL = 'https://data.gov.sg/dataset/e7536645-6126-4358-b959-a02b22c6c473/download'
    DENGUE_ZIP_FILENAME = os.path.join(CURRENT_DIR, 'DENGUE_CLUSTER.zip')
    DENGUE_EXTRACTED_FOLDER = os.path.join(CURRENT_DIR, 'dengue_extracted')
    DENGUE_SHP_FILENAME = "DENGUE_CLUSTER.shp"

    def download_file(self, url, download_file_name):
        """
            Download the necessary file
        """
        r = requests.get(url, stream=True)
        if (r.status_code == 200):
            if os.path.isfile(self.DENGUE_ZIP_FILENAME):
                os.remove(self.DENGUE_ZIP_FILENAME)

            if os.path.isdir(self.DENGUE_EXTRACTED_FOLDER):
                shutil.rmtree(self.DENGUE_EXTRACTED_FOLDER)

            os.makedirs(self.DENGUE_EXTRACTED_FOLDER)

            with open(download_file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return True
        else:
            print(r.status_code)
            return False

    def unzip(self, zipped_file, extract_location):
        """
            Unzip a file
        """
        try:
            zip = zipfile.ZipFile(zipped_file)
            zip.extractall(extract_location)
            return True
        except (zipfile.BadZipfile):
            print("error with zipfile")
            return False

    def update_dengue_info_in_database(self, file_directory):
        """
            Update dengue information into the database
        """
        geojson_file_path = os.path.join(file_directory, 'dengue-clusters-geojson.geojson')
        # shp_file_path = os.path.join(file_directory, 'DENGUE_CLUSTER.shp')
        # command_to_convert_to_shp = 'ogr2ogr -f "ESRI Shapefile" {} "{}"'.format(shp_file_path, geojson_file_path)
        # os.system(command_to_convert_to_shp)
        # command_to_run = "shp2pgsql -s 3414 -d -W LATIN1 %s cms_dengue | psql -d cms" % shp_file_path
        command_to_run = 'ogr2ogr -f "PostgreSQL" PG:"dbname=cms user=divyanshgupta" "{}" -nln cms_dengue -append'.format(geojson_file_path)
        os.system(command_to_run)

    def pull_update(self):
        """
            Pull the dengue update
        """
        try:
            if (self.download_file(self.DENGUE_URL, self.DENGUE_ZIP_FILENAME)):
                if (self.unzip(self.DENGUE_ZIP_FILENAME, self.DENGUE_EXTRACTED_FOLDER)):
                    self.update_dengue_info_in_database(self.DENGUE_EXTRACTED_FOLDER)
                    return True
            return False
        except Exception as e:
            print(e)
            return False

    def return_geo_json(self):
        """
            Return geo json format of dengue
        """
        self.pull_update()
        geojson_file_path = os.path.join(self.DENGUE_EXTRACTED_FOLDER, 'dengue-clusters-geojson.geojson')
        with open(geojson_file_path, 'rb') as file:
            dengue_json = json.load(file)
            for x in dengue_json['features']:
                x['properties']['type'] = 'dengue'
            return dengue_json
