## 🧠 一份總結：如何在「機器人開發電腦」與 GitHub 同步、並與他人協作


### ✅ 第一次設定：開發電腦（例如樹莓派、Jetson Nano）

```bash
# 進入你的專案資料夾
cd ~/thur_car

# 確認是否為 Git 專案，否則初始化
git init

# 加入 GitHub 遠端倉庫（已存在）
git remote add origin git@github.com:lego1002/Thur_car.git

# 第一次提交（如果還沒 commit 過）
git add .
git commit -m "Initial commit"

# 若 GitHub repo 是空的（沒 commit），直接推送：
git push -u origin main

# 若 GitHub 上已有 commit，請先拉下來避免衝突：
git pull origin main --allow-unrelated-histories
# 處理衝突後：
git push origin main
```

---

### 🧍‍♂️ 你自己在另一台筆電繼續開發（或新電腦）

```bash
git clone git@github.com:lego1002/Thur_car.git
cd Thur_car

# 開發流程
git add .
git commit -m "新增 XXX 功能"
git push origin main
```

---

### 🤝 協作者（你已邀請他加入 GitHub repo）

1. 登入 GitHub 接受邀請。
2. 在自己電腦上執行：

```bash
git clone git@github.com:lego1002/Thur_car.git
cd Thur_car

# 編輯程式後：
git add .
git commit -m "我做了某某功能"
git push origin main
```

---

### 🧯 常見錯誤處理

| 問題 | 解法 |
|------|------|
| push 出現 `non-fast-forward` 錯誤 | `git pull origin main` 再 push |
| 權限錯誤（403、permission denied） | 確認 GitHub 帳號、已接受邀請、設好 SSH |
| 別人也有 push，內容有衝突 | `git pull` → 手動解衝突 → `git add .` → `git commit` → `git push` |

---

### 📁 進階推薦（多人開發最佳實踐）

- ✅ 每人用自己的 branch 開發：
  ```bash
  git checkout -b feature/sensor-integration
  ```
- ✅ 合併用 Pull Request（可審查）
- ✅ 主要分支（main）要穩定可用

