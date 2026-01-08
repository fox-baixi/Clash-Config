# Clash Configuration & Rules Sync

这个仓库用于维护自定义 Clash 配置文件及规则，并通过 GitHub Actions 自动同步到 GitHub Gist。

## 📋 功能特点

- ✨ **配置维护**：托管定制化的 `ACL4SS_Pro_Custom.ini` 模板
- 📁 **本地规则**：包含提取的防吸血/直连规则列表 (`Local_Download.list`)
- 🔄 **Gist 同步**：提交更改到 `main` 分支时，自动将 `Clash/` 目录下的文件同步到指定的 GitHub Gist

## 📁 文件说明

### 核心配置 (Clash/)

- `ACL4SS_Pro_Custom.ini` - � 自定义 Clash 配置文件模板（包含自动选择、防吸血等优化）
- `Local_Download.list` - 🛑 本地防吸血/直连规则（提取自 Process-Name/Keyword）
- `ACL4SS_Pro.ini` - 原始规则模板备份

### 规则列表

- `Proxy.list`
- `Telegram.list`
- `Netflix.list`
- `Bilibili.list`
- `Apple.list`
- `Direct.list`
- 其他各类媒体与屏蔽列表...

## 🚀 使用方法

### 1. 修改配置
直接编辑 `Clash/` 目录下的 `.ini` 或 `.list` 文件。

### 2. 自动同步
将更改提交并推送到 GitHub 仓库的 `main` 分支：

```bash
git add .
git commit -m "Update rules"
git push
```

**[Gist Changes Sync](.github/workflows/gist-Changes-Sync.yml)** 工作流会自动触发：
1. 检测文件变化
2. 将变动同步到您配置的 GitHub Gist
3. 您可以在订阅转换工具中直接使用 Gist 的 Raw 链接

## 🔗 访问地址

同步后的文件可通过 Gist Raw 链接访问（用于订阅转换）：

```
https://gist.githubusercontent.com/<用户名>/<Gist-ID>/raw/<文件名>
```

例如：
```
https://gist.githubusercontent.com/fox-baixi/128a370090d45e8da2bf3dd2bca2f0e7/raw/ACL4SS_Pro_Custom.ini
```

## ⚙️ 配置说明

### Gist 同步配置
需要在 GitHub 仓库中设置 Secret（Settings → Secrets and variables → Actions）：
- `GIST_TOKEN`: 具有 `gist` 权限的 GitHub Personal Access Token

在 `.github/workflows/gist-Changes-Sync.yml` 中配置目标 Gist ID：
```yaml
env:
  GIST_ID: 您的Gist ID
```

## 📄 许可证

MIT License
