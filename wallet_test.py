# 【Scent-ID 專案中心】
# 檔案名稱：D:\Jay_AI\vault_manager.py
# 版本編號：V.4.2.2
# 核心任務：自動化監控 .env 檔案參數數量 (40項)

import os
from dotenv import load_dotenv

def initialize_vault():
    load_dotenv()
    print("--- 🔐 Jay AI 密鑰保險箱啟動 ---")
    
    if not os.path.exists('.env'):
        print("❌ 錯誤：找不到 .env 檔案！")
        return

    try:
        with open('.env', 'r', encoding='utf-8') as f:
            count = sum(1 for line in f if line.strip().startswith('['))
        
        print(f"系統檢查：當前載入參數總量為 [{count}/40]")
        
        if count < 40:
            print(f"⚠️ 警告：參數不足 40，請檢查 .env。")
        else:
            print("✅ 完整性驗證通過。")
    except Exception as e:
        print(f"❌ 讀取錯誤：{e}")

if __name__ == "__main__":
    initialize_vault()