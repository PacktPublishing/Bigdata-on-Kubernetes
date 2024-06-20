# Create namespace
kubectl create namespace genai

# Create the necessary credentials and the configmap
kubectl create secret generic aws-credentials --from-literal=aws_access_key_id=<YOUR_ACCESS_KEY_ID> --from-literal=aws_secret_access_key="<YOUR_SECRET_ACCESS_KEY>" -n genai
kubectl create configmap kb-config --from-literal=kb_id=<YOUR_KB_ID> -n genai 

# Deploy the chatbot and the LoadBalancer
kubectl apply -f deploy_chat_with_claude.yaml -n genai
