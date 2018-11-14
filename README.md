Serverless application to collect failed EMR info from CloudWatch events and store to DynamoDB table.

This application will deploy a CloudWatch rule to catch EMR cluster event when it is terminated with errors. CW rule will invoke a lambda that will store details about error in Dynamo table.

Once this application is deployed, you can use the python script provided in github repo to query the Dynamo table and fetch the report of failed clusters.
