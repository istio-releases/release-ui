import abc

class ReleaseData(object):
    """ABC to retrieve data from File Adapter and Airflow Adapter"""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getReleases(self):
        """Retrieve all release information"""
        pass


    @abc.abstractmethod
    def getLabels(self):
        """Retrieve all possible labels for UI"""
        pass
