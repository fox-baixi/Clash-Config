# Clash 规则自动更新与同步

这个仓库自动从上游源获取 Clash 配置文件，生成规则列表文件，并同步到 GitHub Gist 以便公开访问。

## 📋 功能特点

- ✨ **自动更新**：每周一自动检查上游 YAML 文件是否有更新
- 🧠 **智能比对**：忽略时间戳变化，仅在实质内容变化时才执行更新
- � **Gist 同步**：自动将生成的规则文件同步到 GitHub Gist
- �📦 **规则分类**：自动将规则按代理组分类生成独立的 list 文件
- 🤖 **全自动化**：使用 GitHub Actions 完全自动化，无需手动干预
- ✅ **完整性验证**：下载后验证 YAML 文件的有效性和完整性
- 📧 **邮件通知**：当更新失败时发送邮件通知

## 📁 文件说明

### 规则列表文件 (Clash/)

- `Proxy.list` - 🔰国外流量规则
- `Telegram.list` - ✈️Telegram 规则
- `Youtube.list` - 🎬Youtube 规则
- `Netflix.list` - 🎬Netflix 规则
- `Bilibili.list` - 🎬哔哩哔哩规则
- `Media.list` - 🎬国外媒体规则
- `Apple.list` - 🍎苹果服务规则
- `Direct.list` - 直连规则
- `ACL4SS_Pro.ini` - ACL4SS 配置文件

### 源文件

- `source.yaml` - 上游下载的原始 YAML 配置文件

### 脚本文件

- `download_yaml.py` - 下载、验证并智能比对 YAML 文件
- `generate_list_files.py` - 从 YAML 提取规则并生成 list 文件

## 🚀 使用方法

### 自动更新

仓库包含两个 GitHub Actions 工作流：

#### 1. **Update Clash Rules** (`update-rules.yml`)
- **触发时机**：
  - 每周一北京时间 8:00（UTC 0:00）
  - 手动触发
- **功能**：
  - 下载并验证 YAML 文件
  - 智能比对（忽略时间戳，只检测实质内容变化）
  - 生成规则列表文件
  - 提交到 GitHub 仓库
  - 失败时发送邮件通知

#### 2. **Gist Changes Sync** (`gist-Changes-Sync.yml`)
- **触发时机**：
  - 当 `Clash/` 文件夹或 `source.yaml` 被推送到 main 分支时
  - 手动触发
- **功能**：
  - 检测文件变化
  - 如果 `source.yaml` 变化，重新生成规则文件
  - 将所有 `.list` 和 `.ini` 文件同步到 Gist
  - 使用内容比对，避免不必要的 Gist 更新

### 手动触发

在 GitHub 仓库的 **Actions** 页面，选择对应的 workflow，点击 **"Run workflow"** 按钮。

### 本地运行

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

编辑 `config.ini` 文件：

```ini
[source]
yaml_url = 你的新订阅地址
```

### 配置文件说明 (`config.ini`)

```ini
[source]
# YAML 下载地址
yaml_url = 你的订阅地址

[validation]
# 验证必需字段（逗号分隔）
required_fields = rules,proxies,proxy-groups
# 最小规则数量（少于此值视为异常）
min_rules = 50
```

### Gist 同步配置

需要在 GitHub 仓库中设置 Secret：

1. 前往 **Settings → Secrets and variables → Actions**
2. 添加 Secret：
   - Name: `GIST_TOKEN`
   - Value: 你的 GitHub Personal Access Token（需要 `gist` 权限）

修改目标 Gist ID（在 `gist-Changes-Sync.yml` 中）：

```yaml
env:
  GIST_ID: 你的Gist ID
```

### 邮件通知配置

当 YAML 文件下载失败或验证不通过时，系统会发送邮件通知。

**设置步骤**：

1. 在 GitHub 仓库中设置 Secrets（Settings → Secrets and variables → Actions）：
   - `MAIL_USERNAME`：发件邮箱（如 Gmail）
   - `MAIL_PASSWORD`：邮箱应用专用密码
   - `MAIL_TO`：接收通知的邮箱

2. 如果使用 Gmail，需要开启"应用专用密码"

**注意**：如果不配置邮件 Secrets，通知步骤会被跳过，不影响其他功能。

### 修改更新频率

在 `.github/workflows/update-rules.yml` 文件中修改 cron 表达式：

```yaml
schedule:
  # 每周一北京时间 8:00 运行
  - cron: '0 0 * * 1'
  
  # 如果需要每天运行两次（早晚各一次）：
  # - cron: '0 0,12 * * *'  # 北京时间 8:00 和 20:00
  
  # 如果需要每天运行一次：
  # - cron: '0 0 * * *'  # 北京时间 8:00
```

## 📊 工作流程

### 自动更新流程

```
定时触发 → 下载 YAML → 验证完整性 → 内容比对（忽略时间戳）
                                              ↓
                                          发现变化？
                                              ↓
                                             是
                                              ↓
                            生成 list 文件 → 提交到 GitHub
                                              ↓
                                    触发 Gist 同步工作流
                                              ↓
                                      同步到 GitHub Gist
```

### 智能比对机制

**内容哈希计算**：
- 读取整个文件的所有行
- 过滤掉包含"上次更新于"或"Last updated"的时间戳行
- 对剩余内容计算 SHA256 哈希值
- 只在实质内容变化时触发更新

**优势**：
- ✅ 避免因时间戳更新导致的不必要提交
- ✅ 减少 Git 历史噪音
- ✅ 节省 GitHub Actions 运行时间
- ✅ 降低 Gist 同步频率

## 🔗 访问规则文件

规则文件同步到 Gist 后，可以通过以下格式访问：

```
https://gist.githubusercontent.com/用户名/Gist-ID/raw/文件名
```

例如：
```
https://gist.githubusercontent.com/fox-baixi/128a370090d45e8da2bf3dd2bca2f0e7/raw/Proxy.list
```

## 📝 更新日志

所有自动更新都会以 commit 的形式记录在 Git 历史中，commit 信息包含更新时间和类型。

## 📄 许可证

MIT License
