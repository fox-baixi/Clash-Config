#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载 YAML 文件并检查是否有变化
"""

import os
import sys
import hashlib
import requests

def calculate_file_hash(file_path):
    """计算文件的 SHA256 哈希值"""
    if not os.path.exists(file_path):
        return None
    
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def download_yaml(url, output_path):
    """下载 YAML 文件"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ 成功下载 YAML 文件到 {output_path}")
        return True
    except Exception as e:
        print(f"✗ 下载失败: {e}")
        return False

def main():
    # 从环境变量获取 URL
    yaml_url = os.environ.get('YAML_URL')
    if not yaml_url:
        print("✗ 错误: 未设置 YAML_URL 环境变量")
        sys.exit(1)
    
    output_file = 'source.yaml'
    temp_file = 'source_temp.yaml'
    
    print(f"开始下载 YAML 文件...")
    print(f"URL: {yaml_url}")
    
    # 下载到临时文件
    if not download_yaml(yaml_url, temp_file):
        sys.exit(1)
    
    # 计算新旧文件的哈希值
    old_hash = calculate_file_hash(output_file)
    new_hash = calculate_file_hash(temp_file)
    
    # 比对是否有变化
    if old_hash == new_hash:
        print("✓ 文件内容未变化，跳过更新")
        os.remove(temp_file)
        # 设置 GitHub Actions 输出
        with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            f.write('changed=false\n')
    else:
        print("✓ 检测到文件变化，准备更新")
        # 替换旧文件
        if os.path.exists(output_file):
            os.remove(output_file)
        os.rename(temp_file, output_file)
        
        # 设置 GitHub Actions 输出
        with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            f.write('changed=true\n')
        
        print(f"  旧哈希: {old_hash}")
        print(f"  新哈希: {new_hash}")

if __name__ == '__main__':
    main()
