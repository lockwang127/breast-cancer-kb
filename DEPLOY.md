# 乳腺癌知识库 GitHub 部署指南

本指南帮助您将乳腺癌知识库同步到 GitHub 仓库。

## 前置条件

- 已安装 Git
- 拥有 GitHub 账号
- 可访问 https://github.com/new

## 部署步骤

### Step 1: 创建 GitHub 仓库

1. 访问 [github.com/new](https://github.com/new) 登录 GitHub 账号
2. 创建新仓库，配置如下：
   - **Repository name**: `breast-cancer-kb`
   - **Description**: `结构化的乳腺癌医学知识图谱，基于知识三元组构建`
   - **Visibility**: Public（公开）
   - **Initialize**: 不勾选任何初始化选项

3. 点击 "Create repository" 完成创建

### Step 2: 配置本地仓库并推送

在本地仓库目录中执行以下命令：

```bash
# 进入仓库目录
cd /Users/wangxiaodong/WorkBuddy/breast-cancer-kb

# 初始化 Git（如果尚未初始化）
git init

# 添加所有文件
git add .

# 创建初始提交
git commit -m "feat: 初始化乳腺癌知识库 v1.0.0

- 流行病学数据 (17条三元组)
- 分子分型与生物标志物 (17条三元组)
- CSCO 2024指南推荐 (17条三元组)
- 治疗方案 (17条三元组)
- 共计 68 条知识三元组，4 个知识域"
```

### Step 3: 设置远程仓库

根据您创建的仓库设置远程地址：

```bash
# SSH 方式（推荐）
git remote add origin git@github.com:lockwang127/breast-cancer-kb.git

# 或者 HTTPS 方式
git remote add origin https://github.com/lockwang127/breast-cancer-kb.git
```

### Step 4: 推送代码

```bash
# 推送到 GitHub（首次推送设置上游分支）
git push -u origin main
```

> 注意：如果您使用 HTTPS 方式，系统会提示输入 GitHub 用户名和 Personal Access Token。

## 验证部署

访问 `https://github.com/lockwang127/breast-cancer-kb` 确认代码已成功推送。

## 后续更新

### 添加新知识三元组

1. 编辑对应的知识图谱文件（如 `data/knowledge-graph/epidemiology.json`）
2. 运行构建脚本验证：
   ```bash
   python3 scripts/build_kb.py
   python3 scripts/tests/test_kb_format.py
   ```
3. 提交变更：
   ```bash
   git add .
   git commit -m "feat: 新增XXX知识三元组"
   git push
   ```

### 同步到其他设备

```bash
git clone git@github.com:lockwang127/breast-cancer-kb.git
cd breast-cancer-kb
python3 scripts/build_kb.py
```

## 故障排除

### SSH 方式推送失败

如果 SSH 方式失败，可能需要配置 SSH Key：

```bash
# 检查现有 SSH Key
ls -la ~/.ssh

# 生成新的 SSH Key（如果需要）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 将公钥添加到 GitHub Settings > SSH Keys
```

### HTTPS 方式认证失败

使用 Personal Access Token 替代密码：

1. GitHub Settings > Developer settings > Personal access tokens
2. Generate new token (classic)
3. 勾选 `repo` 权限
4. 使用生成的 token 作为密码

## 仓库地址

- **GitHub**: https://github.com/lockwang127/breast-cancer-kb
- **本地**: `/Users/wangxiaodong/WorkBuddy/breast-cancer-kb/`
