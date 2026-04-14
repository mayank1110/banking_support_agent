# 🏦 Banking Customer Support AI Agent

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agentic AI](https://img.shields.io/badge/Agentic%20AI-LangGraph-green)](https://langchain-ai.github.io/langgraph/)

An intelligent AI-powered customer support agent for banking institutions, built with **LangGraph**, **Hugging Face Transformers**, and **Gradio**. This project demonstrates Agentic AI capabilities including intent classification, automated ticket management, and interactive conversational workflows.

## 🌟 Features

- **Multi-Intent Classification**: Fine-tuned DistilBERT model for classifying customer messages into:
  - ✅ Positive Feedback
  - ❌ Negative Feedback  
  - ❓ General Queries

- **Agentic Workflow**: LangGraph-based state machine for intelligent routing and response generation
- **Automated Ticket System**: Automatic ticket generation for negative feedback with unique IDs
- **Ticket Status Tracking**: Query ticket status using 6-digit ticket IDs
- **Satisfaction Rating**: 1-5 star rating system for resolved tickets
- **Interactive UI**: Gradio-based web interface with real-time interaction
- **Persistent Storage**: CSV-based ticket storage for easy deployment

## 🏗️ Project Structure

```
banking_support_agent/
├── Banking_Customer_Support.ipynb    # Jupyter notebook with complete implementation
├── src/
│   ├── __init__.py
│   ├── classifier.py                             # Intent classification model
│   ├── agents.py                                 # LangGraph agent workflows
│   ├── handlers.py                               # Feedback and query handlers
│   ├── ticket_manager.py                         # Ticket CRUD operations
│   └── ui.py                                     # Gradio UI components
├── data/
│   ├── banking_support_dataset_train_model.csv   # Training dataset
│   └── support_tickets.csv                       # Runtime ticket storage
├── models/
│   └── .gitkeep                                  # Saved model directory
├── tests/
│   ├── __init__.py
│   └── test_agent.py                             # Unit tests
├── config.py                                     # Configuration settings
├── requirements.txt                              # Python dependencies
├── setup.py                                      # Package installation
├── .gitignore                                    # Git ignore rules
├── LICENSE                                       # MIT License
└── README.md                                     # This file
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/mayank1110/banking_support_agent.git
cd banking_support_agent
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

#### Option A: Jupyter Notebook (Recommended for Exploration)
```bash
jupyter notebook Banking_Customer_Support.ipynb
```

#### Option B: Python Script (Production)
```bash
python src/ui.py
```

## 🎯 Usage Examples

### Intent Classification
```python
from src.classifier import hf_model_classify

print(hf_model_classify("Thanks, that was helpful"))
# Output: Positive Feedback

print(hf_model_classify("My card was declined and I need help"))
# Output: Negative Feedback

print(hf_model_classify("What is the status of 123456"))
# Output: Query
```

### Agent Interaction
```python
from src.agents import app

state = {"input": "How do I activate my debit card", "customer_name": "John"}
result = app.invoke(state)
print(result["answer"]["response"])
```

### Ticket Management
```python
from src.ticket_manager import generate_unique_ticket_id, view_tickets

# Create new ticket
ticket_id = generate_unique_ticket_id()

# View all tickets
print(view_tickets())
```

## 🧠 Technical Architecture

### Model Architecture
- **Base Model**: DistilBERT-base-uncased
- **Training**: 3 epochs, batch size 16, learning rate 2e-5
- **Labels**: Query, Positive Feedback, Negative Feedback
- **Accuracy**: Evaluated on 10% test split

### Agentic Workflow (LangGraph)
```
User Input → Reason Node → Tool Executor → Finalize → Response
                ↓
         Intent Classification
         ↓              ↓
    Feedback Tool   Query Tool
         ↓              ↓
    Handle         Check Ticket
    Feedback       Status
```

## 📊 Dataset

The model is trained on a custom banking support dataset with the following structure:

| Column | Type | Description |
|--------|------|-------------|
| text | string | Customer message/query |
| label | string | Intent category (Query/Positive Feedback/Negative Feedback) |

**Dataset Requirements**:
- Minimum 1000 samples recommended for production
- Balanced class distribution
- Real-world banking scenarios

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or run individual test file:
```bash
python tests/test_agent.py
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Model settings
MODEL_NAME = "distilbert-base-uncased"
OUTPUT_DIR = "./models/intent-distilbert"
NUM_LABELS = 3
BATCH_SIZE = 16
EPOCHS = 3
LEARNING_RATE = 2e-5

# Ticket settings
CSV_FILE = "./data/support_tickets.csv"
TICKET_ID_LENGTH = 6
```

## 📦 Installation from Source

For development:

```bash
pip install -e .
```

This installs the package in editable mode with all dependencies.

## 🌐 Deployment Options

### Local Deployment
```bash
python src/ui.py
```

### Google Colab
Upload the notebook to Google Colab and run all cells. The Gradio interface will generate a shareable URL.

### Hugging Face Spaces
Deploy to Hugging Face Spaces for free hosting:
1. Create new Space with Gradio template
2. Upload repository files
3. Add requirements.txt
4. Configure environment variables

### Docker (Future Enhancement)
```bash
docker build -t banking-agent .
docker run -p 7860:7860 banking-agent
```

## 🔐 Security Considerations

- **Data Privacy**: Customer names and messages stored locally
- **Ticket IDs**: Randomly generated 6-digit integers
- **No External APIs**: All processing happens locally
- **CSV Storage**: Suitable for development; use database for production

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| Model Size | ~268MB (DistilBERT) |
| Inference Time | <100ms per query |
| Training Time | ~5-10 minutes (3 epochs) |
| Accuracy | >90% (on test set) |

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Gradio](https://gradio.app/)
- [DistilBERT](https://huggingface.co/distilbert-base-uncased)

## 📧 Contact

For questions or support, please open an issue on GitHub or contact at mayank.jha10@gmail.com.

---

**Built with ❤️ for showcasing Agentic AI skills**
