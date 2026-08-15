# 微信聊天 PWA

这是一个单文件的微信聊天模拟 PWA（演示用）。已完成：

- PWA manifest（`manifest.webmanifest`）— 使用真实 PNG 图标（非 SVG data URL）
- Service Worker（`sw.js`）及离线回退页（`offline.html`）— 三级缓存回退策略
- 安装横幅与二维码面板逻辑已集成在 `index.html`
- 多尺寸 PNG 图标（72~512px）+ maskable 自适应图标，兼容 iOS/安卓
- iOS 专用 apple-touch-icon（PNG）、apple-mobile-web-app-capable 等 meta 标签

快速部署与测试：

1. 在本地临时测试（开发机需运行一次，手机通过同一局域网访问）：

```bash
# 在项目目录运行本地静态服务器
python -m http.server 8000
```

在手机浏览器中访问 `http://<电脑局域网IP>:8000/`。

2. 推荐线上部署（支持 HTTPS，安装体验更好）
- 使用 GitHub Pages / Netlify /Vercel 等托管服务直接部署整个文件夹。

快速一键推送到你自己的 GitHub 仓库（Windows）：

1) 在 GitHub 网站创建一个空仓库（记下仓库 HTTPS 地址，例如 `https://github.com/yourname/wechat-sim-pwa.git`）
2) 在项目目录运行：

```powershell
publish_to_github.bat https://github.com/yourname/wechat-sim-pwa.git
```

这会把 `main` 与 `gh-pages` 分支推送到远端；然后在仓库设置里启用 GitHub Pages，选择 `gh-pages` 分支作为发布源。

3. 在手机上安装与验证：
- Android（Chrome/Edge）：打开页面后点击横幅或浏览器菜单 → “安装应用”
- iOS（Safari）：打开页面后点击分享 → “添加到主屏幕”

4. 离线验证：
- 首次在线访问页面后，断开网络并刷新页面；若已缓存，页面应能打开或显示 `offline.html` 回退页。

已知限制：
- iOS 不支持自动安装提示（`beforeinstallprompt`），只能手动“添加到主屏幕”。
- 首次访问必须联网以缓存资源并注册 Service Worker；无法实现“完全一步在离线下安装”。

如果需要，我可以：
- 生成多尺寸的真实 PNG 图标并将它们写入项目以进一步提升 iOS 体验（我可以直接生成并添加）。
- 帮你把项目自动部署到 GitHub Pages（需要你提供仓库或允许我创建）。

直接告诉我你希望我继续执行哪项（我会自动开始并完成）。
