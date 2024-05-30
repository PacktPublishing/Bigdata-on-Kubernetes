kubectl create configmap agent-config --from-literal=agent_alias_id=<YOUR_ALIAS_ID> --from-literal=agent_id=<YOUR_AGENT_ID> -n genai

kubectl apply -f deploy_agent.yaml -n genai