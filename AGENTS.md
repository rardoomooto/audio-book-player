# 有声读物播放器 - 代理配置与工作流指南

## 项目概述

这是一个面向家庭使用的有声读物播放器系统，运行在家庭服务器（如NAS）上。系统包含用户播放界面和管理员后台界面，支持多用户管理、播放时长限制、播放统计等功能。

### 技术栈
- **后端**：FastAPI (Python)
- **前端**：React + TypeScript
- **UI组件库**：Material-UI (MUI)
- **数据库**：PostgreSQL (生产) / SQLite (开发)
- **部署**：Docker + Docker Compose
- **认证**：JWT with refresh tokens
- **存储**：抽象层支持WebDAV + 本地挂载 (SMB/CIFS, NFS)
- **API文档**：OpenAPI（从代码自动生成）
- **图表库**：Chart.js 或 ECharts
- **测试框架**：pytest + httpx (后端), Playwright (前端E2E)

### 项目结构
```
audio-book-player/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/               # API路由
│   │   │   └── v1/           # API v1版本
│   │   ├── core/              # 核心配置
│   │   ├── models/            # SQLAlchemy模型
│   │   ├── schemas/           # Pydantic模式
│   │   ├── services/          # 业务逻辑
│   │   └── utils/             # 工具函数
│   ├── alembic/               # 数据库迁移
│   ├── tests/                 # 测试文件
│   ├── requirements.txt       # Python依赖
│   └── Dockerfile
├── frontend/                   # 前端应用（monorepo）
│   ├── packages/
│   │   ├── user-app/          # 用户界面SPA (/user/*)
│   │   └── admin-app/         # 管理界面SPA (/admin/*)
│   ├── shared/                # 共享代码
│   │   ├── types/            # TypeScript类型
│   │   ├── utils/            # 工具函数
│   │   └── api-client/       # API客户端
│   ├── package.json           # 根配置
│   └── tsconfig.json
├── infra/                      # 基础设施
│   ├── docker-compose.yml     # Docker编排
│   ├── nginx.conf             # Nginx配置
│   └── scripts/               # 部署脚本
├── docs/                       # 文档
├── AGENTS.md                   # 本文件
├── REQUIREMENTS.md            # 需求文档
├── IMPLEMENTATION_PLAN.md     # 实现计划
├── .gitignore
└── README.md
```

---

## 代理配置

### 1. 代码质量代理 (Code Quality Agent)

**职责**：确保代码质量、风格一致性和最佳实践

**触发条件**：
- 代码提交前
- 代码审查时
- 重构前后

**检查内容**：
- Python: PEP 8, Type Hints, Docstrings
- TypeScript: ESLint, Prettier, Type Safety
- 安全性: 密码哈希, SQL注入防护, XSS防护
- 性能: 数据库查询优化, 缓存策略

**工具链**：
- `flake8` (Python linting)
- `black` (Python formatting)
- `mypy` (Python type checking)
- `eslint` (TypeScript/React linting)
- `prettier` (TypeScript/React formatting)

### 2. 测试代理 (Testing Agent)

**职责**：执行测试、生成测试用例、验证功能

**测试类型**：
- **单元测试**：数据模型、业务逻辑、工具函数
- **集成测试**：API端点、数据库交互
- **端到端测试**：用户流程、播放功能
- **性能测试**：并发播放、大量内容导入

**工具链**：
- `pytest` + `httpx` (后端测试)
- `jest` + `react-testing-library` (前端单元测试)
- `playwright` (E2E测试)
- `locust` (性能测试，可选)

**测试策略**：
1. **TDD流程**：先写测试 → 实现 → 重构
2. **测试覆盖率**：核心功能 > 80%
3. **测试数据**：使用fixture和factory模式
4. **测试隔离**：每个测试独立，不依赖外部服务

### 3. 部署代理 (Deployment Agent)

**职责**：管理Docker容器、环境配置、部署流程

**部署环境**：
- **本地开发**：Docker Compose + SQLite
- **测试环境**：Docker Compose + PostgreSQL
- **生产环境**：Docker Compose + PostgreSQL + NAS挂载

**部署流程**：
1. 代码推送到仓库
2. 构建Docker镜像
3. 运行数据库迁移
4. 启动服务容器
5. 健康检查验证

**配置管理**：
- 环境变量：`.env` 文件
- 密钥管理：Docker secrets
- 配置文件：`config/` 目录

### 4. 存储代理 (Storage Agent)

**职责**：管理NAS内容访问、文件索引、元数据提取

**存储协议**：
- **WebDAV**：远程访问NAS
- **本地挂载**：SMB/CIFS、NFS

**功能**：
- 内容扫描和索引
- 元数据提取（标题、作者、时长、封面）
- 文件访问权限控制
- 播放流媒体传输

**工具链**：
- `webdavclient3` (WebDAV客户端)
- `mutagen` (音频元数据提取)
- `ffmpeg` (音频格式转换，可选)

