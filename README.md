# RAG 知识库智能问答系统

基于 **LangChain + Chroma + 阿里云百炼（DashScope）** 的 RAG 知识库问答系统。支持知识库文档自动分块入库、向量检索增强生成、多轮对话记忆，并提供 Streamlit 网页界面完成文件上传与对话问答。

## 功能特性

- **知识库构建**：TXT 文件上传 → RecursiveCharacterTextSplitter 分块（chunk_size=1000 / overlap=100，兼容中英文标点）→ DashScope text-embedding-v4 向量化 → Chroma 持久化存储
- **内容去重**：基于 MD5 指纹记录已入库内容，重复内容直接跳过，避免重复消耗 Embedding API
- **RAG 问答**：向量检索 → 文档格式化 → 提示词拼接 → Qwen3-max 生成，检索为空时兜底提示"无相关资料"，回答可溯源
- **多轮对话**：继承 `BaseChatMessageHistory` 自定义 JSON 文件持久化会话历史，按 `session_id` 隔离，重启不丢历史
- **Web 界面**：`app_file_uploader.py` 知识库更新页 + `app_qa.py` 智能客服对话页

## 技术栈

Python · LangChain · Chroma · 阿里云百炼 DashScope（text-embedding-v4 / qwen3-max）· Streamlit

## 项目结构

```
├── rag.py                 # RAG 问答链（检索 → 提示词 → 模型 → 解析，含多轮对话）
├── knowledge_base.py      # 知识库入库（分块、向量化、MD5 去重）
├── vector_stores.py       # Chroma 向量库封装
├── file_history_store.py  # 自定义会话历史持久化（JSON 文件）
├── app_file_uploader.py   # Streamlit：文件上传更新知识库
├── app_qa.py              # Streamlit：对话式问答
├── config_data.py         # 全局配置
├── data/                  # 示例知识文档（服装穿搭）
├── chroma_db/             # 向量库持久化目录（运行时生成）
└── requirements.txt
```

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置阿里云百炼 API Key
# Windows:  set DASHSCOPE_API_KEY=sk-xxx
# macOS/Linux: export DASHSCOPE_API_KEY=sk-xxx

# 3. （可选）将 data/ 下的示例文档入库
python knowledge_base.py

# 4. 启动问答
python rag.py                      # 命令行测试
streamlit run app_qa.py            # 网页对话
streamlit run app_file_uploader.py # 网页上传知识文档
```

## 说明

- 首次运行会创建 `chroma_db/` 向量库与 `md5.text` 去重记录，`chat_history/` 存放会话历史文件，三者均为运行时生成，不入库
- 模型、分块参数、检索数量可在 `config_data.py` 中调整
