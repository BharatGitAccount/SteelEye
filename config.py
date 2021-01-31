import boto3

# configurations used for fetching/converting/generating the files
xmlfilename = "select.xml"
csvheader = ['FinInstrmGnlAttrbts.Id', 'FinInstrmGnlAttrbts.FullNm', 'FinInstrmGnlAttrbts.ClssfctnTp',
             'FinInstrmGnlAttrbts.CmmdtyDerivInd', 'FinInstrmGnlAttrbts.NtnlCcy', 'Issr']
xmlurl = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:" \
         "%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100"

# directory location where all the files will be stored
downloaddir = "E://temp//"

# AWS S3 configuration
s3 = boto3.resource(
    service_name='s3',
    region_name='ap-south-1',
    aws_access_key_id='AKIA2F4YQJGR5PLWHU6P',
    aws_secret_access_key='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'
)

# S3 bucket to be used for uploading csv files
s3_bucket_name = "bharatpatel"
