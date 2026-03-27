# 内容导入管道设计

## 概述

内容导入管道负责从NAS存储中扫描、提取元数据并导入有声书内容到数据库。

## 设计目标

1. **高效扫描**：快速扫描NAS目录结构
2. **准确元数据**：提取准确的音频元数据（标题、作者、时长等）
3. **增量更新**：支持增量导入，只处理新文件或修改过的文件
4. **错误恢复**：处理网络中断、文件损坏等异常情况
5. **可扩展性**：支持多种音频格式和存储后端

## 架构设计

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   扫描器        │    │   元数据提取器   │    │   数据库写入器   │
│   (Scanner)     │───▶│   (Metadata)    │───▶│   (Persister)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   文件队列      │    │   元数据队列    │    │   批量写入      │
│   (File Queue)  │    │   (Meta Queue)  │    │   (Batch Write) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 组件设计

### 1. 扫描器 (Scanner)

**职责**：
- 递归扫描NAS目录
- 识别音频文件
- 提取文件基本信息（路径、大小、修改时间）

**接口**：
```python
class Scanner:
    def scan_directory(self, path: str) -> List[ScanResult]
    def scan_incremental(self, path: str, last_scan_time: datetime) -> List[ScanResult]
```

**音频文件识别**：
- 文件扩展名：`.mp3`, `.m4a`, `.m4b`, `.flac`, `.ogg`, `.wav`, `.aac`
- MIME类型检测：`audio/*`

### 2. 元数据提取器 (MetadataExtractor)

**职责**：
- 从音频文件提取元数据
- 支持多种音频格式
- 提取封面图片

**接口**：
```python
class MetadataExtractor:
    def extract(self, file_path: str, file_data: bytes) -> AudioMetadata
    def extract_cover(self, file_path: str, file_data: bytes) -> Optional[bytes]
```

**支持的元数据字段**：
- 标题 (title)
- 作者 (artist/author)
- 专辑 (album)
- 时长 (duration)
- 格式 (format)
- 比特率 (bitrate)
- 采样率 (sample_rate)
- 封面 (cover_art)

### 3. 数据库写入器 (Persister)

**职责**：
- 将元数据写入数据库
- 创建或更新Content和Folder记录
- 处理文件移动和重命名

**接口**：
```python
class Persister:
    def persist_content(self, metadata: AudioMetadata) -> Content
    def persist_folder(self, folder_path: str) -> Folder
    def cleanup_deleted_files(self, current_files: List[str]) -> int
```

### 4. 导入管道 (IngestionPipeline)

**职责**：
- 协调扫描、元数据提取和数据库写入
- 管理导入进度
- 处理错误和重试

**接口**：
```python
class IngestionPipeline:
    def run_full_import(self, root_path: str) -> ImportResult
    def run_incremental_import(self, root_path: str) -> ImportResult
    def get_progress(self) -> ImportProgress
```

## 数据流

### 完整导入流程

```
1. 开始导入
   ↓
2. 扫描根目录
   ↓
3. 识别音频文件
   ↓
4. 提取元数据
   ↓
5. 写入数据库
   ↓
6. 更新进度
   ↓
7. 重复3-6直到完成
   ↓
8. 清理已删除文件
   ↓
9. 完成导入
```

### 增量导入流程

```
1. 开始增量导入
   ↓
2. 获取上次扫描时间
   ↓
3. 扫描目录（只检查修改时间 > 上次扫描时间）
   ↓
4. 识别新文件和修改过的文件
   ↓
5. 提取元数据
   ↓
6. 更新数据库
   ↓
7. 完成增量导入
```

## 错误处理

### 网络错误
- **策略**：指数退避重试
- **最大重试次数**：3次
- **重试间隔**：1s, 2s, 4s

### 文件损坏
- **策略**：跳过损坏文件，记录错误日志
- **恢复**：下次导入时重新尝试

### 数据库错误
- **策略**：事务回滚，重试当前批次
- **批次大小**：100条记录

### 元数据提取错误
- **策略**：使用默认值，记录警告日志
- **默认值**：
  - 标题：文件名（不含扩展名）
  - 作者：未知
  - 时长：0

## 性能优化

### 批量处理
- **批次大小**：100条记录
- **并行处理**：最多4个并发任务

### 缓存策略
- **文件哈希缓存**：避免重复计算
- **元数据缓存**：缓存提取结果

### 内存管理
- **流式处理**：大文件分块读取
- **及时释放**：处理完立即释放内存

## 配置参数

```python
# 导入配置
INGESTION_BATCH_SIZE = 100
INGESTION_MAX_WORKERS = 4
INGESTION_RETRY_COUNT = 3
INGESTION_RETRY_DELAY = 1  # 秒

# 扫描配置
SCAN_RECURSIVE = True
SCAN_FOLLOW_SYMLINKS = False
SCAN_INCLUDE_HIDDEN = False

# 元数据配置
METADATA_EXTRACT_TIMEOUT = 30  # 秒
METADATA_CACHE_TTL = 3600  # 秒
```

## 监控和日志

### 关键指标
- 扫描文件数量
- 导入成功数量
- 导入失败数量
- 处理时间
- 内存使用情况

### 日志级别
- **DEBUG**：详细的处理信息
- **INFO**：导入进度和结果
- **WARNING**：可恢复的错误
- **ERROR**：不可恢复的错误

## 扩展点

### 新格式支持
- 实现新的元数据提取器
- 注册到格式工厂

### 新存储后端
- 实现存储接口
- 注册到存储工厂

### 自定义元数据映射
- 配置字段映射规则
- 支持自定义元数据字段

## 测试策略

### 单元测试
- 扫描器测试
- 元数据提取器测试
- 数据库写入器测试

### 集成测试
- 完整导入流程测试
- 增量导入测试
- 错误恢复测试

### 性能测试
- 大目录扫描测试
- 并发导入测试
- 内存使用测试