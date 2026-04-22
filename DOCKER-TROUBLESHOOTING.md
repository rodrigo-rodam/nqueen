# 🐳 Solucionando Problemas do Docker

## Problema Atual
```
error during connect: Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.51/containers/json": 
open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```

## ✅ Soluções

### 1. **Iniciar Docker Desktop (Mais Simples)**

1. Procure "Docker Desktop" no menu Iniciar
2. Clique com o botão direito e escolha "Executar como administrador"
3. Aguarde 2-3 minutos para inicializar completamente
4. Verifique se o ícone do Docker na bandeja do sistema está verde

### 2. **Via PowerShell (Alternativa)**
```powershell
# Tentar iniciar o Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Aguardar alguns minutos e testar
docker version
```

### 3. **Verificar Serviços do Docker**
```powershell
# Verificar serviços
Get-Service docker*

# Iniciar serviço se necessário (como admin)
Start-Service com.docker.service
```

## 🚀 Continuar Deploy Sem Docker Local

Se o Docker não funcionar, use o script alternativo:

```powershell
# Deploy apenas com kubectl (sem construir imagem localmente)
.\deploy-kubectl-only.ps1 -ResourceGroup "nqueen-rg" -AksCluster "nqueen-aks" -AcrName "nqueenacr"
```

Este script:
- ✅ Não precisa do Docker local
- ✅ Usa imagem existente no ACR ou nginx para teste
- ✅ Permite testar o deploy rapidamente

## 📦 Construir Imagem Manualmente Depois

Quando o Docker funcionar:

```powershell
# Login no ACR
az acr login --name nqueenacr

# Construir e enviar
docker build -t nqueenacr.azurecr.io/nqueen:latest .
docker push nqueenacr.azurecr.io/nqueen:latest

# Atualizar no Kubernetes
kubectl set image deployment/nqueen-app nqueen=nqueenacr.azurecr.io/nqueen:latest
```

## 🔍 Verificar Status do Deploy

```powershell
# Ver pods
kubectl get pods

# Ver logs
kubectl logs -l app=nqueen

# Port-forward para teste
kubectl port-forward service/nqueen-service 8080:80
```

## 💡 Dicas

1. **Docker Desktop demora para iniciar** - seja paciente
2. **Use WSL2** se disponível para melhor performance
3. **Reinicie o Windows** se nada funcionar
4. **Verifique antivírus** - pode estar bloqueando o Docker