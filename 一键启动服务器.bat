@echo off
chcp 65001 >nul
title 微信聊天模拟 - 本地服务器 (仅本机127.0.0.1)
cd /d "%~dp0"
echo 正在启动 HTTP 服务器 http://127.0.0.1:8765
echo 访问地址: http://127.0.0.1:8765/index.html
echo.
echo 关闭此窗口即停止服务器。
echo.
start "" "http://127.0.0.1:8765/index.html"
python -m http.server 8765 --bind 127.0.0.1
if errorlevel 1 (
   echo.
   echo [错误] 未找到 Python。请先安装 Python 3: https://www.python.org/downloads/
   echo 安装时务必勾选 "Add Python to PATH"。
   pause
)
