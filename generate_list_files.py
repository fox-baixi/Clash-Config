#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 YAML 文件提取规则并生成对应的 list 文件
"""

import yaml
import os
import sys
from collections import defaultdict

# 设置输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def load_yaml_file(file_path):
    """加载 YAML 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def extract_rules_by_group(yaml_data):
    """从 YAML 数据中提取规则，按代理组分类"""
    rules = yaml_data.get('rules', [])
    rules_by_group = defaultdict(list)
    
    for rule in rules:
        # rule 格式: "规则类型,规则内容,代理组[,no-resolve]"
        parts = rule.split(',')
        if len(parts) < 3:
            continue
        
        rule_type = parts[0].strip()
        rule_content = parts[1].strip()
        proxy_group = parts[2].strip()
        no_resolve = ',no-resolve' if len(parts) > 3 and 'no-resolve' in parts[3] else ''
        
        # 重建规则（去掉代理组）
        if rule_type in ['IP-CIDR', 'IP-CIDR6']:
            rule_line = f"{rule_type},{rule_content}{no_resolve}"
        else:
            rule_line = f"{rule_type},{rule_content}"
        
        rules_by_group[proxy_group].append(rule_line)
    
    return rules_by_group

def write_list_file(file_path, rules, group_name):
    """写入 list 文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        # 写入文件头注释
        f.write(f"# {group_name} 规则集\n")
        f.write(f"# 从 YAML 文件自动生成\n\n")
        
        # 写入规则
        for rule in rules:
            f.write(f"{rule}\n")

def main():
    # 文件路径
    yaml_file = 'source.yaml'  # GitHub Actions 会下载到当前目录
    output_dir = 'Clash'  # 输出到 Clash 子目录
    
    # 代理组与文件名的映射
    group_to_file = {
        '🔰国外流量': 'Proxy.list',
        '✈️Telegram': 'Telegram.list',
        '🎬Youtube': 'Youtube.list',
        '🎬Netflix': 'Netflix.list',
        '🎬哔哩哔哩': 'Bilibili.list',
        '🎬国外媒体': 'Media.list',
        '🍎苹果服务': 'Apple.list',
        'DIRECT': 'Direct.list',
    }
    
    print("从 YAML 文件提取规则...")
    
    # 加载 YAML 文件
    yaml_data = load_yaml_file(yaml_file)
    
    # 提取规则
    rules_by_group = extract_rules_by_group(yaml_data)
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成文件
    total_rules = 0
    for proxy_group, file_name in group_to_file.items():
        file_path = os.path.join(output_dir, file_name)
        rules = rules_by_group.get(proxy_group, [])
        
        if rules:
            write_list_file(file_path, rules, proxy_group)
            print(f"  {file_name}: {len(rules)} 条规则")
            total_rules += len(rules)
        else:
            print(f"  {file_name}: 0 条规则 (警告)")
    
    print(f"\n总计: {total_rules} 条规则")
    print("所有文件生成完成!")

if __name__ == '__main__':
    main()