### 5. 认证代理 (Authentication Agent)

**职责**：用户认证、授权、会话管理

**认证方式**：
- JWT with refresh tokens
- 密码哈希：bcrypt
- 角色：user, admin

**安全措施**：
- 短期访问令牌（15分钟）
- 长期刷新令牌（7天）
- 令牌轮换策略
- CSRF保护
- 输入验证

### 6. 统计代理 (Analytics Agent)

**职责**：播放统计、数据分析、报表生成

**统计维度**：
- 时间：每日、每周、每月、每年
- 用户：个人播放历史、使用模式
- 内容：热门内容、播放次数
- 时长：总播放时长、平均播放时长

**可视化**：
- Chart.js 或 ECharts
- 交互式图表
- 数据导出功能

---

## 工作流规约

### 规约1：进度同步

**每完成一次任务后，必须及时将进度更新到计划文档中。**

具体要求：
1. **更新IMPLEMENTATION_PLAN.md**：将已完成的任务标记为 ✅ 已完成
2. **更新里程碑状态**：如果阶段内所有任务完成，标记里程碑为 ✅ 已达成
3. **更新进度概览**：在文件开头的进度概览表中更新完成度
4. **记录关键产出**：在进度概览中列出已完成的关键产出

**触发条件**：
- 单个任务（如T0.1、T1.2）完成时
- 整个阶段完成时
- 里程碑达成时

**执行步骤**：
```
1. 任务完成 → 立即更新IMPLEMENTATION_PLAN.md
2. 标记任务状态：✅ 已完成
3. 检查阶段是否全部完成 → 更新阶段状态
4. 更新进度概览表
5. 向用户报告进度更新完成
```

**示例**：
```markdown
#### T1.4 认证端点 ✅ 已完成
- 实现login、refresh、logout、me端点
- JWT令牌签发和刷新
- **预计时间**：5天
- **依赖**：T1.3
- **交付物**：认证API、JWT实现
- **验收标准**：认证流程正常，令牌安全
```

---

## 工作流指南

### 1. 开发工作流

#### 1.1 功能开发流程
```
1. 创建功能分支：feat/feature-name
2. 编写测试用例（TDD）
3. 实现功能代码
4. 运行本地测试
5. 代码审查
6. 合并到主分支
7. 部署到测试环境
```

#### 1.2 分支命名规范
- `feat/` - 新功能
- `fix/` - Bug修复
- `refactor/` - 重构
- `docs/` - 文档更新
- `test/` - 测试相关
- `chore/` - 构建/工具相关

#### 1.3 提交消息规范
```
类型(范围): 简短描述

详细描述（可选）

相关Issue（可选）
```

示例：
```
feat(auth): 添加JWT认证端点

实现了登录、刷新令牌、登出端点，支持access_token和refresh_token。
包含单元测试和集成测试。

Closes #123
```

### 2. 测试工作流

#### 2.1 后端测试
```bash
# 运行所有测试
cd backend && pytest

# 运行特定测试文件
pytest tests/test_auth.py

# 运行带覆盖率的测试
pytest --cov=app tests/

# 运行并生成HTML报告
pytest --cov=app --cov-report=html tests/
```

#### 2.2 前端测试
```bash
# 运行单元测试
cd frontend && npm test

# 运行E2E测试
npx playwright test

# 运行带UI的测试
npx playwright test --ui
```

#### 2.3 测试覆盖率目标
- 核心业务逻辑：> 90%
- API端点：> 80%
- 工具函数：> 95%
- 组件：> 70%

### 3. 部署工作流

#### 3.1 本地开发
```bash
# 启动开发环境
docker-compose -f docker-compose.dev.yml up -d

# 查看日志
docker-compose logs -f backend

# 停止环境
docker-compose down
```

#### 3.2 测试环境
```bash
# 构建镜像
docker-compose build

# 启动测试环境
docker-compose -f docker-compose.test.yml up -d

# 运行迁移
docker-compose exec backend alembic upgrade head
```

#### 3.3 生产环境
```bash
# 构建生产镜像
docker-compose -f docker-compose.prod.yml build

# 启动生产环境
docker-compose -f docker-compose.prod.yml up -d

# 验证服务
curl http://localhost:8000/health
```

### 4. 代码审查流程

#### 4.1 审查清单
- [ ] 代码符合项目规范
- [ ] 测试用例覆盖核心逻辑
- [ ] 无安全漏洞
- [ ] 性能考虑
- [ ] 文档更新

#### 4.2 审查要点
1. **正确性**：功能是否按需求实现
2. **可读性**：代码是否清晰易懂
3. **可维护性**：是否易于修改和扩展
4. **性能**：是否有性能问题
5. **安全性**：是否有安全漏洞

---

## 代理协作模式

