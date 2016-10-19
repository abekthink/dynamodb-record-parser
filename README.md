# dynamodb-record-parser

## the parser function

parse_dynamodb_record(): parse the data structure sent by DynamoDB to Lambda using python

## invoke the function

parse_dynamodb_record(record)

## input params

input params: a dynamodb record sent by the dynamodb trigger(lambda function)
```python
record = {
    "SequenceNumber": "6321200000000003285225378",
    "Keys": {
        "key": {
            "S": "test123"
        }
    },
    "SizeBytes": 14330,
    "ApproximateCreationDateTime": 1476859080,
    "StreamViewType": "NEW_AND_OLD_IMAGES",
    "OldImage": {
        "integer": {
            "N": "123"
        },
        "string": {
            "S": "xxx"
        }
    },
    "NewImage": {
        "integer": {
            "N": "345"
        },
        "string": {
            "S": "zzz"
        }
    }
}
```

## output result:

output result: the dictionary data in python
```python
{
    "SequenceNumber": "6321200000000003285225378", 
    "OldImage": {
        "string": "xxx", 
        "integer": 123, 
    }, 
    "Keys": {
        "key": "test123"
    }, 
    "SizeBytes": 14330, 
    "NewImage": {
        "string": "zzz", 
        "integer": 345, 
    }, 
    "ApproximateCreationDateTime": 1476859080, 
    "StreamViewType": "NEW_AND_OLD_IMAGES"
}
```
