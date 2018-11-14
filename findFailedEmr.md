## Usage
### How to run
Run this with proper account credentials.   
`python findFailedEmr.py [options]`   

### Options
All options are optional.
```
Usage: findFailedEmr.py [options]

Options:
  -h, --help            show this help message and exit
  -d DATE, --date=DATE  starting date for data
  -a ACCOUNT, --account=ACCOUNT
                        AWS account number
  --endDate=ENDDATE     ending date for data
  -e ERRORCODE, --errorCode=ERRORCODE
                        error code for EMR failure
  -t DDBTABLENAME, --ddbTableName=DDBTABLENAME
                        DDB table name where failed EMR info is stored
```

#### Date format
For both starting and ending date option, value should be in `YYYY-mm-dd` format.   

#### Account
To filter data based on account number, use `-a` option.   

#### Error code
Valid choices for error code are `'INTERNAL_ERROR', 'BOOTSTRAP_FAILURE', 'VALIDATION_ERROR', 'INSTANCE_FALURE', 'STEP_FAILURE'`. If not selected,
all errors will be queried.

#### DynamoDB Table Name
This is default to `failed-emr-info`. If you change the the default value of table name at the time of application deployment, then provide this option to query proper table.
