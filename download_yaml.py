#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载 YAML 文件并检查是否有变化
支持完整性验证和错误检测
"""

import os
import sys
import hashlib
import requests
import yaml
import configparser
import re

def load_config():
    """加载配置文件"""
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    return config

def calculate_file_hash(file_path):
    """计算文件的 SHA256 哈希值"""
    if not os.path.exists(file_path):
        return None
    
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def calculate_content_hash(file_path):
    """计算文件内容的 SHA256 哈希值，忽略时间戳行"""
    if not os.path.exists(file_path):
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 过滤掉时间戳行（包含 "上次更新于" 或 "Last updated"）
        filtered_lines = [
            line for line in lines 
            if not re.search(r'上次更新于[:：]|Last updated[:：]|last updated[:：]', line, re.IGNORECASE)
        ]
        
        # 计算过滤后内容的哈希值
        content = ''.join(filtered_lines)
        sha256_hash = hashlib.sha256()
        sha256_hash.update(content.encode('utf-8'))
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"⚠️ 计算内容哈希时出错: {e}")
        # 如果出错，回退到计算整个文件的哈希
        return calculate_file_hash(file_path)

def download_yaml(url, output_path):
    """下载 YAML 文件"""
    try:
        print(f"正在下载: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ 成功下载到 {output_path}")
        return True
    except Exception as e:
        print(f"✗ 下载失败: {e}")
        return False

def validate_yaml_file(file_path, config):
    """验证 YAML 文件的完整性和有效性"""
    errors = []
    
    try:
        # 1. 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 2. 检测是否是 HTML（续费页面、错误页面等）
        if content.strip().startswith('<!DOCTYPE') or content.strip().startswith('<html'):
            errors.append("❌ 文件内容是 HTML 页面，不是有效的 YAML 文件！可能是订阅过期或链接失效。")
            return False, errors
        
        # 3. 检测是否包含常见错误信息
        error_keywords = ['404', 'not found', 'expired', '过期', '错误', 'error']
        first_line = content.split('\n')[0].lower() if content else ''
        if any(keyword in first_line for keyword in error_keywords):
            errors.append(f"⚠️ 文件开头包含错误关键词: {first_line[:100]}")
        
        # 4. 尝试解析 YAML
        try:
            yaml_data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            errors.append(f"❌ YAML 格式无效: {str(e)}")
            return False, errors
        
        # 5. 检查是否为空或不是字典
        if not yaml_data or not isinstance(yaml_data, dict):
            errors.append("❌ YAML 文件为空或格式不正确")
            return False, errors
        
        # 6. 检查必需字段
        required_fields = config.get('validation', 'required_fields', fallback='rules,proxies,proxy-groups').split(',')
        missing_fields = []
        for field in required_fields:
            field = field.strip()
            if field not in yaml_data:
                missing_fields.append(field)
        
        if missing_fields:
            errors.append(f"❌ 缺少必需字段: {', '.join(missing_fields)}")
            return False, errors
        
        # 7. 检查规则数量
        min_rules = config.getint('validation', 'min_rules', fallback=50)
        rules = yaml_data.get('rules', [])
        if not isinstance(rules, list) or len(rules) < min_rules:
            errors.append(f"⚠️ 规则数量异常: 只有 {len(rules) if isinstance(rules, list) else 0} 条，期望至少 {min_rules} 条")
            return False, errors
        
        # 8. 检查代理组数量
        proxy_groups = yaml_data.get('proxy-groups', [])
        if not isinstance(proxy_groups, list) or len(proxy_groups) == 0:
            errors.append("⚠️ 没有找到代理组")
        
        # 9. 验证通过
        print(f"✅ YAML 文件验证通过:")
        print(f"   - 规则数量: {len(rules)}")
        print(f"   - 代理数量: {len(yaml_data.get('proxies', []))}")
        print(f"   - 代理组数量: {len(proxy_groups)}")
        
        return True, []
        
    except Exception as e:
        errors.append(f"❌ 验证过程出错: {str(e)}")
        return False, errors

def set_github_output(key, value):
    """设置 GitHub Actions 输出"""
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f'{key}={value}\n')

def set_error_message(errors):
    """设置错误消息供 GitHub Actions 使用"""
    error_msg = '\n'.join(errors)
    # 转义特殊字符
    error_msg = error_msg.replace('%', '%25').replace('\n', '%0A').replace('\r', '%0D')
    set_github_output('error_message', error_msg)

def main():
    print("=" * 60)
    print("Clash YAML 文件下载与验证工具")
    print("=" * 60)
    
    # 加载配置
    try:
        config = load_config()
        yaml_url = config.get('source', 'yaml_url')
        print(f"\n📋 从配置文件读取 URL")
    except Exception as e:
        print(f"⚠️ 无法读取配置文件，尝试使用环境变量: {e}")
        yaml_url = os.environ.get('YAML_URL')
        config = configparser.ConfigParser()
        # 设置默认值
        config.add_section('validation')
        config.set('validation', 'required_fields', 'rules,proxies,proxy-groups')
        config.set('validation', 'min_rules', '50')
    
    if not yaml_url:
        print("✗ 错误: 未找到 YAML URL（检查 config.ini 或 YAML_URL 环境变量）")
        sys.exit(1)
    
    output_file = 'source.yaml'
    temp_file = 'source_temp.yaml'
    
    print(f"\n🔗 下载地址: {yaml_url[:50]}...")
    
    # 下载到临时文件
    if not download_yaml(yaml_url, temp_file):
        set_github_output('status', 'failed')
        set_error_message(['下载失败，请检查网络或 URL 是否正确'])
        sys.exit(1)
    
    # 验证 YAML 文件
    print(f"\n🔍 验证 YAML 文件...")
    is_valid, errors = validate_yaml_file(temp_file, config)
    
    if not is_valid:
        print(f"\n{'='*60}")
        print("❌ YAML 文件验证失败!")
        print(f"{'='*60}")
        for error in errors:
            print(error)
        print(f"{'='*60}")
        
        # 清理临时文件
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        # 设置输出供邮件通知
        set_github_output('status', 'invalid')
        set_error_message(errors)
        sys.exit(1)
    
    # 计算新旧文件的哈希值（忽略时间戳）
    old_hash = calculate_content_hash(output_file)
    new_hash = calculate_content_hash(temp_file)
    
    print(f"\n🔐 内容哈希值比对（忽略时间戳）:")
    print(f"   旧: {old_hash}")
    print(f"   新: {new_hash}")
    
    # 比对是否有变化
    if old_hash == new_hash:
        print("\n✓ 文件内容未变化（仅时间戳可能变化），跳过更新")
        os.remove(temp_file)
        set_github_output('changed', 'false')
        set_github_output('status', 'unchanged')
    else:
        print("\n✓ 检测到实质性内容变化，准备更新")
        # 替换旧文件
        if os.path.exists(output_file):
            os.remove(output_file)
        os.rename(temp_file, output_file)
        
        set_github_output('changed', 'true')
        set_github_output('status', 'success')
    
    print(f"\n{'='*60}")
    print("✅ 任务完成")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
