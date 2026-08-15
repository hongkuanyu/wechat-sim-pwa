@echo off
chcp 65001 >nul
title 微信聊天模拟 - 一键安装
cd /d "%~dp0"

echo ========================================================
echo   微信聊天模拟 - 一键安装
echo ========================================================
echo.
echo   桌面电脑：浏览器已自动打开，点页面顶部绿色「安装」按钮
echo.
echo   手机安装（2步）：
echo   1. 用手机浏览器扫描页面右下角弹出的二维码
echo   2. 打开后点页面顶部「安装」按钮（安卓）/ 分享→添加到主屏幕（苹果）
echo.
echo   --------------------------------------------------------
echo   本机局域网 IP（手机和电脑需连同一 WiFi）：
echo   --------------------------------------------------------
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
   for /f "tokens=* delims= " %%b in ("%%a") do (
      echo     http://%%b:8765/index.html
   )
)
echo   --------------------------------------------------------
echo.
echo   关闭此窗口即停止服务器。
echo.
echo   若 Windows 弹出防火墙提示，请勾选「专用网络」并允许。
echo.

start "" "http://127.0.0.1:8765/index.html"
python -m http.server 8765 --bind 0.0.0.0
if errorlevel 1 (
   echo.
   echo [错误] 未找到 Python。请先安装 Python 3 并勾选 "Add Python to PATH"：
   echo        https://www.python.org/downloads/
   pause
)
