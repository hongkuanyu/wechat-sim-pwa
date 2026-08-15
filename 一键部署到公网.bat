@echo off
chcp 65001 >nul
title 微信聊天模拟 - 一键部署到公网
cd /d "%~dp0"
python "部署到GitHub.py"
if errorlevel 1 (
   echo.
   echo [错误] 未找到 Python。请先安装 Python 3:
   echo        https://www.python.org/downloads/
   echo        安装时勾选 "Add Python to PATH"
   pause
)
