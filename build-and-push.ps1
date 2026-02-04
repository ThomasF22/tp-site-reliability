# Build and Push Docker Images to Docker Hub
# Usage: .\build-and-push.ps1

Write-Host "🐳 Building and pushing images to Docker Hub (thomasf22)..." -ForegroundColor Green

# Login to Docker Hub (you'll be prompted for password)
Write-Host "📝 Logging into Docker Hub..." -ForegroundColor Yellow
docker login

# Stop any running containers
Write-Host "🛑 Stopping existing containers..." -ForegroundColor Yellow
docker-compose down

# Build all images
Write-Host "🔨 Building all images..." -ForegroundColor Yellow

# Build database image
Write-Host "📦 Building database image..." -ForegroundColor Cyan
docker build -t thomasf22/forum-database:latest ./db

# Build backend image
Write-Host "📦 Building backend image..." -ForegroundColor Cyan
docker build -t thomasf22/forum-backend:latest ./backend

# Build frontend image
Write-Host "📦 Building frontend image..." -ForegroundColor Cyan
docker build -t thomasf22/forum-frontend:latest ./frontend

# Push images to Docker Hub
Write-Host "🚀 Pushing images to Docker Hub..." -ForegroundColor Green

Write-Host "⬆️  Pushing database image..." -ForegroundColor Cyan
docker push thomasf22/forum-database:latest

Write-Host "⬆️  Pushing backend image..." -ForegroundColor Cyan
docker push thomasf22/forum-backend:latest

Write-Host "⬆️  Pushing frontend image..." -ForegroundColor Cyan
docker push thomasf22/forum-frontend:latest

Write-Host "✅ All images successfully pushed to Docker Hub!" -ForegroundColor Green
Write-Host "📋 Images available at:" -ForegroundColor Yellow
Write-Host "   - https://hub.docker.com/r/thomasf22/forum-database" -ForegroundColor White
Write-Host "   - https://hub.docker.com/r/thomasf22/forum-backend" -ForegroundColor White
Write-Host "   - https://hub.docker.com/r/thomasf22/forum-frontend" -ForegroundColor White

Write-Host "🚀 You can now run: docker-compose up -d" -ForegroundColor Green