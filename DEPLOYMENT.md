# Deployment Guide

This guide covers various deployment options for the Banking Customer Support AI Agent.

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Google Colab](#google-colab)
3. [Hugging Face Spaces](#hugging-face-spaces)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Deployment (AWS/Azure/GCP)](#cloud-deployment)

---

## Local Development

See [QUICKSTART.md](QUICKSTART.md) for local setup instructions.

---

## Google Colab

### Steps to Deploy on Colab

1. **Upload Files to Google Drive**
   - Upload the entire `banking_support_agent` folder to Google Drive
   - Or upload the notebook directly

2. **Open in Colab**
   - Go to [colab.research.google.com](https://colab.research.google.com)
   - Upload the notebook from Google Drive

3. **Install Dependencies**
   ```python
   !pip install -q transformers datasets accelerate evaluate gradio langgraph pandas numpy torch
   ```

4. **Mount Google Drive (Optional)**
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

5. **Run All Cells**
   - Execute cells in order
   - The Gradio interface will generate a shareable URL

### Colab-Specific Notes

- GPU acceleration is available (Runtime → Change runtime type → GPU)
- Training time: ~5-10 minutes on GPU
- Gradio share link valid for 72 hours
- Session resets after inactivity

---

## Hugging Face Spaces

### Prerequisites

- Hugging Face account
- Git LFS installed

### Deployment Steps

1. **Create New Space**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose **Gradio** SDK
   - Select **Python** template

2. **Configure Space**
   - Space name: `banking-support-agent`
   - Visibility: Public or Private
   - Hardware: CPU (free tier sufficient)

3. **Upload Files**
   ```bash
   git clone https://huggingface.co/spaces/yourusername/banking-support-agent
   cd banking-support-agent
   
   # Copy project files
   cp /path/to/project/* .
   
   # Add and commit
   git add .
   git commit -m "Initial deployment"
   git push
   ```

4. **Required Files**
   - `requirements.txt` ✅
   - `src/` directory ✅
   - `config.py` ✅
   - `app.py` (create below)

5. **Create app.py for Spaces**
   ```python
   from src.ui import create_ui
   
   # Create Gradio app
   demo = create_ui()
   
   # Launch
   if __name__ == "__main__":
       demo.launch()
   ```

6. **Add Model Files**
   - Upload pre-trained model to `models/` directory
   - Or train on first launch (adds startup time)

### Space Configuration

**README.md** (auto-generated):
```markdown
---
title: Banking Customer Support AI Agent
emoji: 🏦
colorFrom: blue
colorTo: gray
sdk: gradio
sdk_version: 4.0.0
python_version: 3.10
---
```

---

## Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p models data

# Expose Gradio port
EXPOSE 7860

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

# Run application
CMD ["python", "src/ui.py"]
```

### Build and Run

```bash
# Build Docker image
docker build -t banking-support-agent .

# Run container
docker run -p 7860:7860 banking-support-agent

# Access at http://localhost:7860
```

### Docker Compose (Optional)

```yaml
version: '3.8'

services:
  banking-agent:
    build: .
    ports:
      - "7860:7860"
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    environment:
      - GRADIO_SHARE=false
    restart: unless-stopped
```

---

## Cloud Deployment

### AWS Deployment

#### Option 1: EC2 Instance

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04
   - Instance type: t2.medium (minimum)
   - Security group: Allow ports 22 (SSH) and 7860 (HTTP)

2. **Connect and Setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Install Python
   sudo apt update
   sudo apt install python3-pip -y
   
   # Clone repository
   git clone https://github.com/mayank1110/banking_support_agent.git
   cd banking_support_agent
   
   # Setup virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run application
   python src/ui.py
   ```

3. **Access**
   - http://your-ec2-ip:7860

#### Option 2: AWS SageMaker

```python
from sagemaker.huggingface import HuggingFaceModel

# Create model
huggingface_model = HuggingFaceModel(
    model_data="s3://your-bucket/model.tar.gz",
    role="your-sagemaker-role",
    transformers_version="4.35",
    pytorch_version="2.0",
    py_version="py310",
)

# Deploy endpoint
predictor = huggingface_model.deploy(
    initial_instance_count=1,
    instance_type="ml.t2.medium",
)
```

### Azure Deployment

#### Azure App Service

1. **Create Web App**
   ```bash
   az group create --name banking-agent-rg --location eastus
   az appservice plan create --name banking-agent-plan \
     --resource-group banking-agent-rg --sku B1 --is-linux
   az webapp create --resource-group banking-agent-rg \
     --plan banking-agent-plan --name banking-agent-app \
     --runtime "PYTHON:3.10"
   ```

2. **Deploy Code**
   ```bash
   az webapp deployment source config-local-git \
     --resource-group banking-agent-rg --name banking-agent-app
   
   git remote add azure <git-url>
   git push azure main
   ```

3. **Configure Startup**
   ```bash
   az webapp config set \
     --resource-group banking-agent-rg \
     --name banking-agent-app \
     --startup-file "python src/ui.py"
   ```

### Google Cloud Platform

#### Cloud Run

1. **Build Container**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/banking-agent
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy banking-agent \
     --image gcr.io/PROJECT_ID/banking-agent \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 7860
   ```

---

## Production Considerations

### Database Migration

Replace CSV with proper database:

```python
# PostgreSQL example
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:pass@localhost/banking_support")
df.to_sql("tickets", engine, if_exists="replace")
```

### Load Balancing

For high traffic:
- Use Nginx reverse proxy
- Deploy multiple instances
- Implement session affinity

### Monitoring

```python
# Add logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Security

1. **API Authentication**
   ```python
   # Add API key protection
   GRADIO_APP_PASSWORD="your-password"
   ```

2. **Rate Limiting**
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   ```

3. **HTTPS**
   - Use Let's Encrypt for SSL certificates
   - Configure reverse proxy (Nginx/Apache)

---

## Performance Optimization

### Model Optimization

```python
# Use quantization
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,  # Mixed precision
    device_map="auto",  # Automatic device placement
)
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_classification(text: str) -> str:
    return hf_model_classify(text)
```

---

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   lsof -i :7860
   kill -9 <PID>
   ```

2. **Out of Memory**
   - Reduce batch size in `config.py`
   - Use smaller model (e.g., TinyBERT)

3. **Slow Inference**
   - Enable GPU acceleration
   - Use model quantization
   - Implement caching

---

## Support

For deployment issues:
- Check cloud provider documentation
- Review application logs
- Create GitHub issue with error details
