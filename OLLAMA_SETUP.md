# Ollama Integration Guide for CodeRAG

This guide explains how to set up and use CodeRAG with Ollama instead of OpenAI.

## Prerequisites

1. **Install Ollama**: Download and install from [ollama.ai](https://ollama.ai/)
2. **Pull a Model**: You'll need both a chat model and an embedding model

## Quick Setup

### 1. Install Ollama Dependencies

```bash
pip install ollama==0.1.7
```

### 2. Configure Environment

Create or update your `.env` file:

```bash
# Model Provider
MODEL_PROVIDER=ollama

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL=llama2
OLLAMA_EMBEDDING_MODEL=llama2

# Project Configuration
WATCHED_DIR=/path/to/your/codebase
FAISS_INDEX_FILE=/path/to/faiss_index.bin
EMBEDDING_DIM=4096  # Adjust based on your model
```

### 3. Start Ollama and Pull Models

```bash
# Start Ollama server
ollama serve

# In another terminal, pull the models you need
ollama pull llama2
```

### 4. Test the Integration

```bash
python test_ollama_integration.py
```

### 5. Run CodeRAG

```bash
# Start the backend
python main.py

# In another terminal, start the UI
streamlit run app.py
```

## Model Compatibility

### Recommended Models

| Model | Chat | Embeddings | Dimension | Notes |
|-------|------|------------|-----------|-------|
| llama2 | ✅ | ✅ | 4096 | Good balance of performance and size |
| llama2:7b | ✅ | ✅ | 4096 | Smaller, faster version |
| llama2:13b | ✅ | ✅ | 4096 | Larger, more capable version |
| codellama | ✅ | ✅ | 4096 | Specialized for code |
| mistral | ✅ | ✅ | 4096 | Good performance, smaller size |

### Checking Model Dimensions

To find the embedding dimension of your model:

```bash
# Test with a simple prompt
curl -X POST http://localhost:11434/api/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "llama2", "prompt": "test"}'
```

The response will contain an embedding array. Count the elements to get the dimension.

## Troubleshooting

### Common Issues

1. **"Connection refused" error**
   - Make sure Ollama is running: `ollama serve`
   - Check the URL in your `.env` file

2. **"Model not found" error**
   - Pull the model: `ollama pull llama2`
   - Check model name spelling in `.env`

3. **"Dimension mismatch" error**
   - Update `EMBEDDING_DIM` in your `.env` file
   - Clear and rebuild the index: `python main.py`

4. **Slow performance**
   - Use a smaller model (e.g., `llama2:7b`)
   - Consider using a GPU-enabled Ollama build
   - Reduce the number of search results in `prompt_flow.py`

### Performance Tips

1. **Use appropriate model sizes**:
   - For development: `llama2:7b`
   - For production: `llama2:13b` or `codellama`

2. **Optimize embedding dimensions**:
   - Set `EMBEDDING_DIM` correctly for your model
   - Rebuild index when changing models

3. **Monitor resource usage**:
   - Ollama models can be memory-intensive
   - Consider using quantized models for better performance

## Advanced Configuration

### Custom Model Parameters

You can customize model parameters in `prompt_flow.py`:

```python
# In _generate_ollama_response function
payload = {
    "model": OLLAMA_CHAT_MODEL,
    "prompt": f"{SYSTEM_PROMPT}\n\n{full_prompt}",
    "stream": False,
    "options": {
        "temperature": 0.3,      # Adjust creativity
        "num_predict": 4000,     # Max tokens
        "top_k": 40,            # Top-k sampling
        "top_p": 0.9,           # Nucleus sampling
        "repeat_penalty": 1.1    # Reduce repetition
    }
}
```

### Using Different Models for Chat and Embeddings

You can use different models for different tasks:

```bash
# .env file
OLLAMA_CHAT_MODEL=codellama
OLLAMA_EMBEDDING_MODEL=llama2
```

This is useful when you want a code-specialized model for chat but a general model for embeddings.

## Migration from OpenAI

If you're switching from OpenAI to Ollama:

1. **Update your `.env` file**:
   ```bash
   MODEL_PROVIDER=ollama
   # Remove or comment out OpenAI settings
   # OPENAI_API_KEY=...
   ```

2. **Clear and rebuild the index**:
   ```bash
   python main.py
   ```

3. **Test the integration**:
   ```bash
   python test_ollama_integration.py
   ```

## Support

If you encounter issues:

1. Check the test script output: `python test_ollama_integration.py`
2. Verify Ollama is running: `ollama list`
3. Check model availability: `ollama show llama2`
4. Review the logs in your terminal

For more help, refer to the [Ollama documentation](https://github.com/ollama/ollama).
