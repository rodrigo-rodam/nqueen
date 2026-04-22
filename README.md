# nqueen

Esta aplicação é uma implementação do problema N-Queens usando Flask e Docker.
Fornece uma API REST para resolver o problema N-Queens para um tamanho de tabuleiro dado.

## Desenvolvimento Local

### Setup do ambiente Python
```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Usando Docker Compose
```bash
docker-compose up -d --build
```

Acesse:
- Aplicação: http://localhost:8080/
- Swagger API: http://localhost:8080/api/

## Deploy no Azure Kubernetes Service (AKS)

### Pré-requisitos
- Azure CLI instalado e configurado
- kubectl instalado
- Docker instalado
- Azure Container Registry (ACR) criado
- AKS Cluster criado

### Deploy Automático

Use o script PowerShell fornecido:

```powershell
.\deploy.ps1 -ResourceGroup "your-resource-group" -AksCluster "your-aks-cluster" -AcrName "your-acr-name"
```

### Deploy Manual

Veja instruções detalhadas em [`k8s/README.md`](k8s/README.md)

#### Passos Rápidos:

1. **Login e configuração**:
```bash
az login
az aks get-credentials --resource-group "your-rg" --name "your-aks"
```

2. **Build e push da imagem**:
```bash
az acr login --name "your-acr"
docker build -t your-acr.azurecr.io/nqueen:latest .
docker push your-acr.azurecr.io/nqueen:latest
```

3. **Deploy no Kubernetes**:
```bash
kubectl apply -f k8s/postgres-config.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/nqueen-config.yaml
kubectl apply -f k8s/nqueen-app.yaml
kubectl apply -f k8s/ingress.yaml
```

4. **Verificar deploy**:
```bash
kubectl get pods
kubectl port-forward service/nqueen-service 8080:80
```

### Arquivos Kubernetes

- `k8s/postgres-config.yaml` - Configuração do PostgreSQL
- `k8s/postgres.yaml` - Deployment do PostgreSQL
- `k8s/nqueen-config.yaml` - Configuração da aplicação
- `k8s/nqueen-app.yaml` - Deployment da aplicação
- `k8s/ingress.yaml` - Ingress controller
- `k8s/production.yaml` - Configuração para produção com HPA

### Configurações de Produção

Para produção, use o manifesto otimizado:
```bash
kubectl apply -f k8s/production.yaml
```

Inclui:
- ✅ Múltiplas réplicas
- ✅ Health checks otimizados
- ✅ Resource limits apropriados
- ✅ Horizontal Pod Autoscaler
- ✅ Pod Disruption Budget
- ✅ Security contexts

## Troubleshooting

### Docker
Se encontrar problemas com pacotes Python:
```bash
pip install <package-name>  # Sem especificar versão
```

### Kubernetes
```bash
# Verificar logs
kubectl logs -l app=nqueen

# Verificar eventos
kubectl get events --sort-by=.metadata.creationTimestamp

# Debug de pods
kubectl describe pod <pod-name>
```

## Tecnologias Utilizadas

- **Python 3.9** - Linguagem principal
- **Flask** - Framework web
- **Flask-RESTPlus** - API REST
- **PostgreSQL** - Banco de dados
- **Docker** - Containerização
- **Kubernetes** - Orquestração
- **Azure AKS** - Cluster Kubernetes gerenciado
- **Gunicorn** - Servidor WSGI para produção
