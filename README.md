# Research Writing Skills

为 Codex 项目安装和维护 5 个科研技能。四个通用技能跟踪 [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)；结构生物学审计技能由本仓库维护。本仓库保存上游来源清单和锁定版本，以及自有的结构审计技能；上游技能文件在安装到项目时按需下载，不使用 Git 子模块。

| Skill | 用途 | 来源 |
|---|---|---|
| `scientific-writing` | 以可追溯证据撰写、修订和核查科学论文与报告 | K-Dense-AI `skills/scientific-writing` |
| `paper-lookup` | 从学术数据库检索论文、预印本、引用、开放全文及机构信息 | K-Dense-AI `skills/paper-lookup` |
| `citation-management` | 检索和核验文献元数据，整理引用并生成 BibTeX | K-Dense-AI `skills/citation-management` |
| `peer-review` | 按授权和保密要求开展有证据依据的同行评审 | K-Dense-AI `skills/peer-review` |
| `structural-biology-audit` | 审计 cryo-EM、X-ray 及结构推断的证据是否支持具体主张 | 本仓库 `skills/structural-biology-audit` |

四个上游 Skill 的科学规则与提示词以原文为准；管理工具按锁文件提取每项 Skill 所需的文件，不会复制整个上游仓库。`sources.json` 跟踪上游 `main`，`upstreams.lock.json` 记录当前固定提交 `65d6e786832e2c52832713117bbbf5096b56f77f` 和文件校验值。

## 安装

需要 Python 3.11 或更新版本，以及联网访问 GitHub 和 Python 包索引。安装器会在目标项目的 `.agents/skills/` 安装五项技能，并在 `.agents/research-writing-skills/` 创建隔离运行环境，安装 `requests` 和 `PyYAML`。如果有 `uv`，安装器优先使用它；没有时使用 Python 自带的 `venv` 和 `pip`。Google Scholar 专用的 `scholarly` 包为可选项，默认不安装。

安装器会在项目 `AGENTS.md` 中加入一段带标记的环境指引，告诉 Codex 使用本项目解释器，保留文件中其余文字。科学规则、上游提示词和辅助文件均保持原文。项目运行环境的位置和用途也记录在 `.agents/research-writing-skills/ENVIRONMENT.md`。

```bash
git clone https://github.com/Jaaayden/research-writing-skills.git
cd research-writing-skills
python3 scripts/manage.py install --project "/path/to/My Research Project"
python3 scripts/manage.py check --project "/path/to/My Research Project"
```

将 `--project` 的路径替换为目标项目的绝对路径；带空格的路径要用引号括起。Windows PowerShell 示例使用 `python` 命令：

```powershell
git clone https://github.com/Jaaayden/research-writing-skills.git
cd research-writing-skills
python scripts/manage.py install --project "C:\Users\you\My Research Project"
python scripts/manage.py check --project "C:\Users\you\My Research Project"
```

`check` 会核对目标项目的安装状态。未知同名技能、已安装技能的手动修改、受管环境指引或许可证的修改都会使安装或卸载停止，保留原内容。相同版本重复安装会跳过下载和重建环境。`run` 使用目标项目中隔离环境里的依赖运行 Skill 脚本：

```bash
python3 scripts/manage.py run --project "/path/to/My Research Project" paper-lookup scripts/paginate.py --help
```

不再需要时，可移除管理工具安装的技能：

```bash
python3 scripts/manage.py uninstall --project "/path/to/My Research Project"
```

卸载会移除此工具创建的 Python 环境，包括后来加入的可选包；其他技能和 `AGENTS.md` 中用户自己的指令会保留。未受管内容放入运行目录后，工具会停止卸载，便于先将它们移出。

## 更新与维护

本仓库代码与上游 Skill 内容是两件事：`git pull` 更新本仓库的管理工具和清单；`manage.py update` 按清单从上游 `main` 获取 Skill 更新并刷新锁定提交。预览后再更新，并重新安装到目标项目：

```bash
# 获取本仓库的管理工具和清单更新
git pull --ff-only

# 预览上游 main 更新会带来的变化
python3 scripts/manage.py update --dry-run

# 刷新上游内容和锁文件，再安装至目标项目
python3 scripts/manage.py update
python3 scripts/manage.py install --project "/path/to/My Research Project"
python3 scripts/manage.py check --project "/path/to/My Research Project"
```

