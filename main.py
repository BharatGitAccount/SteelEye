import requests
import boto3
from botocore.exceptions import ClientError
import csv
import zipfile
import logging
from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET
from config import xmlURL, downloadDir, xmlFileName, csvHeader, s3, s3_bucket_name

logging.basicConfig(level=logging.DEBUG)


def downloadFile(url, filename):
    """
    This function downloads and saves the contents of the URL into a local file
    :param url: The link to the online resource
    :param filename: Filename by which the contents of the URL will be saved on local machine
    :return:
    """
    logging.info("Downloading file - " + url)
    r = requests.get(url, allow_redirects=True)
    open(downloadDir + filename, 'wb').write(r.content)


def parseXMLandGetURLList() -> object:
    """
    This function will parse the select.xml file and get the list of zip files to download.
    :return: List of all zip files to be downloaded
    """
    logging.info("Parsing xml file...")

    tree = ET.parse(downloadDir + 'select.xml')
    root = tree.getroot()

    urllist = []

    for child in root:
        if child.tag == 'result':
            for newChild in child:
                logging.info("Adding %s to the list", newChild[1].text)
                urllist.append(newChild[1].text)

    return urllist


def extractZipFile(filepath):
    """
    This function extracts the zip file on the local disk
    :param filepath: Filepath of the zip file
    :return:
    """
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(downloadDir)


def convertXMLToCSV(filepath):
    """
    This function converts the xml file to csv and saves the csv file on the local disk
    :param filepath: Filepath of the input xml file
    :return:
    """
    logging.info("Converting xml file (%s) to csv...", filepath)
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()

        csvdata = []

        for child in root.getchildren():
            if child.tag.endswith('Pyld'):
                for dataNode in child.getchildren()[0].getchildren()[0].getchildren():
                    id = ""
                    fullnm = ""
                    shrtnm = ""
                    clssfctntp = ""
                    ntnlccy = ""
                    cmmdtyderivind = ""
                    issr = ""

                    for ele in dataNode.getchildren()[0].getchildren():
                        if ele.tag.endswith("FinInstrmGnlAttrbts"):
                            id = ele.getchildren()[0].text
                            fullnm = ele.getchildren()[1].text
                            shrtnm = ele.getchildren()[2].text
                            clssfctntp = ele.getchildren()[3].text
                            ntnlccy = ele.getchildren()[4].text
                            cmmdtyderivind = ele.getchildren()[5].text

                        if ele.tag.endswith("Issr"):
                            issr = ele.text

                    if id != "":
                        csvdata.append({csvHeader[0]: id, csvHeader[1]: fullnm, csvHeader[2]: clssfctntp,
                                        csvHeader[3]: cmmdtyderivind, csvHeader[4]: ntnlccy, csvHeader[5]: issr})

        logging.info("File conversion successful.")
        return csvdata
    except:
        print("error parsing file")


def writecsv(csvdata, filename):
    """
    This function will write the content to the csv file
    :param csvdata: Comma separated data
    :param filename: Output file name
    :return:
    """
    logging.info("Writing file - " + filename)

    try:
        with open(downloadDir + filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csvHeader)
            writer.writeheader()
            writer.writerows(csvdata)

        logging.info("CSV file created.")
    except:
        logging.error("Error occurred while writing csv file.,")


def uploadfiletos3() -> bool:
    """
    This function will update all the CSV files found in the downloadDir to the S3 bucket
    :rtype: bool
    """
    try:
        files = [f for f in listdir(downloadDir) if isfile(join(downloadDir, f))]
        for file in files:
            if file.endswith(".csv"):
                logging.info("Uploading file (%s) to S3 bucket (%s)...", downloadDir + file, s3_bucket_name)
                s3.Bucket(s3_bucket_name).upload_file(Filename=downloadDir + file, Key=file)
                logging.info("File upload successful.")
    except ClientError as e:
        logging.error("Error occurred while uploading file to S3.")
        logging.error(e)
        return False
    return True


if __name__ == '__main__':
    # download select.xml file
    downloadFile(xmlURL, xmlFileName)

    # create the list of zip files to be downloaded
    urlList = parseXMLandGetURLList()

    for url in urlList:
        # Download the zip file
        downloadFile(url, url.split("/")[-1])

        # extract zip file to get the xml data files
        extractZipFile(downloadDir + url.split("/")[-1])

        # generate data to be saved into csv file
        csvData = convertXMLToCSV(downloadDir + url.split("/")[-1].replace("zip", "xml"))

        if csvData is not None:
            # save data into csv file
            writecsv(csvData, (url.split("/")[-1]).replace('.zip', '.csv'))

    # upload csv files to S3 bucket
    uploadfiletos3()
