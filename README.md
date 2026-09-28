# Vendor Keynote Insights

用于从用户指定的发布会视频、讲解词和官网资料形成有证据支撑的洞察演示文稿。

## 输入

- 必选：发布会讲解词、核心问题及每个问题的大约页数。
- 视频来源建议由用户指定 B 站链接；官网来源由用户指定产品页、新闻通稿等网址。
- 读者受众与视觉风格可选；未指定色彩时默认浅色背景。

## 工作流

完整的用户提示词与交接步骤见 [协作工作流](vendor-keynote-insights_%E5%8D%8F%E4%BD%9C%E5%B7%A5%E4%BD%9C%E6%B5%81.md)。

1. 创建同一份 `Storyboard_Manifest.md` 的逐页草稿，供用户审阅。
2. 用户批准指定版本后，调用 [Storyboard Governance](https://github.com/lwyjames/presentation-storyboard-governance) 记录批准状态并校验稳定页 ID。
3. 按事先要求制作 HTML／PPTX／PDF 等格式，并逐页检查内容、素材裁切和排版。

在 ChatGPT 中可使用 `@vendor-keynote-insights` 作为用户入口。本仓库存放 skill 源文件；GitHub 版本与已安装的个人 skill 需分别维护和同步。
