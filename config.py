import boto3

xmlFileName = "select.xml"
xmlURL = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:" \
         "%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100"
downloadDir = "E://temp//"
csvHeader = ['FinInstrmGnlAttrbts.Id', 'FinInstrmGnlAttrbts.FullNm', 'FinInstrmGnlAttrbts.ClssfctnTp',
             'FinInstrmGnlAttrbts.CmmdtyDerivInd', 'FinInstrmGnlAttrbts.NtnlCcy', 'Issr']

s3 = boto3.resource(
    service_name='s3',
    region_name='ap-south-1',
    aws_access_key_id='AKIA2F4YQJGR5PLWHU6P',
    aws_secret_access_key='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'
)

s3_bucket_name = "bharatpatel"
