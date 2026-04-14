# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/banking_support_agent.git
cd banking_support_agent
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare Training Data

Place your training dataset in the `data/` directory:
- File: `data/banking_support_dataset_train_model.csv`
- Columns: `text`, `label`
- Labels: `Query`, `Positive Feedback`, `Negative Feedback`

### 5. Run the Application

#### Option A: Jupyter Notebook (Recommended for Development)

```bash
jupyter notebook Capstone_1_Banking_Customer_Support.ipynb
```

Follow the notebook cells in order:
1. Install dependencies
2. Import libraries
3. Load and validate dataset
4. Train the model
5. Test classification
6. Set up ticket system
7. Initialize LangGraph agents
8. Build workflow graph
9. Launch Gradio UI

#### Option B: Python Script (Production)

```bash
# Launch the Gradio web interface
python src/ui.py
```

Or use the installed command:
```bash
pip install -e .
banking-agent
```

## First-Time Setup

### Train the Model

If running the notebook, the model will train automatically. For script-based usage:

```python
from src.classifier import IntentClassifier

classifier = IntentClassifier()
train_ds, eval_ds = classifier.load_dataset()
classifier.train(train_ds, eval_ds)
```

### Verify Installation

Run the test suite:
```bash
python -m pytest tests/ -v
```

## Access the Application

Once the Gradio interface launches:
- **Local URL**: http://127.0.0.1:7860
- **Public URL**: If `share=True`, a public URL will be generated (valid for 72 hours)

## Example Usage

### 1. Positive Feedback
```
Name: John
Message: Thanks, that was very helpful!
Expected: Positive feedback response with thanks
```

### 2. Negative Feedback
```
Name: Jane
Message: My card was declined and I'm frustrated
Expected: Apology + ticket creation with ID
```

### 3. Ticket Status Query
```
Name: Bob
Message: What is the status of 123456
Expected: Current ticket status
```

### 4. General Banking Query
```
Name: Alice
Message: How do I activate my debit card
Expected: Guidance and request for more details
```

## Troubleshooting

### Issue: Module not found
```bash
pip install -e .
```

### Issue: Model not found
Run the training cells in the notebook or train programmatically (see above)

### Issue: Port already in use
```bash
# Launch on different port
python src/ui.py --server-port 7861
```

### Issue: CSV file not found
The application creates the CSV automatically. If issues persist:
```python
from src.ticket_manager import _ensure_csv_exists
_ensure_csv_exists()
```

## Next Steps

1. **Customize**: Edit `config.py` for model parameters
2. **Extend**: Add new intent categories or tools
3. **Deploy**: Follow `DEPLOYMENT.md` for production deployment
4. **Test**: Run `pytest tests/ -v` to verify functionality

## Support

For issues or questions:
- Check existing GitHub issues
- Create a new issue with details
- Review the main README.md for comprehensive documentation
