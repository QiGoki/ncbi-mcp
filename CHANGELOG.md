# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.4] - 2026-01-09

### Changed
- 修复模块导入问题，将目录名从 `ncbi-mcp` 改为 `ncbi_mcp` 以符合 Python 命名规范
- 更新 server.py 中的导入语句为相对导入
- 修复 pyproject.toml 中的脚本入口点配置

### Added
- 创建 pyproject.toml 配置文件，支持现代 Python 构建系统

## [0.1.3] - 2026-01-09

### Added
- 初始版本发布
- 实现 NCBI E-utilities MCP 服务器
- 支持 EInfo、ESearch、ESummary、EFetch 工具
