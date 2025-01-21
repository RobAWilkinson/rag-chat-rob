# Chat with Your Notes
A simple application that allows you to chat with your personal notes using vector search and LLMs.

## Prerequisites
- Docker
- Python 3.8+
- pip

## Installation

1. Install required Python packages:
```bash
pip install -r requirements.txt
```

2. Run Qdrant
```bash
docker run -p 6333:6333 qdrant/qdrant
```

3. Run Loader
```bash
python 3 loader.py
```

4. Run Streamlit
```bash
streamlit query_app.py
```