### 1. 并行开发模式
```
前端开发者 ←→ 后端开发者
      ↓           ↓
   UI测试      API测试
      ↓           ↓
   集成测试 ←→ 集成测试
      ↓           ↓
      E2E测试
```

### 2. 代码质量门禁
```
代码提交
    ↓
代码质量代理检查
    ↓
测试代理执行测试
    ↓
部署代理验证环境
    ↓
代码审查
    ↓
合并到主分支
```

### 3. 持续集成流程
```
Git Push
    ↓
GitHub Actions触发
    ↓
构建Docker镜像
    ↓
运行测试套件
    ↓
代码质量检查
    ↓
部署到测试环境
    ↓
通知开发者
```

---

## 配置文件模板

### 1. 环境变量模板 (`.env.example`)
```bash
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/audiobook
DATABASE_TEST_URL=postgresql://user:password@localhost:5432/audiobook_test

# JWT配置
JWT_SECRET_KEY=your-secret-key-here
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# NAS存储配置
STORAGE_TYPE=webdav  # webdav 或 local
WEBDAV_URL=http://nas.local:5005
WEBDAV_USERNAME=admin
WEBDAV_PASSWORD=password
LOCAL_MOUNT_PATH=/mnt/nas/audiobooks

# 应用配置
APP_NAME=AudioBook Player
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO
```

### 2. Docker Compose模板
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/audiobook
    depends_on:
      - db
    volumes:
      - ./backend:/app
      - nas_storage:/mnt/nas

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=audiobook
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
  nas_storage:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /path/to/nas
```

### 3. 代码质量配置
#### Python (`.flake8`)
```ini
[flake8]
max-line-length = 88
extend-ignore = E203
exclude = 
    .git,
    __pycache__,
    .venv,
    alembic/versions
```

#### TypeScript (`.eslintrc.json`)
```json
{
  "extends": [
    "react-app",
    "react-app/jest"
  ],
  "rules": {
    "react/react-in-jsx-scope": "off",
    "import/no-anonymous-default-export": "off"
  }
}
```

---

## 故障排除指南

### 1. 数据库连接问题
```bash
# 检查数据库状态
docker-compose ps db

# 查看数据库日志
docker-compose logs db

# 重启数据库
docker-compose restart db
```

### 2. NAS连接问题
```bash
# 测试WebDAV连接
curl -u username:password http://nas.local:5005/

# 检查本地挂载
ls -la /mnt/nas

# 重新挂载
sudo umount /mnt/nas
sudo mount -t nfs nas:/volume1/audiobooks /mnt/nas
```

### 3. 播放问题
```bash
# 检查音频文件格式
ffprobe /path/to/audio.mp3

# 转换音频格式
ffmpeg -i input.m4a -codec:a libmp3lame output.mp3

# 检查流媒体端点
curl http://localhost:8000/api/content/1/stream
```

---

## 性能优化建议

### 1. 数据库优化
- 为常用查询字段创建索引
- 使用连接池
- 实现查询缓存
- 分页加载大量数据

### 2. 存储优化
- 实现本地缓存
- 使用CDN（可选）
- 压缩音频文件
- 预加载热门内容

### 3. 前端优化
- 代码分割
- 懒加载组件
- 图片优化
- 服务端渲染（可选）

---

## 安全最佳实践

### 1. 密码安全
- 使用bcrypt哈希密码
- 设置最小密码长度（8位）
- 实现密码重置功能
- 记录登录失败尝试

### 2. API安全
- 实现速率限制
- 验证所有输入
- 使用HTTPS
- 实现CORS策略

### 3. 数据安全
- 加密敏感数据
- 定期备份数据库
- 实现访问日志
- 定期安全审计

---

## 监控与日志

### 1. 应用监控
- 健康检查端点：`/health`
- 性能指标：响应时间、错误率
- 资源使用：CPU、内存、磁盘

### 2. 日志配置
```python
# Python日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
```

### 3. 关键日志事件
- 用户登录/登出
- 播放开始/结束
- 时长限制触发
- 管理员操作
- 系统错误

---

## 下一步行动

### 1. 立即开始
1. 初始化项目仓库
2. 设置开发环境
3. 创建基础骨架
4. 实现核心数据模型

### 2. 短期目标（1-2周）
1. 完成阶段0：基础框架搭建
2. 完成阶段1：数据模型和API合约
3. 建立测试框架
4. 配置代码质量工具

### 3. 中期目标（1-2月）
1. 完成存储层和内容导入
2. 实现用户认证和授权
3. 构建播放功能
4. 实现时长限制

### 4. 长期目标（2-3月）
1. 完成前端界面
2. 实现统计功能
3. 完成端到端测试
4. 部署到生产环境

---

## 联系与支持

- **项目文档**：`/docs` 目录
- **问题反馈**：GitHub Issues
- **代码审查**：Pull Requests
- **紧急联系**：项目维护者

---

*本文档最后更新：2026年3月27日*
*版本：1.0.0*
