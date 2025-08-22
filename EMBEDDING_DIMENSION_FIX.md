# 修復嵌入維度不匹配問題

## 🚨 問題描述

錯誤訊息：
```
Embedding dimension 2048 does not match FAISS index dimension 4096
```

這表示你的 Ollama 模型產生 2048 維的嵌入，但 FAISS 索引期望 4096 維。

## 🔍 問題原因

1. **模型維度不匹配**：不同的 Ollama 模型有不同的嵌入維度
2. **配置錯誤**：`.env` 檔案中的 `EMBEDDING_DIM` 設定不正確
3. **索引過時**：FAISS 索引是用舊的維度創建的

## 🛠️ 解決方案

### 方法 1: 自動修復（推薦）

```bash
python fix_embedding_dimension.py
```

這個腳本會：
- 檢測所有可用模型的嵌入維度
- 自動選擇正確的維度
- 更新 `.env` 檔案
- 清除舊的 FAISS 索引

### 方法 2: 手動修復

#### 步驟 1: 檢測模型維度

```bash
# 測試當前模型的嵌入維度
curl -X POST http://localhost:11434/api/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "llama-3.2-1b-instruct", "prompt": "test"}'
```

#### 步驟 2: 更新 .env 檔案

根據檢測結果，更新 `.env` 檔案中的 `EMBEDDING_DIM`：

```bash
# 如果模型產生 2048 維嵌入
EMBEDDING_DIM=2048

# 如果模型產生 4096 維嵌入
EMBEDDING_DIM=4096
```

#### 步驟 3: 清除 FAISS 索引

```bash
# 刪除舊的索引檔案
rm coderag_index.faiss metadata.npy
```

#### 步驟 4: 重新建立索引

```bash
python main.py
```

## 📊 常見模型維度

| 模型 | 嵌入維度 | 說明 |
|------|----------|------|
| llama2 | 4096 | 標準 Llama2 模型 |
| llama2:7b | 4096 | 7B 參數版本 |
| llama2:13b | 4096 | 13B 參數版本 |
| llama-3.2-1b-instruct | 2048 | 1B 參數版本 |
| mistral | 4096 | Mistral 模型 |
| codellama | 4096 | Code Llama 模型 |

## 🔧 進階修復

### 檢查所有可用模型

```bash
# 列出所有可用模型
ollama list

# 測試每個模型的維度
python fix_embedding_dimension.py
```

### 使用不同的模型

如果你想使用不同的模型：

```bash
# 更新 .env 檔案
OLLAMA_CHAT_MODEL=llama2
OLLAMA_EMBEDDING_MODEL=llama2
EMBEDDING_DIM=4096
```

### 重新建立自定義模型

```bash
# 刪除舊模型
ollama rm llama-3.2-1b-instruct

# 重新創建
python setup_custom_model_windows.py
```

## 📝 驗證修復

修復後，驗證設定：

```bash
# 測試嵌入生成
python test_ollama_integration.py

# 重新建立索引
python main.py

# 啟動應用
streamlit run app.py
```

## 💡 預防措施

1. **記錄模型維度**：記錄每個模型的嵌入維度
2. **測試新模型**：添加新模型時先測試維度
3. **版本控制**：將 `.env` 檔案加入版本控制
4. **備份索引**：定期備份 FAISS 索引

## 🔄 如果問題持續

如果問題持續存在：

1. **重新安裝 Ollama**：確保使用最新版本
2. **檢查模型完整性**：重新下載模型
3. **使用標準模型**：嘗試使用 `llama2` 而不是自定義模型
4. **檢查記憶體**：確保有足夠的 RAM

## 📞 支援

如果仍然遇到問題：

1. 檢查 Ollama 日誌：`ollama logs`
2. 驗證模型：`ollama show <model_name>`
3. 測試連接：`curl http://localhost:11434/api/tags`
4. 檢查系統資源：記憶體和磁碟空間
