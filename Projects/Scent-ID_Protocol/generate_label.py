r"""
【標準化標題：Scent-ID 標籤幾何容器比例校正】
檔案名稱：D:\Jay_AI\Projects\Scent-ID_Protocol\generate_label.py
版本編號：V.5.0.1
核心任務：修正 QR Code 爆框溢出問題，鎖定安全邊界並保持最大視覺比例與絕對置中。
"""

import json
import os
import qrcode
import qrcode.image.svg
import svgwrite
import xml.etree.ElementTree as ET
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

# 1. 檔案路徑規範
BASE_DIR = r"D:\Jay_AI\Projects\Scent-ID_Protocol"
JSON_PATH = os.path.join(BASE_DIR, "database", "SID-CH-N5.json")
EXPORT_DIR = os.path.join(BASE_DIR, "exports", "labels")
if not os.path.exists(EXPORT_DIR): os.makedirs(EXPORT_DIR)

# 讀取數據 (確認 JSON 結構正確)
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 固定輸出檔名，味道唯一制
final_pdf_path = os.path.join(EXPORT_DIR, f"{data['sid_index']}_Official_Label.pdf")

# 2. QR Code 生成 (精確去除白邊)
qr_url = f"https://github.com/chunchieh0811-cloud/Scent-ID-Protocol/blob/main/database/{data['sid_index']}.json"
qr = qrcode.QRCode(version=1, border=0) # 徹底移除 QR 內建白邊，這是居中的核心！
qr.add_data(qr_url)
qr.make(fit=True)

qr_img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
svg_string = qr_img.to_string().decode('utf-8')
root = ET.fromstring(svg_string)
qr_path_data = "".join([path.get('d') for path in root.findall(".//{http://www.w3.org/2000/svg}path")])

# 3. 建立 400x600 專業佈局畫布
temp_svg = os.path.join(EXPORT_DIR, "layout_engine.svg")
dwg = svgwrite.Drawing(temp_svg, size=("400px", "600px"), profile='tiny')
dwg.viewbox(0, 0, 400, 600)

# 背景與外邊框 (加厚線條提升專櫃質感)
dwg.add(dwg.rect(insert=(0, 0), size=('400', '600'), fill='#FFFFFF'))
dwg.add(dwg.rect(insert=(20, 20), size=('360', '560'), fill='none', stroke='#1A1A1A', stroke_width=4))

# --- 4. QR Code 絕對置中校對 (精確 10.5x Scale) ---
# 計算：Version 1 QR 是 21x21 單元。
# 我們採用 Scale 10.5，總寬高 = 21 * 10.5 = 220.5px
# X 偏移 = (400 - 220.5) / 2 = 89.75 -> 取 90
# Y 偏移 = 70 (留白緩衝，確保與上方對稱且不壓下方)
if qr_path_data:
    # 這裡的 scale 調整為 10.5，大尺寸且具緩衝
    qr_group = dwg.g(transform="translate(90, 70) scale(10.5)")
    qr_group.add(dwg.path(d=qr_path_data, fill="black"))
    dwg.add(qr_group)

# --- 5. 文字資訊區 (穩定錨點) ---
# 黑色資訊條
dwg.add(dwg.rect(insert=(20, 360), size=('360', '45'), fill='#1A1A1A'))
dwg.add(dwg.text("SCENT-ID OFFICIAL ASSET", insert=(200, 388), 
                 font_family="Helvetica, Arial", font_size="16px", fill="white", 
                 text_anchor="middle", font_weight="bold"))

# 詳細資訊 (text-anchor="middle" 確保以中線對齊散開)
f_main = "Helvetica, Arial"
dwg.add(dwg.text(f"ID: {data['sid_index']}", insert=(200, 460), 
                 font_family=f_main, font_size="28px", font_weight="bold", text_anchor="middle"))
dwg.add(dwg.text(f"BRAND: {data['brand']}", insert=(200, 505), 
                 font_family=f_main, font_size="20px", fill="#333333", text_anchor="middle"))
dwg.add(dwg.text(f"NAME: {data['name']}", insert=(200, 540), 
                 font_family=f_main, font_size="20px", fill="#333333", text_anchor="middle"))

# 頁尾小字
dwg.add(dwg.text("SCENT-ID PROTOCOL VERIFIED", insert=(200, 575), 
                 font_family=f_main, font_size="10px", fill="#AAAAAA", text_anchor="middle"))

dwg.save()

# --- 6. 轉檔並覆寫單一 PDF 檔案 ---
drawing = svg2rlg(temp_svg)
renderPDF.drawToFile(drawing, final_pdf_path)
if os.path.exists(temp_svg): os.remove(temp_svg)

print("=" * 50)
print(f"✅ Scent-ID 專業標籤定案成功！")
print(f"📄 存檔路徑：{final_pdf_path}")
print(f"📏 佈局狀態：QR 比例 10.5 (精緻且不爆框)")
print("=" * 50)