# VPN Ruleset

个人代理规则聚合与多客户端订阅服务

## 快速开始

### 1. 配置机场订阅

在 GitHub 仓库 Settings → Secrets and variables → Actions 中添加：

- Name: `CLASH_SUB`
- Value: 你的机场 Clash 订阅地址

### 2. 运行 GitHub Actions

- 方式一：等待每天 00:00 自动运行
- 方式二：手动触发 Actions → Build Rules → Run workflow

### 3. 订阅生成的配置

运行成功后，使用以下地址订阅：

**Clash**:
```
https://raw.githubusercontent.com/<你的用户名>/<仓库名>/main/output/clash.yaml
```

**Shadowrocket**:
```
https://raw.githubusercontent.com/<你的用户名>/<仓库名>/main/output/shadowrocket.conf
```

## 自定义规则

编辑 `ruleset/` 目录下的文件来添加你的规则：

- [proxy.yaml](ruleset/proxy.yaml) - 走代理的规则
- [direct.yaml](ruleset/direct.yaml) - 直连的规则
- [reject.yaml](ruleset/reject.yaml) - 拒绝的规则

### 规则格式

```yaml
rules:
  - type: domain-suffix
    value: openai.com
    policy: proxy
  - type: geoip
    value: CN
    policy: direct
```

**支持的类型**：
- `domain` - 完整域名匹配
- `domain-suffix` - 域名后缀匹配
- `ip-cidr` - IP 段匹配
- `geoip` - 地理位置匹配

**支持的策略**：
- `proxy` - 走代理
- `direct` - 直连
- `reject` - 拒绝

## 工作原理

1. GitHub Actions 定时拉取机场订阅
2. 解析机场配置（保留节点和原始规则）
3. 将你的自定义规则添加到最前面（优先级更高）
4. 分别生成 Clash 和 Shadowrocket 配置
5. 提交到仓库供订阅使用

## 项目结构

```
ruleset/                  # 逻辑规则源（唯一维护点）
  ├── proxy.yaml
  ├── direct.yaml
  └── reject.yaml

generators/               # 规则生成器
  ├── gen_clash.py
  └── gen_shadowrocket.py

scripts/                  # 辅助脚本
  └── fetch_clash.py

output/                   # 生成的配置文件
  ├── clash.yaml
  └── shadowrocket.conf

.github/workflows/
  └── build.yml          # 自动化流程
```
