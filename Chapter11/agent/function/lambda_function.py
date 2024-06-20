import uuid
from openpyxl import Workbook
import boto3
from worksheet import CaseTemplate

s3_client = boto3.client('s3')
dynamodb = boto3.client('dynamodb')


def get_named_parameter(event, name):
    return next(item for item in event['parameters'] if item['name'] == name)['value']

def get_named_property(event, name):
    return next(item for item in event['requestBody']['content']['application/json']['properties'] if item['name'] == name)['value']

def generateCaseSheet(event):
    # Extract parameters
    client = get_named_parameter(event, 'client') 
    casename = get_named_parameter(event, 'casename')
    challenge = get_named_parameter(event, 'challenge')
    solution = get_named_parameter(event, 'solution')
    budget = float(get_named_parameter(event, 'budget'))
    kpi = get_named_parameter(event, 'kpi')

    # Generate unique ID
    unique_id = uuid.uuid1().int>>64

    param_dict = {
        'client': client,
        'caseid': unique_id,
        'casename': casename,
        'challenge': challenge,
        'solution': solution,
        'budget': budget,
        'kpi': kpi,
    }

    # Create and fill the price sheet with the given information
    wb = Workbook()
    t1 = CaseTemplate()
    wb = t1.build_template(wb, unique_id)
    wb = t1.fill_template_parameters(wb, param_dict)
    # Save the sheet and upload to s3
    t1.save_template(wb, '/tmp/new_case.xlsx')
    NEW_FILE_PATH = f'agent/output/{unique_id}_{client}.xlsx'
    s3_client.upload_file('/tmp/new_case.xlsx', 'bdok-539445819060', NEW_FILE_PATH)
    # Save sheet information on Dynamo Table
    dynamodb.put_item(
        TableName='case-sheets',
        Item={
            'caseSheetId': {
                'N': str(unique_id),
            },
            'sheetPath': {
                'S': f"s3://bdok-539445819060/{NEW_FILE_PATH}",
            },
            'client': {
                'S': client,
            },
            'casename': {
                'S': casename,
            },
            'challenge': {
                'S': challenge,
            },
            'solution': {
                'S': solution,
            },
            'budget': {
                'N': str(budget),
            },
            'kpi': {
                'S': kpi,
            }
        }
    )
    # Return response matching schema
    return {
        "id": str(unique_id),
        "client": client,
        "casename": casename,
        "challenge": challenge,
        "solution": solution,
        "budget": budget,
        "kpi": kpi
    }

def checkCase(event):
    # Extract parameter
    caseSheetId = get_named_parameter(event, 'caseSheetId')
    # Get information from Dynamo Table
    info = dynamodb.get_item(
        TableName='case-sheets',
        Key={
            'caseSheetId': {
                'N': str(caseSheetId),
            }
        }
    )
    client = info['Item']['client']['S']
    casename = info['Item']['casename']['S']
    challenge = info['Item']['challenge']['S']
    solution = info['Item']['solution']['S']
    budget = info['Item']['budget']['N']
    kpi = info['Item']['kpi']['S']

    # Return success response
    return {
        "id": str(caseSheetId),
        "client": client,
        "casename": casename,
        "challenge": challenge,
        "solution": solution,
        "budget": budget,
        "kpi": kpi
    }


def lambda_handler(event, context):

    response_code = 200
    action_group = event['actionGroup']
    api_path = event['apiPath']

    if api_path == '/generateCaseSheet':
        result = generateCaseSheet(event)
    elif api_path == '/checkCase':
        result = checkCase(event)
    else:
        response_code = 404
        result = f"Unrecognized api path: {action_group}::{api_path}"

    response_body = {
        'application/json': {
            'body': result 
        }
    }

    action_response = {
        'actionGroup': event['actionGroup'],
        'apiPath': event['apiPath'],
        'httpMethod': event['httpMethod'],
        'httpStatusCode': response_code,
        'responseBody': response_body
    }

    api_response = {'messageVersion': '1.0', 'response': action_response}
    return api_response
