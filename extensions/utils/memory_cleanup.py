#!/usr/bin/env python3
"""
Memory cleanup utility for multi-stock analysis

This script helps clean up ChromaDB collections that might cause conflicts
during multi-threaded analysis.
"""

import chromadb
from chromadb.config import Settings
import os


def cleanup_memory_collections():
    """Clean up all existing memory collections"""
    try:
        client = chromadb.Client(Settings(allow_reset=True))
        
        # Get all collections
        collections = client.list_collections()
        
        memory_collections = []
        for collection in collections:
            if any(name in collection.name for name in ['bull_memory', 'bear_memory']):
                memory_collections.append(collection.name)
        
        print(f"发现 {len(memory_collections)} 个内存集合需要清理")
        
        # Delete memory collections
        for collection_name in memory_collections:
            try:
                client.delete_collection(collection_name)
                print(f"已删除集合: {collection_name}")
            except Exception as e:
                print(f"删除集合 {collection_name} 失败: {str(e)}")
        
        print("内存清理完成")
        
    except Exception as e:
        print(f"清理过程出错: {str(e)}")


def reset_chromadb():
    """完全重置 ChromaDB"""
    try:
        client = chromadb.Client(Settings(allow_reset=True))
        client.reset()
        print("ChromaDB 已完全重置")
    except Exception as e:
        print(f"重置失败: {str(e)}")


if __name__ == "__main__":
    print("ChromaDB 内存清理工具")
    print("=" * 30)
    
    choice = input("选择操作:\n1. 清理内存集合\n2. 完全重置ChromaDB\n请输入选择 (1/2): ").strip()
    
    if choice == "1":
        cleanup_memory_collections()
    elif choice == "2":
        reset_chromadb()
    else:
        print("无效选择")