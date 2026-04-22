# Deploy script alternativo - sem construção local do Docker
# Execute: .\deploy-kubectl-only.ps1 -ResourceGroup "your-rg" -AksCluster "your-aks" -AcrName "your-acr"

param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroup,
    
    [Parameter(Mandatory=$true)]
    [string]$AksCluster,
    
    [Parameter(Mandatory=$true)]
    [string]$AcrName,
    
    [string]$ImageTag = "latest",
    
    [string]$ExistingImage = ""
)

Write-Host "🚀 Deploy da aplicação N-Queen no AKS (sem Docker local)..." -ForegroundColor Green

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

# Definir imagem a usar
if ($ExistingImage) {
    $imageName = $ExistingImage
    Write-Host "🎯 Usando imagem existente: $imageName" -ForegroundColor Cyan
} else {
    $imageName = "$AcrName.azurecr.io/nqueen:$ImageTag"
    Write-Host "⚠️ Usando imagem presumida: $imageName" -ForegroundColor Orange
    Write-Host "   Certifique-se de que esta imagem existe no ACR" -ForegroundColor Orange
    
    # Verificar se a imagem existe no ACR
    Write-Host "🔍 Verificando se a imagem existe no ACR..." -ForegroundColor Yellow
    $repoList = az acr repository list --name $AcrName --output tsv 2>$null
    if ($repoList -and ($repoList -contains "nqueen")) {
        Write-Host "✅ Repositório 'nqueen' encontrado no ACR" -ForegroundColor Green
    } else {
        Write-Host "❌ Repositório 'nqueen' não encontrado no ACR" -ForegroundColor Red
        Write-Host "💡 Opções:" -ForegroundColor Cyan
        Write-Host "   1. Construa e envie a imagem manualmente:" -ForegroundColor White
        Write-Host "      docker build -t $imageName ." -ForegroundColor Gray
        Write-Host "      docker push $imageName" -ForegroundColor Gray
        Write-Host "   2. Use uma imagem de teste temporária" -ForegroundColor White
        
        $response = Read-Host "Deseja continuar com imagem nginx para teste? (y/n)"
        if ($response -eq "y" -or $response -eq "Y") {
            $imageName = "nginx:latest"
            Write-Host "🧪 Usando nginx para teste. Lembre-se de atualizar depois!" -ForegroundColor Orange
        } else {
            Write-Host "❌ Deploy cancelado" -ForegroundColor Red
            exit 1
        }
    }
}

# Conectar AKS ao ACR
Write-Host "🔗 Conectando AKS ao ACR..." -ForegroundColor Yellow
az aks update -n $AksCluster -g $ResourceGroup --attach-acr $AcrName
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Aviso: Pode já estar conectado ao ACR" -ForegroundColor Orange
}

# Atualizar manifesto com a imagem correta
Write-Host "📝 Atualizando manifesto com nova imagem..." -ForegroundColor Yellow
$manifestPath = "k8s\nqueen-app.yaml"
$manifestBackup = "k8s\nqueen-app.yaml.bak"

# Fazer backup do manifesto original
Copy-Item $manifestPath $manifestBackup -Force

$manifestContent = Get-Content $manifestPath -Raw
$manifestContent = $manifestContent -replace "image: .+", "image: $imageName"
$manifestContent | Set-Content $manifestPath
Write-Host "✅ Manifesto atualizado (backup em .bak)" -ForegroundColor Green

try {
    # Deploy PostgreSQL
    Write-Host "🗄️ Fazendo deploy do PostgreSQL..." -ForegroundColor Yellow
    kubectl apply -f k8s\postgres-config.yaml
    kubectl apply -f k8s\postgres.yaml

    Write-Host "⏳ Aguardando PostgreSQL ficar pronto..." -ForegroundColor Yellow
    kubectl wait --for=condition=ready pod -l app=postgres --timeout=300s
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ PostgreSQL não ficou pronto no tempo esperado" -ForegroundColor Red
        throw "PostgreSQL timeout"
    }
    Write-Host "✅ PostgreSQL está pronto" -ForegroundColor Green

    # Deploy da aplicação
    Write-Host "🚀 Fazendo deploy da aplicação N-Queen..." -ForegroundColor Yellow
    kubectl apply -f k8s\nqueen-config.yaml
    kubectl apply -f k8s\nqueen-app.yaml

    Write-Host "⏳ Aguardando aplicação ficar pronta..." -ForegroundColor Yellow
    Start-Sleep 30
    
    # Verificar se os pods estão sendo criados
    $pods = kubectl get pods -l app=nqueen --no-headers 2>$null
    if ($pods) {
        Write-Host "📦 Pods da aplicação encontrados:" -ForegroundColor Cyan
        kubectl get pods -l app=nqueen
    } else {
        Write-Host "⚠️ Nenhum pod da aplicação encontrado ainda" -ForegroundColor Orange
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
    
    if ($imageName -eq "nginx:latest") {
        Write-Host "⚠️ IMPORTANTE: Você está usando nginx para teste!" -ForegroundColor Red
        Write-Host "📝 Para usar sua aplicação real:" -ForegroundColor Cyan
        Write-Host "   1. Construa e envie a imagem para o ACR" -ForegroundColor White
        Write-Host "   2. Execute: kubectl set image deployment/nqueen-app nqueen=$AcrName.azurecr.io/nqueen:latest" -ForegroundColor White
    }
    
    Write-Host "🔗 Para acessar localmente, execute:" -ForegroundColor Cyan
    Write-Host "kubectl port-forward service/nqueen-service 8080:80" -ForegroundColor White
    Write-Host "Em seguida acesse: http://localhost:8080" -ForegroundColor White

} finally {
    # Restaurar manifesto original
    Write-Host "🔄 Restaurando manifesto original..." -ForegroundColor Yellow
    Move-Item $manifestBackup $manifestPath -Force
}