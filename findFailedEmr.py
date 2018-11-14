import boto3
import json
from boto3.dynamodb.conditions import Attr
from optparse import OptionParser
from botocore.exceptions import ClientError

parser = OptionParser()
parser.add_option("-d", "--date",
                  help="starting date for data",)
parser.add_option("-a", "--account",
                  help="AWS account number",)
parser.add_option("--endDate",
                  help="ending date for data",)
parser.add_option("-e", "--errorCode",
                  choices=['INTERNAL_ERROR', 'BOOTSTRAP_FAILURE', 'VALIDATION_ERROR', 'INSTANCE_FALURE', 'STEP_FAILURE', 'ALL',],
                  default='ALL',
                  help="error code for EMR failure")
parser.add_option("-t", "--ddbTableName",
                  default='failed-emr-info',
                  help="DDB table name where failed EMR info is stored. Default: failed-emr-info")
parser.add_option("-r", "--region",
                  default='us-west-2',
                  help="AWS region. Default: us-west-2")

(options, args) = parser.parse_args()

client = boto3.client('dynamodb', region_name=options.region)
paginator = client.get_paginator('scan')

operation_parameters = {
  'TableName': options.ddbTableName,
}

operation_parameters['FilterExpression'] = ''
operation_parameters['ExpressionAttributeValues'] = {}

if options.errorCode != 'ALL':
    operation_parameters['FilterExpression'] += 'code = :x'
    operation_parameters['ExpressionAttributeValues'][':x'] = {'S': options.errorCode}
if options.date != None:
    if operation_parameters['FilterExpression'] != '':
	operation_parameters['FilterExpression'] += ' AND '
    operation_parameters['FilterExpression'] += 'eventTime >= :y'
    operation_parameters['ExpressionAttributeValues'][':y'] = {'S': options.date}
if options.endDate != None:
    if operation_parameters['FilterExpression'] != '':
        operation_parameters['FilterExpression'] += ' AND '
    operation_parameters['FilterExpression'] += 'eventTime <= :z'
    operation_parameters['ExpressionAttributeValues'][':z'] = {'S': options.endDate}
if options.account != None:
    if operation_parameters['FilterExpression'] != '':
        operation_parameters['FilterExpression'] += ' AND '
    operation_parameters['FilterExpression'] += 'account = :a'
    operation_parameters['ExpressionAttributeValues'][':a'] = {'S': options.account}

if operation_parameters['FilterExpression'] == '':
    del operation_parameters['FilterExpression']
    del operation_parameters['ExpressionAttributeValues']
try:
    page_iterator = paginator.paginate(**operation_parameters)
    for page in page_iterator:
        for item in page['Items']:
        	name = item['detail']['M']['name']['S']
        	name = name.split('-')
        	name = name[:len(name)-5]
        	name = '-'.join(name)
                print item['clusterId']['S'] + ',' + name + ','  + item['code']['S'] + ',' + item['message']['S'] + ',' + item['eventTime']['S'] + ',' + item['account']['S']
except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceNotFoundException':
        print("Table %s not found" %options.ddbTableName)
