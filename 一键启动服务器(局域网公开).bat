@echo off
chcp 65001 >nul
title 微信聊天模拟 - 局域网服务器 (手机也能连)
cd /d "%~dp0"

echo ========================================================
echo   局域网公开模式 - 请确保手机和电脑在同一 WiFi
echo ========================================================
echo.
echo 本机所有 IPv4 地址:
echo --------------------------------------------------------
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
   for /f "tokens=* delims= " %%b in ("%%a") do (
      echo     手机浏览器打开:  http://%%b:8765/index.html
   )
)
echo --------------------------------------------------------
echo.
echo 提示：若 Windows 弹出防火墙提示，请勾选 "专用网络" 并允许。
echo 关闭此窗口即停止服务器。
echo.
echo 正在启动 http://0.0.0.0:8765 ...
python -m http.server 8765 --bind 0.0.0.0
if errorlevel 1 (
   echo.
   echo [错误] 未找到 Python。请先安装 Python 3 并勾选 "Add Python to PATH"：
   echo        https://www.python.org/downloads/
   pause
)
