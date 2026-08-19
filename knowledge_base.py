#知识库
import hashlib
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from datetime import datetime

def check_md5(md5_str: str):
    #检查传入的md字符串是否已经被处理了
    if not os.path.exists(config.md5_path):
        #条件表示没处理过
        open(config.md5_path, 'w',encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path, 'r',encoding='utf-8').readlines():
            line = line.strip()  #处理空格和回车
            if line == md5_str:
                return True
        return False

def save_md5(md5_str: str):
    #将传入的md5字符串记录到文件内保存
    with open(config.md5_path, 'a',encoding='utf-8') as f :
        f.write(md5_str + '\n')

def ger_string_md5(input_str: str,encoding='utf-8'):
    # 将传入的字符串转换为md5字符串

    #将字符串还原为bytes数组
    str_bytes = input_str.encode(encoding=encoding)

    #创建md5对象
    md5_obj = hashlib.md5()     #得到md5对象
    md5_obj.update(str_bytes)   #更新内容（传入要被转换的字节数组）
    md5_hex = md5_obj.hexdigest()  #得到md5的十六进制字符串
    return md5_hex
class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)

        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory,
        )     #向量存储的实例
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len,
        )    #文本切割器的对象

    def upload_by_str(self,data,filename):
        #将传入的字符串，进行向量化，存入向量数据库中
        md5_hex = ger_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过，内容已存在知识库中]"
        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "小曹",
        }
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],
        )

        save_md5(md5_hex)

        return "[成功]内容已经成功载入向量库"

if __name__ == '__main__':
    service = KnowledgeBaseService()
    r = service.upload_by_str("周杰伦","test.file")
    print(r)