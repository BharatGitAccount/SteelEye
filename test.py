import unittest
from os import path
from os import listdir
from os.path import isfile, join
from config import xmlurl, downloaddir, xmlfilename, s3, s3_bucket_name
from main import uploadfiletos3, downloadFile, extractZipFile


class TestMain(unittest.TestCase):
    def test_uploadfiletos3(self):
        uploadfiletos3()

        files = [f for f in listdir(downloaddir) if isfile(join(downloaddir, f))]
        for file in files:
            if file.endswith(".csv"):
                objs = list(s3.Bucket(s3_bucket_name).objects.filter(Prefix=file))
                if len(objs) > 0:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)

    def test_downloadFile(self):
        downloadFile(xmlurl, xmlfilename)
        self.assertTrue(path.exists(downloaddir + xmlfilename))

    def test_extractZipFile(self):
        extractZipFile("E:/temp/Temp.zip")
        self.assertTrue(path.exists(downloaddir + "Temp.txt"))


if __name__ == '__main__':
    unittest.main()
