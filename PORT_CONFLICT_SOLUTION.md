# 解決 Ollama 端口衝突問題

## 🚨 問題描述

當你運行 `ollama serve` 時出現錯誤：
```
Error: listen tcp 127.0.0.1:11434: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.
```

這表示端口 11434 已經被佔用。

## 🔍 快速診斷

運行診斷腳本：
```bash
python check_ollama_status.py
```

## 🛠️ 解決方案

### 方法 1: 自動修復（推薦）

```bash
python check_ollama_status.py
```

這個腳本會：
- 檢查 Ollama 是否正在運行
- 檢查 API 是否響應
- 檢查端口使用情況
- 自動停止和重啟 Ollama

### 方法 2: 手動修復

#### 步驟 1: 檢查 Ollama 進程

```bash
# 檢查 Ollama 是否在運行
tasklist /FI "IMAGENAME eq ollama.exe"

# 檢查端口使用情況
netstat -ano | findstr :11434
```

#### 步驟 2: 停止 Ollama

```bash
# 強制停止 Ollama 進程
taskkill /F /IM ollama.exe
```

#### 步驟 3: 重新啟動 Ollama

```bash
# 在背景啟動 Ollama
ollama serve
```

### 方法 3: 使用不同的端口

如果端口 11434 被其他程序佔用，你可以使用不同的端口：

#### 步驟 1: 設定環境變數

```bash
# 設定不同的端口
set OLLAMA_HOST=127.0.0.1:11435
ollama serve
```

#### 步驟 2: 更新 .env 檔案

```bash
# 在 .env 檔案中更新端口
OLLAMA_BASE_URL=http://localhost:11435
```

## 🔧 常見問題

### 1. Ollama 進程卡住

```bash
# 強制終止所有 Ollama 進程
taskkill /F /IM ollama.exe /T
```

### 2. 端口被其他程序佔用

```bash
# 查看佔用端口的進程
netstat -ano | findstr :11434

# 終止特定進程（替換 PID 為實際進程 ID）
taskkill /F /PID <PID>
```

### 3. 防火牆問題

- 檢查 Windows Defender 防火牆設定
- 確保 Ollama 有網路訪問權限

## 📝 驗證修復

修復後，驗證 Ollama 是否正常工作：

```bash
# 檢查 Ollama 狀態
ollama list

# 測試 API
curl http://localhost:11434/api/tags
```

## 🚀 繼續設定

端口問題解決後，繼續你的設定：

```bash
# 運行設定腳本
python setup_custom_model_windows.py

# 或手動設定
ollama create llama-3.2-1b-instruct -f Modelfile
```

## 💡 預防措施

1. **避免重複啟動**：不要同時運行多個 `ollama serve`
2. **正確關閉**：使用 Ctrl+C 正確關閉 Ollama
3. **檢查進程**：定期檢查是否有殘留的 Ollama 進程

## 📞 如果問題持續

如果問題持續存在：

1. 重新啟動電腦
2. 重新安裝 Ollama
3. 檢查是否有其他程序使用端口 11434
4. 使用不同的端口號
