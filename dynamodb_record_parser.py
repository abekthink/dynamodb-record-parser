#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: abekthink
#
# Copyright 2016 GURU Tech, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import with_statement

import traceback
import json
from decimal import Decimal
from boto3.dynamodb.types import Binary


def parse_dynamodb_record(record):
    # the main function: transforms a dynamodb record into dict-type data
    if not record:
        return None

    result = {}
    if isinstance(record, dict):
        for (key, value) in record.items():
            if isinstance(record[key], dict):
                result[key] = format_dict(value)
            else:
                result[key] = value
    else:
        print("record is invalid: " + json.dumps(record))
        traceback.print_exc()
        return None
    return result


def format_dict(data):
    if not data:
        return None

    result = {}
    for (key, value) in data.items():
        first_item_key = value.items()[0][0]
        first_item_value = value.items()[0][1]
        result[key] = format_attribute(first_item_key, first_item_value)
    return result


def format_attribute(key, value):
    if key == 'M':
        return format_dict(value)
    elif key == 'L':
        res_array = []
        for item in value:
            first_item_key = item.items()[0][0]
            first_item_value = item.items()[0][1]
            res_array.append(format_attribute(first_item_key, first_item_value))
        return res_array
    elif key in ['NS', 'SS', 'BS']:
        res_array = []
        for item in value:
            res_array.append(format_attribute(key[0], item))
        return res_array
    # elif key == 'NS':
    #     # fix bug: can not invoke format_attribute() to generate the number set(NS)
    #     # eg: some_set = NS[123, 12.1, 456], generate a set mixed with int and decimal if invoke format_attribute()
    #     return get_number_set(value)
    elif key == 'B':
        return Binary(value)
    elif key == 'S':
        return value
    elif key == 'N':
        if value:
            if is_integer(value):
                return int(value)
            else:
                return Decimal(value)
        else:
            return None

    elif key == 'NULL':
        return None
    else:
        print("key is invalid: key=" + key)
        traceback.print_exc()
        return None


# def get_number_set(number_set):
#     result = set([])
#     if is_integer_set(number_set):
#         result = set([int(i) for i in number_set])
#     else:
#         result = set([Decimal(i) for i in number_set])
#     return result
#
#
# def is_integer_set(number_set):
#     flag = True
#     for i in number_set:
#         if not is_integer(i):
#             flag = False
#             break
#     return flag


def is_integer(i):
    if isinstance(i, int):
        return True
    i = str(i).lstrip('-+')
    return not i.startswith('0') and i.isdigit()


# Helper class to convert a DynamoDB item to JSON.
class CommonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        elif isinstance(o, Binary):
            return o.value
        elif isinstance(o, set):
            return [x for x in o]
        super(CommonEncoder, self).default(o)


if __name__ == "__main__":
    # test case
    dynamodb_record = {
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
            "decimal": {
                "N": "234.1"
            },
            "string": {
                "S": "xxx"
            },
            "boolean": {
                "NULL": 'true'
            },
            "list": {
                "L": [
                    {
                        "S": "yyy"
                    },
                    {
                        "N": "123"
                    }
                ]
            },
            "map": {
                "M": {
                    "key1": {
                        "N": "123"
                    },
                    "key2": {
                        "S": "346"
                    }
                }
            },
            "list_map": {
                "L": [
                    {
                        "M": {
                            "key3": {
                                "N": "123"
                            },
                            "key4": {
                                "S": "xxx"
                            }
                        }
                    },
                    {
                        "N": "123"
                    }
                ]
            },
            "binary_set": {
                "BS": [b"U3Vubnk=", b"UmFpbnk=", b"U25vd3k="]
            },
            "number_set": {
                "NS": ["42.2", "-19", "7.5", "3.14"]
            },
            "string_set": {
                "SS": ["Giraffe", "Hippo" ,"Zebra"]
            }
        },
        "NewImage": {
            "integer": {
                "N": "345"
            },
            "decimal": {
                "N": "123.1"
            },
            "string": {
                "S": "zzz"
            },
            "boolean": {
                "NULL": 'true'
            },
            "list": {
                "L": [
                    {
                        "S": "aaa"
                    },
                    {
                        "N": "234"
                    }
                ]
            },
            "map": {
                "M": {
                    "key1": {
                        "N": "123"
                    },
                    "key2": {
                        "S": "346"
                    }
                }
            },
            "list_map": {
                "L": [
                    {
                        "M": {
                            "key3": {
                                "N": "123"
                            },
                            "key4": {
                                "S": "xxx"
                            }
                        }
                    },
                    {
                        "N": "123"
                    }
                ]
            },
            "binary_set": {
                "BS": [b"U3Vubnk=", b"UmFpbnk=", b"U25vd3k="]
            },
            "number_set": {
                "NS": ["42.2", "-19", "7.5", "3.14"]
            },
            "string_set": {
                "SS": ["Giraffe", "Hippo", "Zebra"]
            }
        }
    }

    print(json.dumps(parse_dynamodb_record(dynamodb_record), indent=4, cls=CommonEncoder))
