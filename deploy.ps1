# Deploy script para N-Queen no AKS
# Execute: .\deploy.ps1 -ResourceGroup "your-rg" -AksCluster "your-aks" -AcrName "your-acr"

param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroup,
    
    [Parameter(Mandatory=$true)]
    [string]$AksCluster,
    
    [Parameter(Mandatory=$true)]
    [string]$AcrName,
    
    [string]$ImageTag = "latest"
)

Write-Host "🚀 Iniciando deploy da aplicação N-Queen no AKS..." -ForegroundColor Green

# Verificar se está logado no Azure
Write-Host "📋 Verificando login do Azure..." -ForegroundColor Yellow
$account = az account show 2>$null | ConvertFrom-Json
if (-not $account) {
    Write-Host "❌ Não logado no Azure. Execute 'az login' primeiro." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Logado como: $($account.user.name)" -ForegroundColor Green

# Conectar ao cluster AKS
Write-Host "🔗 Conectando ao cluster AKS..." -ForegroundColor Yellow
az aks get-credentials --resource-group $ResourceGroup --name $AksCluster --overwrite-existing
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao conectar ao cluster AKS" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Conectado ao cluster AKS" -ForegroundColor Green

# Login no ACR
Write-Host "🔐 Fazendo login no ACR..." -ForegroundColor Yellow
az acr login --name $AcrName
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao fazer login no ACR" -ForegroundColor Red
    exit 1
}

# Construir e enviar imagem
Write-Host "🏗️ Construindo imagem Docker..." -ForegroundColor Yellow
$imageName = "$AcrName.azurecr.io/nqueen:$ImageTag"
docker build -t $imageName .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao construir imagem" -ForegroundColor Red
    exit 1
}

Write-Host "📤 Enviando imagem para ACR..." -ForegroundColor Yellow
docker push $imageName
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao enviar imagem" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Imagem enviada: $imageName" -ForegroundColor Green

# Conectar AKS ao ACR
Write-Host "🔗 Conectando AKS ao ACR..." -ForegroundColor Yellow
az aks update -n $AksCluster -g $ResourceGroup --attach-acr $AcrName
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Aviso: Pode já estar conectado ao ACR" -ForegroundColor Orange
}

# Atualizar manifesto com a imagem correta
Write-Host "📝 Atualizando manifesto com nova imagem..." -ForegroundColor Yellow
$manifestPath = "k8s\nqueen-app.yaml"
$manifestContent = Get-Content $manifestPath -Raw
$manifestContent = $manifestContent -replace "image: nqueen:latest", "image: $imageName"
$manifestContent | Set-Content $manifestPath
Write-Host "✅ Manifesto atualizado" -ForegroundColor Green

# Deploy PostgreSQL
Write-Host "🗄️ Fazendo deploy do PostgreSQL..." -ForegroundColor Yellow
kubectl apply -f k8s\postgres-config.yaml
kubectl apply -f k8s\postgres.yaml

Write-Host "⏳ Aguardando PostgreSQL ficar pronto..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=postgres --timeout=300s
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ PostgreSQL não ficou pronto no tempo esperado" -ForegroundColor Red
    exit 1
}
Write-Host "✅ PostgreSQL está pronto" -ForegroundColor Green

# Deploy da aplicação
Write-Host "🚀 Fazendo deploy da aplicação N-Queen..." -ForegroundColor Yellow
kubectl apply -f k8s\nqueen-config.yaml
kubectl apply -f k8s\nqueen-app.yaml

Write-Host "⏳ Aguardando aplicação ficar pronta..." -ForegroundColor Yellow
Start-Sleep 30
kubectl wait --for=condition=ready pod -l app=nqueen --timeout=300s
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Aplicação pode ainda estar inicializando..." -ForegroundColor Orange
}

# Deploy do Ingress (opcional)
Write-Host "🌐 Fazendo deploy do Ingress..." -ForegroundColor Yellow
kubectl apply -f k8s\ingress.yaml

# Mostrar status
Write-Host "`n📊 Status do deploy:" -ForegroundColor Cyan
Write-Host "Pods:" -ForegroundColor White
kubectl get pods

Write-Host "`nServices:" -ForegroundColor White
kubectl get services

Write-Host "`nIngress:" -ForegroundColor White
kubectl get ingress

Write-Host "`n✅ Deploy concluído!" -ForegroundColor Green
Write-Host "🔗 Para acessar localmente, execute:" -ForegroundColor Cyan
Write-Host "kubectl port-forward service/nqueen-service 8080:80" -ForegroundColor White
Write-Host "Em seguida acesse: http://localhost:8080" -ForegroundColor White