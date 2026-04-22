# Deploy N-Queen Application to AKS

## Pré-requisitos

1. **Azure CLI** instalado e configurado
2. **kubectl** instalado
3. **Docker** instalado
4. **Azure Container Registry (ACR)** criado
5. **AKS Cluster** criado

## Passos para Deploy

### 1. Configurar Azure CLI e conectar ao AKS

```bash
# Login no Azure
az login

# Configurar subscription (substitua pelo seu subscription ID)
az account set --subscription "your-subscription-id"

# Conectar ao cluster AKS
az aks get-credentials --resource-group "your-resource-group" --name "your-aks-cluster"
```

### 2. Configurar Azure Container Registry

```bash
# Login no ACR
az acr login --name "your-acr-name"

# Construir e enviar a imagem para o ACR
docker build -t your-acr-name.azurecr.io/nqueen:latest .
docker push your-acr-name.azurecr.io/nqueen:latest

# Conectar AKS ao ACR (se não estiver conectado)
az aks update -n "your-aks-cluster" -g "your-resource-group" --attach-acr "your-acr-name"
```

### 3. Atualizar a imagem no manifesto

Edite o arquivo `k8s/nqueen-app.yaml` e substitua:
```yaml
image: nqueen:latest
```
por:
```yaml
image: your-acr-name.azurecr.io/nqueen:latest
```

### 4. Fazer o deploy no AKS

```bash
# Aplicar configurações do PostgreSQL
kubectl apply -f k8s/postgres-config.yaml
kubectl apply -f k8s/postgres.yaml

# Aguardar o PostgreSQL estar pronto
kubectl wait --for=condition=ready pod -l app=postgres --timeout=300s

# Aplicar configurações da aplicação
kubectl apply -f k8s/nqueen-config.yaml
kubectl apply -f k8s/nqueen-app.yaml

# Aplicar Ingress (opcional)
kubectl apply -f k8s/ingress.yaml
```

### 5. Verificar o deploy

```bash
# Verificar pods
kubectl get pods

# Verificar services
kubectl get services

# Verificar logs da aplicação
kubectl logs -l app=nqueen

# Port-forward para testar localmente
kubectl port-forward service/nqueen-service 8080:80
```

### 6. Acessar a aplicação

- **Local (port-forward)**: http://localhost:8080
- **Com Ingress**: Use o IP externo do Ingress
- **Com Load Balancer**: Mude o service type para LoadBalancer

## Comandos Úteis

```bash
# Escalar a aplicação
kubectl scale deployment nqueen-app --replicas=3

# Atualizar a aplicação
docker build -t your-acr-name.azurecr.io/nqueen:v2 .
docker push your-acr-name.azurecr.io/nqueen:v2
kubectl set image deployment/nqueen-app nqueen=your-acr-name.azurecr.io/nqueen:v2

# Deletar todos os recursos
kubectl delete -f k8s/
```

## Configurações de Produção Recomendadas

1. **Use secrets externos** como Azure Key Vault
2. **Configure resource limits** apropriados
3. **Configure health checks** personalizados
4. **Use Azure Application Gateway** como Ingress Controller
5. **Configure backup** do PostgreSQL
6. **Monitor com Azure Monitor** ou Prometheus
7. **Configure SSL/TLS** no Ingress

## Troubleshooting

```bash
# Verificar eventos do cluster
kubectl get events --sort-by=.metadata.creationTimestamp

# Verificar logs detalhados
kubectl describe pod <pod-name>

# Acessar o container
kubectl exec -it <pod-name> -- /bin/bash
```