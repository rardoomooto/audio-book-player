# 编码规范指南

本文档规范 Python、TypeScript/React、Git 提交以及代码审查等方面，确保代码质量和可维护性。

## 1. Python 编码规范
- 遵循 PEP 8：命名、缩进、行长等。
- 使用类型提示（Type Hints）提升静态可读性，必要处添加 Docstring。
- 函数/方法要有明确的入参与返回值注释，类和模块要有简要描述。
- 导入分组：标准库、第三方库、本地应用，按空行分组；使用 isort 排序。
- 使用 Black 格式化代码，确保统一风格。
- 测试优先，尽量覆盖边界情况。

### 代码组织
- backend/：业务逻辑、模型、API、测试
- frontend/：前端应用、共享组件、API 客户端
- infra/：部署脚本、配置、CI 集成

## 2. TypeScript/React 编码规范
- 使用 TypeScript 的类型系统，避免 any 的滥用。
- 使用 ESLint + Prettier 统一风格，确保可读性与一致性。
- 组件采用函数组件（React.FC 不强制）并使用 React  hooks。
- 组件的 props 使用精确的类型定义，避免隐式 any。
- 路由与状态管理保持清晰的边界，避免全局污染。
- 测试优先或紧随实现，单元测试覆盖核心逻辑。

## 3. Git 提交规范
- 提交类型前缀：feat | fix | docs | style | refactor | test | chore
- 提交主题采用短语式描述（小于 72 字符为宜）
- 提交信息要解释“为何改变”，而非仅仅描述“做了什么”。
- Test files 应该与实现代码放在同一提交中。
- 遵循原子性原则：尽量一个提交只改动一个较小的、可回滚的点。

示例:
feat(auth): add JWT login endpoint

fix(storage): handle WebDAV timeout gracefully

## 4. 代码审查清单
- 需求实现是否正确、完整。
- 代码可读性、变量命名、注释是否清晰。
- 安全性与输入校验是否到位。
- 性能考虑：数据库查询、缓存、并发等。
- 测试覆盖率是否符合目标。
- 文档和注释是否同步更新。
