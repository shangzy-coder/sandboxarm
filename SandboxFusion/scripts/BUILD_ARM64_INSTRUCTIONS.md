# ARM64 Docker 构建说明

## 问题解决方案

### 🔍 问题分析
构建过程在 GitHub Workflow 中卡住，根本原因：
1. **镜像源问题** - 在国外环境使用阿里云镜像导致下载缓慢
2. **PyQt5 编译超时** - ARM64 上从源码编译 PyQt5 需要很长时间，exit code 143 表示超时
3. **Python 依赖安装脚本** - install-python-runtime.sh 内部强制使用阿里云源
4. **重型包集中安装** - 所有包一次性安装容易超时
5. **Go 编译卡住** - CGO 依赖在 ARM64 上编译问题

### 🛠️ 修复内容

#### 1. 镜像源智能配置
- **默认使用国外源** - GitHub Actions 构建更快
- **支持国内源** - 通过构建参数控制
- **运行时切换** - 提供脚本供国内用户使用

#### 2. Python 依赖安装优化
- **绕过安装脚本** - 直接在 Dockerfile 中控制镜像源，不依赖 install-python-runtime.sh
- **分层安装策略** - 将包按类型分组安装：基础包 → 科学计算 → 图像处理 → ML框架 → 其余包
- **PyQt5 特殊处理** - 使用 conda 安装而非 pip 编译，避免超时
- **优先二进制包** - 使用 `--prefer-binary` 避免源码编译
- **增加超时保护** - 每个安装步骤都有合理的超时时间

#### 3. ARM64 编译优化
- **禁用 CGO** - 避免 C 代码编译问题
- **限制并发** - 防止内存不足导致卡住
- **强制国外源** - 确保使用 PyPI.org 而非阿里云

### 🚀 使用方法

#### GitHub Actions 构建（推荐）
```bash
# 使用国外源，构建更快
docker build -f scripts/Dockerfile.all-in-one.arm64 \
  --build-arg USE_CHINA_MIRRORS=false \
  -t sandboxfusion-arm64:latest .
```

#### 国内环境构建
```bash
# 使用国内源
docker build -f scripts/Dockerfile.all-in-one.arm64 \
  --build-arg USE_CHINA_MIRRORS=true \
  -t sandboxfusion-arm64:latest .
```

#### 运行时配置国内镜像源
```bash
# 在容器内运行此命令配置阿里云镜像源
/usr/local/bin/setup-china-mirrors.sh
```

### 📋 修改详情

1. **添加构建参数** `USE_CHINA_MIRRORS` 控制镜像源选择
2. **优化 Go 编译** - 禁用 CGO，限制并发，添加超时
3. **跳过问题步骤** - .NET 和 Lean 在 ARM64 上的已知问题
4. **添加超时保护** - Python/Poetry/npm 安装都有超时限制
5. **创建镜像源切换脚本** - 供国内用户运行时使用

### ⚠️ 注意事项

- GitHub Actions 默认使用 `USE_CHINA_MIRRORS=false`
- 国内构建可以设置 `USE_CHINA_MIRRORS=true`
- 构建完成后可以使用 `setup-china-mirrors.sh` 切换到阿里云源
- 所有编译步骤都有容错处理，失败时继续构建

### 🔧 故障排除

如果构建仍然卡住：
1. 检查内存是否充足（建议 8GB+）
2. 确认网络连接稳定
3. 可以增加超时时间
4. 查看具体卡在哪个步骤并单独调试