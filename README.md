# Chat with Your Notes
A simple application that allows you to chat with your personal notes using vector search and LLMs.

## Prerequisites
- Docker
- Python 3.8+
- pipo
= LMstudio server running `deepseek-r1-distill-llama-8b`

## Installation


(optional) Initialize venv
```bash
venv venv
source venv/bin/activate
```
1. Install required Python packages:
```bash
pip install -r requirements.txt
```

2. Run Qdrant
```bash
docker run -p 6333:6333 qdrant/qdrant
```

3. Run Loader

### Option 1 one time loader
```bash
python3 loader.py
```

### Option 2, continuous loader

```bash
python continuous_loader.py
```


4. Run Streamlit
```bash
streamlit run query_app.py
```