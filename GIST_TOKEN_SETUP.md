# 设置 Gist Token 指南

## 📝 创建 GitHub Personal Access Token

### 步骤 1：生成 Token

1. **登录 GitHub**，访问：https://github.com/settings/tokens

2. **点击 "Generate new token (classic)"**

3. **配置 Token**：
   - **Note**（名称）：填写 `Clash-Config Gist Sync`
   - **Expiration**（过期时间）：选择 `No expiration`（不过期）或选择一个时间
   - **Select scopes**（权限选择）：
     - ✅ **gist** - 勾选这一项即可（允许创建和更新 Gist）

4. **点击 "Generate token"** 生成

5. **复制 Token**：
   - ⚠️ Token 只显示一次，请立即复制保存
   - Token 格式类似：`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 步骤 2：添加到 GitHub Repository Secrets

1. **访问仓库设置**：
   - 打开：https://github.com/fox-baixi/Clash-Config/settings/secrets/actions

2. **添加 Secret**：
   - 点击 **"New repository secret"**
   - **Name**（名称）：填写 `GIST_TOKEN`
   - **Value**（值）：粘贴刚才复制的 Token
   - 点击 **"Add secret"**

## ✅ 验证设置

设置完成后，下次自动运行时（每周一早上 8:00），系统会：

1. 从源地址下载 YAML 文件
2. 生成规则列表文件
3. 提交到私有 GitHub 仓库
4. **自动同步到 Gist**（新增！）

## 🔗 Gist 链接

您的 Gist ID：`128a370090d45e8da2bf3dd2bca2f0e7`

**访问地址**：
- Gist 页面：https://gist.github.com/fox-baixi/128a370090d45e8da2bf3dd2bca2f0e7
- Raw 链接示例：
  ```
  https://gist.githubusercontent.com/fox-baixi/128a370090d45e8da2bf3dd2bca2f0e7/raw/Proxy.list
  ```

## 🧪 手动测试

设置好 Token 后，您可以在 GitHub Actions 页面手动触发一次运行来测试：

1. 访问：https://github.com/fox-baixi/Clash-Config/actions
2. 点击 "Update Clash Rules" workflow
3. 点击 "Run workflow" 按钮
4. 等待运行完成，检查 Gist 是否更新

## ⚠️ 注意事项

- Token 具有访问权限，请妥善保管
- 不要将 Token 提交到代码中
- 只需要 `gist` 权限，不要勾选其他权限
- 如果 Token 泄露，立即在 GitHub 设置中删除并重新生成

## 📊 Lint 警告说明

关于 workflow 文件中的这些警告：
- `Context access might be invalid: GIST_TOKEN`
- `Context access might be invalid: MAIL_USERNAME/PASSWORD/TO`

这些是正常的，因为：
- 这些是可选的 GitHub Secrets
- 只有在您配置后才会存在
- 不影响功能运行
