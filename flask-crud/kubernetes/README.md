# Kubernetes Manifests - Flask CRUD

Este diretório contém os manifestos do Kubernetes para deployar a aplicação Flask CRUD.

## Estrutura dos Arquivos

- **deployment.yaml** - Define o Deployment com 3 réplicas da aplicação
- **service.yaml** - Expõe o Deployment internamente no cluster (ClusterIP)
- **ingress.yaml** - Configura o acesso externo via Ingress
- **kustomization.yaml** - Agrupa todos os recursos para deploy via Kustomize

## Pré-requisitos

1. Cluster Kubernetes funcionando (minikube, kind, EKS, GKE, AKS, etc.)
2. kubectl configurado
3. Ingress Controller instalado (ex: nginx-ingress)
4. Imagem Docker `flask-crud:latest` disponível no cluster

## Build e Push da Imagem

```bash
# Build da imagem
docker build -t flask-crud:latest .

# Para usar em cluster local (minikube)
eval $(minikube docker-env)
docker build -t flask-crud:latest .

# Para usar em cluster remoto, faça push para um registry
docker tag flask-crud:latest seu-registry/flask-crud:latest
docker push seu-registry/flask-crud:latest
```

## Deploy

### Opção 1: Deploy com kubectl

```bash
# Deploy de todos os recursos
kubectl apply -f kubernetes/

# Verificar o status
kubectl get deployments
kubectl get services
kubectl get ingress
kubectl get pods
```

### Opção 2: Deploy com Kustomize

```bash
# Deploy usando kustomize
kubectl apply -k kubernetes/

# Verificar o status
kubectl get all -l app=flask-crud
```

## Configurações Importantes

### 1. Ingress Hostname

Edite o arquivo `ingress.yaml` e altere o hostname:

```yaml
rules:
- host: flask-crud.local  # Altere para seu domínio
```

Para testar localmente, adicione ao `/etc/hosts`:

```bash
# Obter IP do Ingress
kubectl get ingress flask-crud-ingress

# Adicionar ao /etc/hosts (substitua pelo IP real)
127.0.0.1 flask-crud.local
```

### 2. Ingress Controller

O manifesto está configurado para usar o nginx-ingress. Para outros controllers, ajuste:

```yaml
ingressClassName: nginx  # Altere conforme necessário
```

### 3. HTTPS/TLS

Para habilitar HTTPS, descomente a seção `tls` no `ingress.yaml` e configure um certificado:

```yaml
tls:
- hosts:
  - flask-crud.local
  secretName: flask-crud-tls
```

### 4. Recursos e Réplicas

Ajuste conforme necessário em `deployment.yaml`:

```yaml
replicas: 3  # Número de pods

resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

## Acesso à Aplicação

Após o deploy:

```bash
# Verificar URL do Ingress
kubectl get ingress flask-crud-ingress

# Acessar via browser
http://flask-crud.local  # ou seu domínio configurado
```

## Comandos Úteis

```bash
# Ver logs dos pods
kubectl logs -l app=flask-crud -f

# Ver detalhes do deployment
kubectl describe deployment flask-crud

# Escalar réplicas
kubectl scale deployment flask-crud --replicas=5

# Port-forward para teste local (sem Ingress)
kubectl port-forward service/flask-crud-service 8080:80
# Acessar em http://localhost:8080

# Deletar todos os recursos
kubectl delete -f kubernetes/
# ou
kubectl delete -k kubernetes/
```

## Troubleshooting

### Pods não estão rodando

```bash
kubectl get pods -l app=flask-crud
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Ingress não está funcionando

```bash
# Verificar se o Ingress Controller está instalado
kubectl get pods -n ingress-nginx

# Instalar nginx-ingress (exemplo para minikube)
minikube addons enable ingress

# Ver eventos do Ingress
kubectl describe ingress flask-crud-ingress
```

### Imagem não encontrada

```bash
# Se estiver usando minikube, certifique-se de:
eval $(minikube docker-env)
docker build -t flask-crud:latest .

# Ou ajuste imagePullPolicy para Never em deployment.yaml
imagePullPolicy: Never
```

## Notas

- A aplicação usa SQLite em memória, então os dados são perdidos quando o pod reinicia
- Para persistência de dados, considere usar um banco de dados externo (PostgreSQL, MySQL)
- Para ambientes de produção, remova `debug=True` do app.py
- Configure variáveis de ambiente sensíveis usando Secrets do Kubernetes
