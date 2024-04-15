eksctl create cluster --managed --alb-ingress-access --node-private-networking --full-ecr-access --name=studycluster --instance-types=m6i.xlarge --region=us-east-1 --nodes-min=3 --nodes-max=4 --nodegroup-name=ng-studycluster

eksctl utils associate-iam-oidc-provider --region=us-east-1 --cluster=studycluster --approve

eksctl create iamserviceaccount --name ebs-csi-controller-sa --namespace kube-system --cluster studycluster --role-name AmazonEKS_EBS_CSI_DriverRole --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy --approve

eksctl create addon --name aws-ebs-csi-driver --cluster studycluster --service-account-role-arn arn:aws:iam::<MY_ACCOUNT_NUMBER>:role/AmazonEKS_EBS_CSI_DriverRole --force

kubectl create namespace spark-operator

helm install spark-operator https://github.com/kubeflow/spark-operator/releases/download/spark-operator-chart-1.1.27/spark-operator-1.1.27.tgz --namespace spark-operator --set webhook.enable=true

kubectl create secret generic aws-credentials --from-literal=aws_access_key_id=<YOUR_ACCESS_KEY_ID> --from-literal=aws_secret_access_key="<YOUR_SECRET_ACCESS_KEY>" -n spark-operator
