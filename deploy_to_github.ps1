<#
  部署到 GitHub Pages 的辅助脚本（Windows PowerShell）
  - 在项目目录初始化 git（若尚未初始化）
  - 提交当前代码为 initial commit
  - 创建 gh-pages 分支
  - 若安装了 GitHub CLI (`gh`)，尝试创建远端仓库并推送分支并启用 Pages
  - 若未安装 `gh`，会输出需要手动执行的命令
#>
Set-StrictMode -Version Latest
cd (Split-Path -Parent $MyInvocation.MyCommand.Definition)

function Exec([string]$cmd){ Write-Host "> $cmd"; iex $cmd }

# repo name based on folder name
$folder = Split-Path -Leaf (Get-Location)
$repoName = ($folder -replace "[^0-9a-zA-Z._-]","-")

if (-not (Test-Path ".git")){
  Exec "git init"
} else { Write-Host "git already initialized" }

Exec "git add -A"
try{ Exec "git commit -m \"Initial: PWA app (manifest, sw, icons)\"" } catch { Write-Host "No changes to commit or commit failed: $_" }

Exec "git branch -M main"
Exec "git checkout -B gh-pages"

# Try to use gh CLI
if (Get-Command gh -ErrorAction SilentlyContinue){
  Write-Host "Found gh CLI — attempting to create GitHub repo and push..."
  try{
    Exec "gh repo create $repoName --public --source . --remote origin --confirm"
    Exec "git push -u origin main"
    Exec "git push -u origin gh-pages"
    # enable pages to use gh-pages
    $ownerRepo = gh repo view --json nameWithOwner -q .
    if ($ownerRepo){
      $parts = $ownerRepo -split "/"
      $owner = $parts[0]; $repo = $parts[1]
      Write-Host "Enabling GitHub Pages (gh-pages branch)..."
      gh api --method PUT "/repos/$owner/$repo/pages" -f "source.branch=gh-pages" -f "source.path=/"
      Write-Host "Deployment attempted. If no errors, visit: https://$owner.github.io/$repo/"
    }
  } catch {
    Write-Host "gh CLI flow failed: $_"; Write-Host "You can push manually using the commands printed below.";
  }
} else {
  Write-Host "gh CLI not found. To publish, run these commands manually after creating a GitHub repo and adding it as remote origin:"
  Write-Host "git remote add origin https://github.com/<your-username>/$repoName.git"
  Write-Host "git push -u origin main"
  Write-Host "git push -u origin gh-pages"
  Write-Host "Then enable GitHub Pages in repo settings (branch: gh-pages, folder: /) or use GitHub Pages UI."
}

Write-Host "Done. If you want me to try creating the remote repository automatically, ensure the GitHub CLI 'gh' is installed and authenticated (run 'gh auth login')."
