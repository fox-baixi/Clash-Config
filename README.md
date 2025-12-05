# Clash 规则自动更新

这个仓库自动从上游源获取 Clash 配置文件，并生成对应的规则列表文件。

## 📋 功能特点

- ✨ **自动更新**：每天自动检查上游 YAML 文件是否有更新
- 🔍 **智能比对**：仅在文件内容变化时才执行更新
- 📦 **规则分类**：自动将规则按代理组分类生成独立的 list 文件
- 🤖 **全自动化**：使用 GitHub Actions 完全自动化，无需手动干预

## 📁 文件说明

### 规则列表文件

- `Proxy.list` - 🔰国外流量规则
- `Telegram.list` - ✈️Telegram 规则
- `Youtube.list` - 🎬Youtube 规则
- `Netflix.list` - 🎬Netflix 规则
- `Bilibili.list` - 🎬哔哩哔哩规则
- `Media.list` - 🎬国外媒体规则
- `Apple.list` - 🍎苹果服务规则
- `Direct.list` - 直连规则

### 源文件

- `source.yaml` - 上游下载的原始 YAML 配置文件

### 脚本文件

- `generate_list_files.py` - 从 YAML 提取规则并生成 list 文件
- `download_yaml.py` - 下载并比对 YAML 文件的脚本

## 🚀 使用方法

### 自动更新

GitHub Actions 会在以下情况下自动运行：

- 每天北京时间 08:00 和 20:00
- 手动触发（在 Actions 页面点击 "Run workflow"）

### 手动运行

如果需要在本地运行脚本：

1. 安装依赖：
   ```bash
   pip install pyyaml requests
   ```

2. 设置环境变量并下载 YAML：
   ```bash
   # Windows PowerShell
   $env:YAML_URL="你的YAML地址"
   python download_yaml.py
   ```

3. 生成规则列表：
   ```bash
   python generate_list_files.py
   ```

## ⚙️ 配置说明

### 修改 YAML 源地址

如果上游地址变化，需要修改 `.github/workflows/update-rules.yml` 文件中的 `YAML_URL` 环境变量：

```yaml
env:
  YAML_URL: 你的新地址
```

### 修改更新频率

在 `.github/workflows/update-rules.yml` 文件中修改 cron 表达式：

```yaml
schedule:
  - cron: '0 0,12 * * *'  # 修改这里
```

## 📊 工作流程

```
下载 YAML → 比对哈希值 → 发现变化？
                           ↓
                          是
                           ↓
              生成 list 文件 → 提交到 GitHub
```

## 📝 更新日志

所有自动更新都会以 commit 的形式记录在 Git 历史中，commit 信息包含更新时间。

## 📄 许可证

MIT License
