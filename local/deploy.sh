#!/usr/bin/env bash
set -euo pipefail

echo "==> Building image inside minikube's docker daemon"
eval "$(minikube docker-env)"
docker build -t aks-lab-app:v1 ./app

echo "==> Applying manifests"
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s-local/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml

echo "==> Waiting for rollout"
kubectl rollout status deployment/aks-lab-app -n akslab

MINIKUBE_IP=$(minikube ip)
echo ""
echo "Done. Try:"
echo "  curl -H \"Host: akslab.local\" http://${MINIKUBE_IP}/"
