eksctl create cluster --managed --alb-ingress-access --node-private-networking --full-ecr-access --name=studycluster --instance-types=m6i.xlarge --region=us-east-1 --nodes-min=3 --nodes-max=4 --nodegroup-name=ng-studycluster

kubectl create namespace spark-operator

helm install spark-operator https://github.com/kubeflow/spark-operator/releases/download/spark-operator-chart-1.1.27/spark-operator-1.1.27.tgz --namespace spark-operator --set webhook.enable=true

kubectl create secret generic aws-credentials --from-literal=aws_access_key_id=<YOUR_ACCESS_KEY_ID> --from-literal=aws_secret_access_key="<YOUR_SECRET_ACCESS_KEY>" -n spark-operator
