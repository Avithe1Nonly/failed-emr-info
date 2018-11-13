import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')
emr = boto3.client('emr')

dynamoTable = dynamodb.Table(os.environ['dynamoTableName'])

def lambda_handler(event, context):
    print event
    if event['detail-type'] == 'EMR Cluster State Change':
        if event['detail']['state'] == 'TERMINATED_WITH_ERRORS':
            item = event
            if 'stateChangeReason' in item['detail']:
                stateChangeReason = json.loads(item['detail']['stateChangeReason'])
                item['detail'].pop('stateChangeReason', None)
                for state in stateChangeReason:
                    if stateChangeReason[state] == '':
                        item[state] = 'None'
                    else:
                        item[state] = stateChangeReason[state]

            item.pop('id', None)
            item['clusterId'] = item['detail'].pop('clusterId', None)
            item['eventTime'] = item.pop('time', None)

            print item
            response = dynamoTable.put_item(
              Item = item
            )
