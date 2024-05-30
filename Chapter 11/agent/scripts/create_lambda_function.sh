IAM_ROLE=$1

aws lambda create-function \
    --function-name generateCaseSheet \
    --runtime python3.9 \
    --role ${IAM_ROLE} \
    --handler lambda_function.lambda_handler \
    --timeout 600 \
    --memory-size 256 \
    --package-type Zip \
    --zip-file fileb://lambda_function_payload.zip