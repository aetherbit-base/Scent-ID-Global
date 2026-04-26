# 【Scent-ID 專案中心】
# 檔案名稱：D:\Jay_AI\vault_manager.py
# 版本編號：V.4.2.3 (正式運轉版)
# 核心任務：確認 40 個參數完整性並啟動保險箱

import os
from dotenv import load_dotenv

def initialize_vault():
    load_dotenv()
    print("="*50)
    print("--- 🔐 Jay AI 密鑰保險箱：狀態檢核 ---")
    print("="*50)
    
    if not os.path.exists('.env'):
        print("❌ 錯誤：找不到 .env 檔案，請檢查路徑！")
        return

    try:
        # 計算以 [ 開頭的行數
        with open('.env', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            count = sum(1 for line in lines if line.strip().startswith('['))
        
        print(f"📈 參數載入進度：[{count}/40]")
        
        if count == 40:
            print("✅ 完美！所有 40 個 API 與錢包參數均已就位。")
            print("🚀 系統準備就緒，隨時可以啟動自動化生產。")
        else:
            print(f"⚠️ 注意：目前僅偵測到 {count} 個參數，請檢查 .env 是否有遺失行號。")
            
    except Exception as e:
        print(f"❌ 讀取過程發生非預期錯誤：{e}")
    print("="*50)

if __name__ == "__main__":
    initialize_vault()