需要获取上游最新 `main` 时才运行 `update`；只拉取本仓库代码不会自动更新上游 Skill。不要手工编辑锁文件来代替上游更新。更新完成后提交 `upstreams.lock.json`，其他设备便可复现同一个版本。`structural-biology-audit` 是本仓库的自有技能，今后直接在 `skills/structural-biology-audit/` 修改并提交；该目录是它唯一的维护源。

若上游引入新的 Python 包、移走必要资源或更改许可证，工具会明确停止，等待维护者调整依赖锁或核对许可。它不会自动安装未经声明的科研软件。

## API 密钥与邮箱

通常检索无需 API 密钥。下表区分“使用某个服务时必须”与“使用整个技能组必须”：整体安装和常见检索都不要求这些密钥。若配置，只为相应服务设置；不要将密钥、真实邮箱或 `.env` 文件提交到公开仓库。

| 名称 | 用途 | 使用该服务时是否必需 | 未配置时仍可用 |
|---|---|---|---|
| `NCBI_API_KEY` | 提高 PubMed/PMC Entrez 请求速率 | 否 | PubMed 和 PMC 仍可按较低速率检索 |
| `CORE_API_KEY` | 访问 CORE 全文服务 | 仅 CORE 全文需要 | 其他文献源、元数据检索及本地处理仍可用 |
| `S2_API_KEY` | Semantic Scholar API 认证并改善受限时的访问 | 否 | 可使用共享速率池；也可改用其他学术数据库 |
| `OPENALEX_API_KEY` | OpenAlex API 的较高访问额度 | 否，建议配置 | 仍可使用其他开放数据库；OpenAlex 可用范围和速率依其接口政策 |
| `NCBI_EMAIL` | 向 NCBI 标识 Entrez 请求方 | 否，建议配置 | PubMed/PMC 的一般检索仍可用 |
| `OPENALEX_EMAIL` | 向 OpenAlex 提供联系标识；邮箱不能代替 API key | 否 | OpenAlex 公共查询仍可用 |
| `CROSSREF_MAILTO` | 加入 Crossref 的 polite pool | 否 | Crossref 仍可在公共速率池查询 |
| Unpaywall `email` 参数 | 查询 DOI 的开放获取状态和合法全文位置 | 使用 Unpaywall 时需要真实邮箱；它是请求参数，不是本工具读取的环境变量 | 其他数据库检索与文献管理功能仍可用 |

`citation-management` 当前的 OpenAlex 脚本读取邮箱但不能传入 `OPENALEX_API_KEY`；需要更高额度的调用可用 `paper-lookup` 提供的 API 方式。Google Scholar 分支需要额外安装 `scholarly`，未配置时其余检索、BibTeX 整理和本地核验仍可用。安装器不会读取 `.env` 或收集 API key。

`structural-biology-audit` 的完整 PDF 定位功能可读取 Zotero Desktop 已有的附件。使用该功能时，需要启动 Zotero，并在设置中启用本地 API；只读访问无需 API key，也无需额外环境变量。安装器不安装或修改 Zotero。未配置 Zotero 时，审计指南、来源索引与 DOI 检索仍可用；也可自行准备技能 `full-text/` 目录中的完整本地 PDF。PDF 不随公开仓库或默认安装分发。

## 许可

上游 Skill 文件保留其 MIT 许可和来源信息，许可文本见 [`licenses/K-Dense-AI-MIT.md`](licenses/K-Dense-AI-MIT.md)。本仓库自有管理代码和 `structural-biology-audit` 按根目录 [`LICENSE`](LICENSE) 中的 MIT 许可发布。请勿将私人凭据或个人环境配置迁入本仓库。

## 验证

2026-09-30 在 macOS 上验证：16 项安装器行为测试通过；真实下载、带空格路径的项目安装、重复安装、隔离环境调用及卸载通过。安装后的 5 个 Skill 均由桌面应用随附 Codex 的 `skills/list(forceReload=true)` 识别为已启用的项目技能，加载错误为 0；26 个上游脚本入口检查通过。上游文件与锁定提交的 Git blob 和 SHA-256 摘要一致。源目录中的可选 `full-text/`、Python 缓存和 `.DS_Store` 不会随安装复制；目标中用户后来加入的文件仍受覆盖和卸载保护。

四个上游 Skill 的 339 项原始行为检查也已通过（网络响应使用 fixtures/mock）；这些结果不代表所有学术 API 均已联网验证。仓库 CI 在 Python 3.11 和 3.14 上运行安装器行为测试。Windows 的命令和路径处理已按平台分支编写，尚未在 Windows 实机安装。
