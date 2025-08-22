# CodeRAG 程式碼索引指南

## 🎯 概述

CodeRAG 會自動索引你專案中的 Python 程式碼，讓你可以用自然語言查詢你的程式碼庫。這個指南會詳細解釋程式碼應該放在哪裡，以及索引是如何工作的。

## 📁 程式碼存放位置

### 預設位置
根據你的 `.env` 檔案設定，CodeRAG 會監控以下目錄：

```bash
# 在 .env 檔案中設定
WATCHED_DIR=.
```

這表示 CodeRAG 會索引**當前專案目錄**（你的 CodeRAG 專案資料夾）中的所有 Python 檔案。

### 當前索引的檔案
從你的專案結構來看，CodeRAG 目前會索引：

```
CodeRAG/
├── app.py                    ✅ 會被索引
├── main.py                   ✅ 會被索引
├── prompt_flow.py            ✅ 會被索引
├── coderag/
│   ├── __init__.py           ✅ 會被索引
│   ├── config.py             ✅ 會被索引
│   ├── embeddings.py         ✅ 會被索引
│   ├── index.py              ✅ 會被索引
│   ├── monitor.py            ✅ 會被索引
│   └── search.py             ✅ 會被索引
├── scripts/
│   ├── initialize_index.py   ✅ 會被索引
│   └── run_monitor.py        ✅ 會被索引
└── tests/
    └── test_faiss.py         ✅ 會被索引
```

## 🔍 索引機制

### 1. 初始索引
當你運行 `python main.py` 時：
- 清除舊的 FAISS 索引
- 掃描 `WATCHED_DIR` 中的所有 `.py` 檔案
- 為每個檔案生成嵌入向量
- 將檔案內容和嵌入儲存到 FAISS 索引中

### 2. 即時監控
CodeRAG 使用 `watchdog` 監控檔案系統變化：
- 當你修改任何 `.py` 檔案時，會自動重新索引
- 新的嵌入會即時更新到 FAISS 索引中
- 不需要手動重新運行索引

### 3. 忽略的檔案和目錄
以下內容會被自動忽略：
```python
IGNORE_PATHS = [
    ".venv",           # 虛擬環境
    "node_modules",    # Node.js 模組
    "__pycache__",     # Python 快取
    ".git",           # Git 版本控制
    "tests",          # 測試目錄
]
```

## 🛠️ 自訂索引設定

### 方法 1: 修改 .env 檔案

```bash
# 索引當前目錄（預設）
WATCHED_DIR=.

# 索引特定目錄
WATCHED_DIR=/path/to/your/code

# 索引上層目錄
WATCHED_DIR=..
```

### 方法 2: 修改 config.py

```python
# 在 coderag/config.py 中修改
WATCHED_DIR = os.getenv("WATCHED_DIR", "/your/custom/path")

# 添加更多忽略的目錄
IGNORE_PATHS = [
    # ... 現有的忽略路徑
    "/path/to/ignore",
    "build",
    "dist",
    "*.log"
]
```

## 📂 常見使用場景

### 場景 1: 索引單一專案
```bash
# 在專案根目錄中
WATCHED_DIR=.
```

### 場景 2: 索引多個專案
```bash
# 索引父目錄下的所有專案
WATCHED_DIR=..

# 或索引特定目錄
WATCHED_DIR=/Users/username/Projects
```

### 場景 3: 索引特定程式碼庫
```bash
# 索引你的主要程式碼庫
WATCHED_DIR=/path/to/your/main/project
```

## 🔧 進階設定

### 支援的檔案類型
目前 CodeRAG 只索引 `.py` 檔案，但你可以修改 `monitor.py` 來支援其他檔案類型：

```python
# 在 coderag/monitor.py 中
if event.src_path.endswith((".py", ".js", ".ts", ".java", ".cpp")):
    # 處理多種檔案類型
```

### 自訂檔案過濾
```python
def should_index_file(filepath):
    """自訂檔案過濾邏輯"""
    # 只索引特定目錄
    if not filepath.startswith("/path/to/code"):
        return False
    
    # 排除特定檔案
    if "temp" in filepath or "backup" in filepath:
        return False
    
    return True
```

## 📊 索引狀態檢查

### 檢查索引的檔案
```bash
# 查看 FAISS 索引檔案大小
ls -la coderag_index.faiss metadata.npy

# 檢查索引內容（需要額外的工具）
python -c "
import numpy as np
metadata = np.load('metadata.npy', allow_pickle=True)
print(f'索引了 {len(metadata)} 個檔案')
for item in metadata:
    print(f'- {item[0]}')
"
```

### 重新建立索引
```bash
# 清除並重新建立索引
python main.py

# 或只重新索引（不清除）
python -c "
from coderag.index import clear_index, save_index
from main import full_reindex
full_reindex()
"
```

## 🚀 最佳實踐

### 1. 專案組織
```
YourProject/
├── src/                    # 主要程式碼
│   ├── core/
│   ├── utils/
│   └── api/
├── tests/                  # 測試（會被忽略）
├── docs/                   # 文件
└── .env                    # CodeRAG 設定
```

### 2. 設定建議
```bash
# .env 檔案
WATCHED_DIR=./src           # 只索引 src 目錄
FAISS_INDEX_FILE=./index/coderag_index.faiss
EMBEDDING_DIM=2048          # 根據你的模型調整
```

### 3. 效能優化
- 避免索引大型二進制檔案
- 定期清理不需要的檔案
- 使用 `.gitignore` 來排除不需要的檔案

## 🔍 故障排除

### 問題 1: 檔案沒有被索引
```bash
# 檢查檔案是否在 WATCHED_DIR 中
echo $WATCHED_DIR
ls -la $WATCHED_DIR

# 檢查檔案是否被忽略
python -c "
from coderag.config import WATCHED_DIR, IGNORE_PATHS
print(f'WATCHED_DIR: {WATCHED_DIR}')
print(f'IGNORE_PATHS: {IGNORE_PATHS}')
"
```

### 問題 2: 索引檔案太大
```bash
# 檢查索引檔案大小
du -h coderag_index.faiss metadata.npy

# 如果太大，考慮只索引重要目錄
WATCHED_DIR=./src
```

### 問題 3: 監控不工作
```bash
# 檢查 watchdog 是否正常運行
python -c "
from watchdog.observers import Observer
print('Watchdog 可用')
"
```

## 📝 總結

1. **預設位置**：CodeRAG 會索引當前目錄中的所有 `.py` 檔案
2. **即時更新**：修改檔案時會自動重新索引
3. **可自訂**：可以修改 `WATCHED_DIR` 來索引不同位置
4. **智慧過濾**：自動忽略常見的不需要索引的目錄

現在你可以開始在 CodeRAG 目錄中編寫程式碼，或者修改 `.env` 檔案來索引其他位置的程式碼！
