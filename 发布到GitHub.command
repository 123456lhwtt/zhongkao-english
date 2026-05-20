#!/bin/zsh
set -e

SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"
DEPLOY_DIR="$HOME/Desktop/中考冲刺战-英语-发布包"
REMOTE_URL="https://github.com/123456lhwtt/zhongkao-english.git"

echo "正在准备发布包..."
rm -rf "$DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR"

rsync -a \
  --exclude='.DS_Store' \
  --exclude='.git' \
  --exclude='化学/' \
  --exclude='数学/' \
  --exclude='物理/' \
  --exclude='英语二模/' \
  --exclude='微信图片_*' \
  --exclude='Untitled.docx' \
  --exclude='副本中考英语复习1.xlsx' \
  "$SOURCE_DIR/" "$DEPLOY_DIR/"

cd "$DEPLOY_DIR"

if [ ! -d ".git" ]; then
  git init -b main
fi

git remote remove origin 2>/dev/null || true
git remote add origin "$REMOTE_URL"

git add .
git commit -m "Deploy 中考冲刺战-英语" || true
git push -u origin main

echo ""
echo "推送完成。"
echo "接下来打开 GitHub 仓库 Settings → Pages，Source 选择 Deploy from a branch，Branch 选择 main / root，然后保存。"
echo "网站地址通常是：https://123456lhwtt.github.io/zhongkao-english/"
read -k 1 "?按任意键关闭..."
