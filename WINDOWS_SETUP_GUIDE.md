# Windows 設定指南 - Llama-3.2-1B-Instruct-GGUF

這個指南專門針對 Windows 系統，避免編碼問題。

## 🚀 快速設定

### 方法 1: 使用 Windows 相容腳本

```bash
python setup_custom_model_windows.py
```

### 方法 2: 手動設定（如果腳本失敗）

#### 步驟 1: 確保 Ollama 已安裝並在 PATH 中

1. 下載並安裝 Ollama: https://ollama.ai/
2. 重新啟動終端機
3. 測試安裝：
   ```bash
   ollama --version
   ```

#### 步驟 2: 創建 Modelfile

在專案根目錄創建 `Modelfile` 檔案：

```bash
# 使用 PowerShell 或 CMD
echo "FROM hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF" > Modelfile
echo "" >> Modelfile
echo "TEMPLATE \"\"\"{{ if .System }}<|system|>" >> Modelfile
echo "{{ .System }}<|end|>" >> Modelfile
echo "{{ end }}{{ if .Prompt }}<|user|>" >> Modelfile
echo "{{ .Prompt }}<|end|>" >> Modelfile
echo "{{ end }}<|assistant|>" >> Modelfile
echo "{{ .Response }}<|end|>\"\"\"" >> Modelfile
echo "" >> Modelfile
echo "PARAMETER stop \"<|end|>\"" >> Modelfile
echo "PARAMETER stop \"<|user|>\"" >> Modelfile
echo "PARAMETER stop \"<|system|>\"" >> Modelfile
```

#### 步驟 3: 創建 .env 檔案

在專案根目錄創建 `.env` 檔案：

```bash
# 使用 PowerShell 或 CMD
echo "MODEL_PROVIDER=ollama" > .env
echo "OLLAMA_BASE_URL=http://localhost:11434" >> .env
echo "OLLAMA_CHAT_MODEL=llama-3.2-1b-instruct" >> .env
echo "OLLAMA_EMBEDDING_MODEL=llama-3.2-1b-instruct" >> .env
echo "WATCHED_DIR=." >> .env
echo "FAISS_INDEX_FILE=./coderag_index.faiss" >> .env
echo "EMBEDDING_DIM=4096" >> .env
```

#### 步驟 4: 創建模型

```bash
ollama create llama-3.2-1b-instruct -f Modelfile
```

#### 步驟 5: 測試模型

```bash
# 測試聊天功能
ollama run llama-3.2-1b-instruct "Hello"

# 測試嵌入功能（使用 PowerShell）
Invoke-RestMethod -Uri "http://localhost:11434/api/embeddings" -Method POST -ContentType "application/json" -Body '{"model": "llama-3.2-1b-instruct", "prompt": "test"}'
```

## 🔧 故障排除

### 常見 Windows 問題

1. **編碼錯誤 (cp950)**
   - 使用 `setup_custom_model_windows.py` 腳本
   - 或手動設定（見方法 2）

2. **Ollama 不在 PATH 中**
   ```bash
   # 檢查 Ollama 是否在 PATH 中
   where ollama
   
   # 如果沒有，手動添加到 PATH 或重新安裝
   ```

3. **權限問題**
   - 以管理員身份運行終端機
   - 確保有寫入專案目錄的權限

4. **防火牆問題**
   - 確保 Ollama 可以訪問網路
   - 檢查 Windows Defender 設定

### 檢查設定

```bash
# 檢查 Ollama 狀態
ollama list

# 檢查模型是否存在
ollama show llama-3.2-1b-instruct

# 檢查 Ollama 服務
ollama serve
```

## 🚀 執行 CodeRAG

設定完成後：

```bash
# 啟動後端
python main.py

# 在另一個終端啟動 UI
streamlit run app.py
```

## 📝 注意事項

1. **終端機編碼**：Windows 預設使用 cp950 編碼，可能與 UTF-8 衝突
2. **路徑分隔符**：Windows 使用反斜線 `\`，但建議使用正斜線 `/`
3. **權限**：某些操作可能需要管理員權限
4. **防火牆**：確保 Ollama 可以訪問網路下載模型

## 🔄 重新設定

如果需要重新設定：

```bash
# 刪除舊模型
ollama rm llama-3.2-1b-instruct

# 重新創建
python setup_custom_model_windows.py
```

## 📞 支援

如果仍然遇到問題：

1. 檢查 Ollama 日誌：`ollama logs`
2. 重新啟動 Ollama：`ollama serve`
3. 檢查網路連接
4. 嘗試使用不同的終端機（PowerShell vs CMD）
