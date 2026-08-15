# -*- coding: utf-8 -*-
"""
微信聊天模拟 PWA - 一键部署到 GitHub Pages
运行后会自动创建 GitHub 仓库、上传文件、启用 Pages
部署完成后获得公网 HTTPS 网址，手机浏览器直接访问即可安装
"""
import os, sys, json, base64, time, urllib.request, urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_NAME = "wechat-sim-pwa"
FILES_TO_UPLOAD = ["index.html", "manifest.webmanifest", "sw.js"]

def api_call(method, url, token, data=None):
    """调用 GitHub API"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "PWA-Deploy-Script"
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8")) if resp.read else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.read else ""
        return {"error": e.code, "message": err_body}
    except Exception as e:
        return {"error": str(e)}

def upload_file(token, owner, repo, path, content):
    """上传单个文件到 GitHub"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    data = {
        "message": f"Upload {path}",
        "content": base64.b64encode(content).decode("utf-8"),
        "branch": "main"
    }
    result = api_call("PUT", url, token, data)
    return result

def main():
    print("=" * 60)
    print("  微信聊天模拟 PWA - 一键部署到 GitHub Pages")
    print("=" * 60)
    print()
    print("  部署完成后，手机浏览器直接访问网址即可安装应用")
    print("  无需电脑、无需局域网、任何网络下都能用")
    print()
    print("-" * 60)
    print()
    print("  请先在 GitHub 上创建 Personal Access Token：")
    print("  1. 打开 https://github.com/settings/tokens")
    print("  2. 点「Generate new token (classic)」")
    print("  3. Note 填: pwa-deploy")
    print("  4. Expiration 选: 7 days")
    print("  5. 勾选「repo」权限（第一个大选项）")
    print("  6. 点底部「Generate token」")
    print("  7. 复制生成的 token（只显示一次！）")
    print()
    print("-" * 60)
    print()

    username = input("请输入你的 GitHub 用户名: ").strip()
    if not username:
        print("用户名不能为空！"); return
    token = input("请粘贴你的 Token: ").strip()
    if not token:
        print("Token 不能为空！"); return

    print()
    print("=" * 60)
    print("  开始部署...")
    print("=" * 60)

    # 1. 创建仓库
    print("\n[1/4] 创建 GitHub 仓库...")
    result = api_call("POST", "https://api.github.com/user/repos", token, {
        "name": REPO_NAME,
        "description": "微信聊天模拟 PWA",
        "private": False,
        "auto_init": False
    })
    if "error" in result:
        if result.get("error") == 422:
            print(f"  仓库 {REPO_NAME} 已存在，继续上传文件...")
        else:
            print(f"  创建仓库失败: {result.get('message', '未知错误')}")
            return
    else:
        print(f"  仓库创建成功: https://github.com/{username}/{REPO_NAME}")

    # 等待仓库初始化
    time.sleep(2)

    # 2. 上传文件
    print("\n[2/4] 上传文件...")
    for fname in FILES_TO_UPLOAD:
        fpath = os.path.join(SCRIPT_DIR, fname)
        if not os.path.exists(fpath):
            print(f"  警告: {fname} 不存在，跳过")
            continue
        with open(fpath, "rb") as f:
            content = f.read()
        print(f"  上传 {fname} ({len(content)} bytes)...", end=" ")
        r = upload_file(token, username, REPO_NAME, fname, content)
        if "error" in r and r["error"] != 422:
            # 可能文件已存在，尝试更新
            if r.get("error") == 422:
                # 获取当前文件的 sha
                sha_url = f"https://api.github.com/repos/{username}/{REPO_NAME}/contents/{fname}"
                sha_result = api_call("GET", sha_url, token)
                if "sha" in sha_result:
                    data = {
                        "message": f"Update {fname}",
                        "content": base64.b64encode(content).decode("utf-8"),
                        "sha": sha_result["sha"],
                        "branch": "main"
                    }
                    r2 = api_call("PUT", sha_url, token, data)
                    if "error" not in r2:
                        print("更新成功")
                    else:
                        print(f"失败: {r2.get('message','')}")
                else:
                    print(f"无法获取 sha")
            else:
                print(f"失败: {r.get('message','')}")
        else:
            print("成功")

    # 3. 等待仓库处理
    print("\n[3/4] 等待仓库处理...")
    time.sleep(3)

    # 4. 启用 GitHub Pages
    print("\n[4/4] 启用 GitHub Pages...")
    pages_url = f"https://api.github.com/repos/{username}/{REPO_NAME}/pages"
    # 先检查是否已启用
    check = api_call("GET", pages_url, token)
    if "error" not in check:
        print("  Pages 已启用")
    else:
        result = api_call("POST", pages_url, token, {
            "source": {"branch": "main", "path": "/"}
        })
        if "error" in result:
            print(f"  启用 Pages 失败: {result.get('message','')}")
            print("  请手动到仓库 Settings → Pages 启用")
        else:
            print("  Pages 启用成功！")

    # 最终 URL
    final_url = f"https://{username}.github.io/{REPO_NAME}/"
    print()
    print("=" * 60)
    print("  部署完成！")
    print("=" * 60)
    print()
    print(f"  你的应用网址（手机浏览器直接访问）：")
    print()
    print(f"    {final_url}")
    print()
    print("  安装方法：")
    print("  安卓：Chrome 打开网址 → 点顶部「安装」按钮")
    print("  苹果：Safari 打开网址 → 分享 → 添加到主屏幕")
    print()
    print("  Pages 首次启用需要等 1-2 分钟生效，")
    print("  如果打开是 404，等一会儿再刷新。")
    print()
    print(f"  仓库地址: https://github.com/{username}/{REPO_NAME}")
    print("=" * 60)
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()
