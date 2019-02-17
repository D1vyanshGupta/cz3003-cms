"""
    Pulls dengue cluster information from data.gov.sg
"""

import requests
import zipfile
import os
import json
from ..models import Dengue
from django.core.serializers import serialize


class DengueAPI:

    """
        DengueAPI Class for dengue.py
    """
    DENGUE_URL = "https://ref.data.gov.sg/common/Handler.ashx?ThemeName=DENGUE_CLUSTER&MetaDataID=227753&Format=shp"
    DENGUE_SHP_FILENAME = "DENGUE_CLUSTER.shp"
    DENGUE_ZIP_FILENAME = "DENGUE_CLUSTER.zip"
    DENGUE_EXTRACTED_FOLDER = "pullapis/dengue_extracted"

    def download_file(self, url, download_file_name):
        """
            Download the necessary file
        """
        r = requests.get(url, stream=True)
        if (r.status_code == 200):
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
            # os.remove(zippedfile)
            return True
        except (zipfile.BadZipfile):
            print("error with zipfile")
            return False

    def update_dengue_info_in_database(self, file_directory):
        """
            Update dengue information into the database
        """
        command_to_run = "shp2pgsql -s 3414 -d -W LATIN1 %s cms_dengue | psql -d cms" % file_directory
        os.system(command_to_run)

    def pull_update(self):
        """
            Pull the dengue update
        """
        try:
            if (self.download_file(self.DENGUE_URL, self.DENGUE_ZIP_FILENAME)):
                if (self.unzip(self.DENGUE_ZIP_FILENAME, self.DENGUE_EXTRACTED_FOLDER)):
                    file_directory = "%s/%s" % (
                        self.DENGUE_EXTRACTED_FOLDER, self.DENGUE_SHP_FILENAME)
                    self.update_dengue_info_in_database(file_directory)
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
        dengue = Dengue.objects.all()
        dengue_json = json.loads(serialize('geojson', dengue))
        for x in dengue_json['features']:
            x['properties']['type'] = 'dengue'
        return dengue_json
