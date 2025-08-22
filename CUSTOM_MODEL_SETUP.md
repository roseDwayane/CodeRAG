# 自定義模型設定指南 - Llama-3.2-1B-Instruct-GGUF

這個指南會幫你設定 Hugging Face 的 `hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF` 模型來與 CodeRAG 一起使用。

## 🚀 快速設定

### 1. 執行自動設定腳本

```bash
python setup_custom_model.py
```

這個腳本會：
- 檢查 Ollama 是否已安裝
- 創建 `Modelfile` 來定義你的模型
- 創建 `.env` 檔案並設定正確的配置
- 使用 Ollama 創建自定義模型
- 測試模型是否正常工作

### 2. 手動設定（如果自動腳本失敗）

#### 步驟 1: 創建 Modelfile

```bash
# 創建 Modelfile 檔案
cat > Modelfile << 'EOF'
FROM hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF

TEMPLATE """{{ if .System }}<|system|>
{{ .System }}<|end|>
{{ end }}{{ if .Prompt }}<|user|>
{{ .Prompt }}<|end|>
{{ end }}<|assistant|>
{{ .Response }}<|end|>"""

PARAMETER stop "<|end|>"
PARAMETER stop "<|user|>"
PARAMETER stop "<|system|>"
EOF
```

#### 步驟 2: 創建模型

```bash
# 創建自定義模型
ollama create llama-3.2-1b-instruct -f Modelfile
```

#### 步驟 3: 設定環境變數

創建 `.env` 檔案：

```bash
# Model Provider Configuration
MODEL_PROVIDER=ollama

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL=llama-3.2-1b-instruct
OLLAMA_EMBEDDING_MODEL=llama-3.2-1b-instruct

# Project Directory Configuration
WATCHED_DIR=.

# FAISS Configuration
FAISS_INDEX_FILE=./coderag_index.faiss
EMBEDDING_DIM=4096
```

## 🔧 模型配置說明

### 模型名稱
- **聊天模型**: `llama-3.2-1b-instruct`
- **嵌入模型**: `llama-3.2-1b-instruct`
- **嵌入維度**: `4096`

### 提示詞模板
這個模型使用特殊的提示詞格式：
```
<|system|>
系統提示詞
<|end|>
<|user|>
用戶問題
<|end|>
<|assistant|>
助手回答
<|end|>
```

## 🧪 測試設定

### 1. 測試 Ollama 連接

```bash
python test_ollama_integration.py
```

### 2. 手動測試模型

```bash
# 測試聊天功能
ollama run llama-3.2-1b-instruct "Hello, how are you?"

# 測試嵌入功能
curl -X POST http://localhost:11434/api/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "llama-3.2-1b-instruct", "prompt": "test"}'
```

## 🚀 執行 CodeRAG

設定完成後，你可以正常執行 CodeRAG：

```bash
# 啟動後端（索引和監控）
python main.py

# 在另一個終端啟動 UI
streamlit run app.py
```

## 🔍 故障排除

### 常見問題

1. **"Model not found" 錯誤**
   ```bash
   # 檢查模型是否存在
   ollama list
   
   # 如果不存在，重新創建
   python setup_custom_model.py
   ```

2. **"Dimension mismatch" 錯誤**
   - 確保 `.env` 中的 `EMBEDDING_DIM=4096`
   - 清除並重建索引：`python main.py`

3. **模型下載失敗**
   - 檢查網路連接
   - 確保 Hugging Face 模型 URL 正確
   - 嘗試手動下載模型

4. **記憶體不足**
   - 這個模型相對較小（1B 參數），但首次載入可能需要一些時間
   - 確保有足夠的 RAM（建議 4GB+）

### 效能優化

1. **使用 GPU 加速**
   ```bash
   # 檢查 Ollama 是否支援 GPU
   ollama run llama-3.2-1b-instruct --gpu
   ```

2. **調整模型參數**
   在 `prompt_flow.py` 中調整：
   ```python
   "options": {
       "temperature": 0.3,
       "num_predict": 2000,  # 減少最大 token 數
       "top_k": 40,
       "top_p": 0.9
   }
   ```

## 📝 注意事項

1. **首次運行**：模型首次載入可能需要幾分鐘
2. **記憶體使用**：這個 1B 模型相對較小，適合開發和測試
3. **模型品質**：1B 模型可能不如更大的模型準確，但速度更快
4. **嵌入維度**：確保使用正確的嵌入維度（4096）

## 🔄 更新模型

如果需要更新模型：

```bash
# 刪除舊模型
ollama rm llama-3.2-1b-instruct

# 重新創建
python setup_custom_model.py
```

## 📞 支援

如果遇到問題：

1. 檢查 Ollama 狀態：`ollama list`
2. 查看模型資訊：`ollama show llama-3.2-1b-instruct`
3. 檢查日誌：`ollama logs`
4. 重新啟動 Ollama：`ollama serve`
