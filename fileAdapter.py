import abc
from IReleaseData import ReleaseData
import json

class FileAdapter(ReleaseData):

    def getReleases(self):
        json_data = open("fake_data.json").read()
        releases = json.loads(json_data)
        return releases;


    def getLabels(self):
        releases = self.getReleases()
        labels = []
        for release in releases:
            for label in releases[release]['labels']:
                if label not in labels:
                    labels.append(label)
        return labels
