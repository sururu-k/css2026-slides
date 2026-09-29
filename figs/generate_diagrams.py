import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))

def get_font(size, bold=False):
    font_path = "C:/Windows/Fonts/meiryo.ttc"
    if bold:
        font_path = "C:/Windows/Fonts/meiryob.ttc"
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

F12 = get_font(12)
F14 = get_font(14)
F14B = get_font(14, bold=True)
F16 = get_font(16)
F16B = get_font(16, bold=True)
F18 = get_font(18)
F18B = get_font(18, bold=True)
F20B = get_font(20, bold=True)
F24B = get_font(24, bold=True)

# Colors
C_NAVY = (15, 23, 42)
C_BLUE = (37, 99, 235)
C_LBLUE = (224, 242, 254)
C_GRAY = (100, 116, 139)
C_LGRAY = (241, 245, 249)
C_BORDER = (203, 213, 225)
C_RED = (220, 38, 38)
C_GREEN = (22, 163, 74)
C_ORANGE = (234, 88, 12)
C_PURPLE = (147, 51, 234)
C_WHITE = (255, 255, 255)
C_DARKGRAY = (51, 65, 85)

# Brand colors
COLOR_GO = (0, 172, 215)
COLOR_RUST = (222, 74, 18)
COLOR_JAVA = (229, 44, 47)
COLOR_CSHARP = (155, 79, 150)
COLOR_TS = (49, 120, 198)
COLOR_NIM = (255, 194, 0)
COLOR_PYTHON = (55, 118, 171)
COLOR_ETH = (98, 126, 234)
C_ETH = COLOR_ETH

def save(im, name):
    path = os.path.join(OUT, name)
    im.save(path)
    print(f"Saved: {name} ({os.path.getsize(path)} bytes)")

def draw_eth_logo(d, cx, cy, size=24):
    # Draw Ethereum diamond logo
    w = size // 2
    h = size
    points_top = [(cx, cy - h//2), (cx + w, cy), (cx, cy + h//6), (cx - w, cy)]
    points_bottom = [(cx, cy + h//6), (cx + w, cy), (cx, cy + h//2), (cx - w, cy)]
    d.polygon(points_top, fill=COLOR_ETH, outline=C_NAVY)
    d.polygon(points_bottom, fill=(60, 80, 180), outline=C_NAVY)

def draw_lang_badge(d, x, y, lang):
    badge_colors = {
        "Go": (COLOR_GO, "GO"),
        "Rust": (COLOR_RUST, "RUST"),
        "Java": (COLOR_JAVA, "JAVA"),
        "C#": (COLOR_CSHARP, "C#"),
        "TypeScript": (COLOR_TS, "TS"),
        "Nim": (COLOR_NIM, "NIM"),
        "Python": (COLOR_PYTHON, "PY"),
    }
    bg, label = badge_colors.get(lang, (C_GRAY, lang[:2].upper()))
    text_color = C_WHITE if lang != "Nim" else C_NAVY
    d.rounded_rectangle([x, y, x + 44, y + 20], radius=4, fill=bg)
    d.text((x + 6, y + 2), label, fill=text_color, font=F12)

# -------------------------------------------------------------
# FIG 2: S2 Ethereum Multi-Client Architecture
# -------------------------------------------------------------
def make_fig_s2():
    w, h = 680, 440
    im = Image.new("RGB", (w, h), C_WHITE)
    d = ImageDraw.Draw(im)

    # Title card: Specification with Ethereum Logo
    d.rounded_rectangle([20, 160, 170, 280], radius=10, fill=C_LBLUE, outline=COLOR_ETH, width=3)
    draw_eth_logo(d, 95, 195, size=32)
    d.text((40, 220), "イーサリアム", fill=C_NAVY, font=F16B)
    d.text((45, 248), "共通の仕様書", fill=C_BLUE, font=F14B)

    # Execution Clients Section
    d.rounded_rectangle([210, 15, 660, 210], radius=8, fill=C_LGRAY, outline=C_BORDER)
    d.text((225, 25), "実行層（Execution）のソフト", fill=C_NAVY, font=F16B)
    
    el_clients = [
        ("Geth", "Go"),
        ("Nethermind", "C#"),
        ("Besu", "Java"),
        ("Erigon", "Go"),
        ("Reth", "Rust")
    ]
    for i, (name, lang) in enumerate(el_clients):
        col = i % 3
        row = i // 3
        x = 225 + col * 140
        y = 60 + row * 68
        d.rounded_rectangle([x, y, x + 130, y + 58], radius=6, fill=C_WHITE, outline=C_BLUE, width=2)
        d.text((x + 8, y + 8), name, fill=C_NAVY, font=F16B)
        draw_lang_badge(d, x + 8, y + 32, lang)

    # Consensus Clients Section
    d.rounded_rectangle([210, 225, 660, 425], radius=8, fill=C_LBLUE, outline=C_BLUE)
    d.text((225, 235), "合意層（Consensus）のソフト（本研究の対象）", fill=C_NAVY, font=F16B)
    
    cl_clients = [
        ("Prysm", "Go"),
        ("Lighthouse", "Rust"),
        ("Teku", "Java"),
        ("Nimbus", "Nim"),
        ("Lodestar", "TypeScript")
    ]
    for i, (name, lang) in enumerate(cl_clients):
        col = i % 3
        row = i // 3
        x = 225 + col * 140
        y = 270 + row * 68
        d.rounded_rectangle([x, y, x + 130, y + 58], radius=6, fill=C_WHITE, outline=C_RED, width=2)
        d.text((x + 8, y + 8), name, fill=C_NAVY, font=F16B)
        draw_lang_badge(d, x + 8, y + 32, lang)

    # Connecting arrows
    d.line([170, 220, 210, 110], fill=C_BLUE, width=3)
    d.line([170, 220, 210, 325], fill=C_BLUE, width=3)

    save(im, "fig_s2_clients.png")

# -------------------------------------------------------------
# FIG 3: S3 Casper FFG Accountable Safety & Quorum Overlap
# -------------------------------------------------------------
def make_fig_s3():
    w, h = 680, 440
    im = Image.new("RGB", (w, h), C_WHITE)
    d = ImageDraw.Draw(im)

    d.text((20, 15), "Casper FFG の投票と安全性の仕組み", fill=C_NAVY, font=F18B)

    # Left Circle: Quorum A (2/3)
    d.ellipse([50, 70, 350, 370], outline=C_BLUE, width=4)
    d.text((100, 120), "ブロック A 確定", fill=C_BLUE, font=F16B)
    d.text((110, 150), "2/3 以上の投票", fill=C_NAVY, font=F14)

    # Right Circle: Quorum B (2/3)
    d.ellipse([270, 70, 570, 370], outline=C_ORANGE, width=4)
    d.text((410, 120), "ブロック B 確定", fill=C_ORANGE, font=F16B)
    d.text((410, 150), "2/3 以上の投票", fill=C_NAVY, font=F14)

    # Intersection Area
    d.ellipse([210, 130, 410, 310], fill=C_LBLUE, outline=C_BLUE)
    d.text((250, 175), "必ず重なる！", fill=C_RED, font=F16B)
    d.text((235, 205), "1/3 以上が重複", fill=C_NAVY, font=F16B)
    d.text((225, 235), "（二重投票者）", fill=C_DARKGRAY, font=F14)

    # Bottom Explanation Box
    d.rounded_rectangle([20, 380, 660, 430], radius=6, fill=C_LGRAY, outline=C_BORDER)
    d.text((30, 392), "【安全性の証明】 重なった二重投票者が没収（スラッシュ）される前提で安全と言える", fill=C_RED, font=F14)
    d.text((30, 410), "⇒ この前提がコードで正しく動いていないと、ブロックが2つ同時に確定してしまう", fill=C_NAVY, font=F14)

    save(im, "fig_s3_accountable_safety.png")

# -------------------------------------------------------------
# FIG 4: S4 EIP & Executable Specification Example
# -------------------------------------------------------------
def make_fig_s4():
    w, h = 680, 440
    im = Image.new("RGB", (w, h), C_WHITE)
    d = ImageDraw.Draw(im)

    d.text((20, 15), "イーサリアムの仕様書（EIP / consensus-specs）の中身", fill=C_NAVY, font=F18B)

    # Upper panel: Prose specification
    d.rounded_rectangle([20, 50, 660, 160], radius=8, fill=C_LGRAY, outline=C_BORDER)
    draw_eth_logo(d, 40, 75, size=24)
    d.text((60, 62), "1. 英語の説明文（文章での手順解説 - EIP仕様書）", fill=C_NAVY, font=F16B)
    d.text((35, 95), "「検証者の投票を集計し、全体の 2/3 以上の同意が得られたら", fill=C_DARKGRAY, font=F14)
    d.text((35, 118), "  該当チェックポイントを確定（Finalized）処理する。」", fill=C_DARKGRAY, font=F14)
    d.text((35, 140), "※ 特徴: 処理の手順は書いてあるが「安全のための全体ルール」は書かれない", fill=C_RED, font=F14)

    # Lower panel: Python Executable Spec Code
    d.rounded_rectangle([20, 180, 660, 420], radius=8, fill=C_NAVY, outline=C_NAVY)
    draw_lang_badge(d, 35, 192, "Python")
    d.text((90, 192), "2. 実行できる Python テストコード（Executable Spec）", fill=C_LBLUE, font=F16B)
    
    code_lines = [
        "def process_justification_and_finalization(state: BeaconState) -> None:",
        "    # 集計バランスの計算",
        "    matching_target_balance = get_matching_target_balance(state)",
        "    total_active_balance = get_total_active_balance(state)",
        "    ",
        "    # 2/3 以上のチェック",
        "    if matching_target_balance * 3 >= total_active_balance * 2:",
        "        state.current_justified_checkpoint = Checkpoint(...)",
        "        # ... 確定状態を更新",
        "    # ※「なぜこれで安全と言えるか」の前提条件はコード内にも書かれていない"
    ]
    for i, line in enumerate(code_lines):
        color = C_WHITE
        if "#" in line:
            color = C_GRAY
        if "matching_target_balance * 3" in line:
            color = (253, 224, 71)
        if "※" in line:
            color = (252, 165, 165)
        d.text((35, 225 + i * 19), line, fill=color, font=F14)

    save(im, "fig_s4_eip_spec.png")

# -------------------------------------------------------------
# FIG 5: S5 Lean Premise Extraction Example
# -------------------------------------------------------------
def make_fig_s5():
    w, h = 680, 440
    im = Image.new("RGB", (w, h), C_WHITE)
    d = ImageDraw.Draw(im)

    d.text((20, 15), "証明からの前提取り出しと仕様書の確認（例: CHK-GEN-09）", fill=C_NAVY, font=F18B)

    # Left: Lean 4 Formalization
    d.rounded_rectangle([20, 55, 325, 415], radius=8, fill=C_LBLUE, outline=C_PURPLE, width=2)
    d.rounded_rectangle([30, 63, 100, 83], radius=4, fill=C_PURPLE)
    d.text((36, 65), "LEAN 4", fill=C_WHITE, font=F12)
    d.text((110, 65), "形式証明（定理）", fill=C_PURPLE, font=F16B)
    d.text((35, 90), "theorem no_k_finalized_...", fill=C_NAVY, font=F14)
    
    d.rounded_rectangle([30, 115, 315, 230], radius=6, fill=C_WHITE, outline=C_RED, width=2)
    d.text((40, 125), "【定理が前提としている条件】", fill=C_RED, font=F14)
    d.text((40, 150), "¬ q_intersection_slashed", fill=C_NAVY, font=F16B)
    d.text((40, 180), "「二重投票者が処罰されずに", fill=C_DARKGRAY, font=F14)
    d.text((40, 200), " 放置されていないこと」", fill=C_DARKGRAY, font=F14)

    d.text((35, 245), "  ↓ 型情報から自動取り出し", fill=C_NAVY, font=F14)
    d.rounded_rectangle([30, 275, 315, 400], radius=6, fill=C_WHITE, outline=C_BLUE)
    d.text((40, 285), "確認すべき前提項目", fill=C_NAVY, font=F14)
    d.text((40, 310), "「ブロックが2つ同時に確定", fill=C_DARKGRAY, font=F14)
    d.text((40, 330), " しないための前提条件が", fill=C_DARKGRAY, font=F14)
    d.text((40, 350), " コードで守られているか」", fill=C_DARKGRAY, font=F14)

    # Arrow between panels
    d.polygon([(335, 235), (365, 220), (365, 250)], fill=C_RED)
    d.line([(330, 235), (365, 235)], fill=C_RED, width=3)

    # Right: EIP Specification Search
    d.rounded_rectangle([375, 55, 660, 415], radius=8, fill=C_LGRAY, outline=C_BORDER, width=2)
    d.text((390, 65), "仕様書での検索結果", fill=C_NAVY, font=F16B)
    
    d.rounded_rectangle([385, 100, 650, 300], radius=6, fill=C_WHITE, outline=C_BORDER)
    d.text((395, 110), "全89ファイルの検索結果:", fill=C_NAVY, font=F14)
    d.text((395, 135), "・`quorum` の単語: 0件", fill=C_RED, font=F14)
    d.text((395, 160), "・`q_intersection_slashed`: 0件", fill=C_RED, font=F14)
    d.text((395, 185), "・安全のための前提記述: 0件", fill=C_RED, font=F14)
    d.text((395, 220), "2/3の計算手順はあるが、", fill=C_DARKGRAY, font=F14)
    d.text((395, 245), "前提条件としては書かれていない", fill=C_DARKGRAY, font=F14)

    # Result Box
    d.rounded_rectangle([385, 320, 650, 400], radius=6, fill=(254, 226, 226), outline=C_RED, width=2)
    d.text((420, 335), "7つの判定器すべてで", fill=C_RED, font=F16B)
    d.text((435, 365), "「書かれていない」", fill=C_RED, font=F18B)

    save(im, "fig_s5_extraction.png")

# -------------------------------------------------------------
# FIG 7: S7 Result Pie Chart & Abstract Premise Comparison
# -------------------------------------------------------------
def make_fig_s7():
    w, h = 680, 440
    im = Image.new("RGB", (w, h), C_WHITE)
    d = ImageDraw.Draw(im)

    d.text((20, 15), "結果: 57個の前提条件のうち 48個（84.2%）は仕様書に書かれていない", fill=C_NAVY, font=F18B)

    d.pieslice([50, 80, 290, 320], start=0, end=303, fill=C_RED, outline=C_WHITE)
    d.pieslice([50, 80, 290, 320], start=303, end=360, fill=C_GRAY, outline=C_WHITE)

    d.ellipse([105, 135, 235, 265], fill=C_WHITE, outline=C_WHITE)
    d.text((135, 175), "84.2%", fill=C_RED, font=F24B)
    d.text((132, 210), "仕様書に未記載", fill=C_NAVY, font=F14)

    # Legend under pie
    d.rectangle([40, 340, 60, 355], fill=C_RED)
    d.text((70, 338), "7つの判定器すべてで「書かれていない」: 48個（84.2%）", fill=C_NAVY, font=F14)
    
    d.rectangle([40, 365, 60, 380], fill=C_GRAY)
    d.text((70, 363), "判定に割れあり（状態名のみ記載など）: 9個（15.8%）", fill=C_DARKGRAY, font=F14)

    d.rectangle([40, 390, 60, 405], fill=C_GREEN)
    d.text((70, 388), "7つの判定器すべてで「書かれている」: 0個（0%）", fill=C_GREEN, font=F16B)

    # Right: Abstract vs Concrete Comparison Panel
    d.rounded_rectangle([320, 60, 660, 420], radius=8, fill=C_LGRAY, outline=C_BORDER)
    d.text((335, 75), "「個別の動き」と「全体の安全ルール」の違い", fill=C_NAVY, font=F16B)

    d.rounded_rectangle([330, 110, 650, 240], radius=6, fill=C_WHITE, outline=C_BORDER)
    d.text((340, 120), "【仕様書に書かれていること】", fill=C_NAVY, font=F14)
    d.text((340, 145), "・関数の個別の動き（局所的なルール）", fill=C_DARKGRAY, font=F14)
    d.text((340, 170), "・`is_slashable_attestation_data`", fill=C_BLUE, font=F14)
    d.text((350, 195), "「同じエポックで2回投票したらスラッシュ」", fill=C_DARKGRAY, font=F14)
    d.text((350, 215), " → *各ノードの処理ロジックのみ*", fill=C_GRAY, font=F14)

    d.rounded_rectangle([330, 255, 650, 400], radius=6, fill=C_WHITE, outline=C_RED, width=2)
    d.text((340, 265), "【証明が前提としていること】", fill=C_RED, font=F14)
    d.text((340, 290), "・システム全体で守るべき安全ルール", fill=C_NAVY, font=F14)
    d.text((340, 315), "・`q_intersection_slashed`", fill=C_RED, font=F14)
    d.text((350, 340), "「重複部分の二重投票者が処罰されずに", fill=C_DARKGRAY, font=F14)
    d.text((350, 360), "  放置されることはない」", fill=C_DARKGRAY, font=F14)
    d.text((350, 380), " → *仕様書には文章として書かれていない*", fill=C_RED, font=F14)

    save(im, "fig_s7_chart.png")

# -------------------------------------------------------------
# FIG 9: S9 Bug Co-occurrence & Concrete Incidents
# -------------------------------------------------------------
def make_fig_s9():
    w, h = 680, 440
    im = Image.new("RGB", (w, h), C_WHITE)
    d = ImageDraw.Draw(im)

    d.text((20, 15), "前提が書かれていない部分と、過去のバグ発生場所の一致", fill=C_NAVY, font=F18B)

    # Core Finding Card
    d.rounded_rectangle([20, 50, 660, 120], radius=8, fill=(254, 242, 242), outline=C_RED, width=2)
    d.text((35, 60), "【分かったこと】 仕様書で前提が書かれていなかった処理（正当化・確定）で、", fill=C_RED, font=F16B)
    d.text((35, 88), "                 過去に実際の重大なバグが起きていた！", fill=C_RED, font=F16B)

    # Concrete Bug 1: Nimbus PR#461
    d.rounded_rectangle([20, 140, 330, 420], radius=8, fill=C_WHITE, outline=C_BLUE, width=2)
    d.rounded_rectangle([20, 140, 330, 180], radius=8, fill=C_BLUE, outline=C_BLUE)
    draw_lang_badge(d, 30, 150, "Nim")
    d.text((80, 150), "Nimbus PR#461", fill=C_WHITE, font=F16B)
    
    d.text((35, 195), "■ 障害: チェーン分岐（Chain Split）", fill=C_RED, font=F14)
    d.text((35, 220), "■ 原因: 正当化ビットの処理", fill=C_NAVY, font=F14)
    d.text((35, 245), "■ 内容:", fill=C_NAVY, font=F14)
    d.text((45, 270), "正当化フラグの計算で整数", fill=C_DARKGRAY, font=F14)
    d.text((45, 292), "オーバーフローが発生し、確定の", fill=C_DARKGRAY, font=F14)
    d.text((45, 314), "判定がズレてノード間で合意が", fill=C_DARKGRAY, font=F14)
    d.text((45, 336), "分裂してしまった。", fill=C_DARKGRAY, font=F14)
    d.text((35, 370), "⇒ 修正: ビット計算のチェックを追加", fill=C_GREEN, font=F14)

    # Concrete Bug 2: Lighthouse PR#4576
    d.rounded_rectangle([350, 140, 660, 420], radius=8, fill=C_WHITE, outline=C_BLUE, width=2)
    d.rounded_rectangle([350, 140, 660, 180], radius=8, fill=C_BLUE, outline=C_BLUE)
    draw_lang_badge(d, 360, 150, "Rust")
    d.text((410, 150), "Lighthouse PR#4576", fill=C_WHITE, font=F16B)
    
    d.text((365, 195), "■ 障害: 確定計算の不整合", fill=C_RED, font=F14)
    d.text((365, 220), "■ 原因: エポック境界の集計", fill=C_NAVY, font=F14)
    d.text((365, 245), "■ 内容:", fill=C_NAVY, font=F14)
    d.text((375, 270), "エポック境界での投票集計処理の", fill=C_DARKGRAY, font=F14)
    d.text((375, 292), "バグにより、確定の計算結果が", fill=C_DARKGRAY, font=F14)
    d.text((375, 314), "クライアント間で食い違った。", fill=C_DARKGRAY, font=F14)
    d.text((375, 336), "", fill=C_DARKGRAY, font=F14)
    d.text((365, 370), "⇒ 修正: 確定処理の計算ロジックを直した", fill=C_GREEN, font=F14)

    save(im, "fig_s9_bugs.png")

# -------------------------------------------------------------
# FIG 10: S10 Practical Takeaways for Implementers & Spec Authors
# -------------------------------------------------------------
def make_fig_s10():
    w, h = 680, 440
    im = Image.new("RGB", (w, h), C_WHITE)
    d = ImageDraw.Draw(im)

    d.text((20, 15), "提案: 実装する人と仕様書を書く人はどうすべきか？", fill=C_NAVY, font=F18B)

    # Column 1: For Implementers
    d.rounded_rectangle([20, 55, 330, 420], radius=8, fill=C_LGRAY, outline=C_BLUE, width=2)
    d.rounded_rectangle([20, 55, 330, 100], radius=8, fill=C_BLUE, outline=C_BLUE)
    d.text((35, 68), "1. クライアントを実装する人へ", fill=C_WHITE, font=F16B)

    d.text((35, 115), "■ 仕様コードの丸写しをしない", fill=C_NAVY, font=F16B)
    d.text((35, 142), "・仕様書の手順通りに動かすだけでは", fill=C_DARKGRAY, font=F14)
    d.text((35, 162), "  安全上の前提が守られないことがある", fill=C_DARKGRAY, font=F14)

    d.text((35, 195), "■ 安全チェック（アサーション）を入れる", fill=C_NAVY, font=F16B)
    d.text((35, 222), "・`q_intersection_slashed` などの", fill=C_DARKGRAY, font=F14)
    d.text((35, 242), "  前提条件が壊れていないか確認する", fill=C_DARKGRAY, font=F14)
    d.text((35, 262), "  コードを自作して入れておく", fill=C_DARKGRAY, font=F14)

    d.text((35, 295), "■ 57個の前提リストをテストに活用", fill=C_NAVY, font=F16B)
    d.text((35, 322), "・本研究で抽出した 57 条件を", fill=C_DARKGRAY, font=F14)
    d.text((35, 342), "  自動テスト（ファジング）やコード確認", fill=C_DARKGRAY, font=F14)
    d.text((35, 362), "  のチェックリストとして使う", fill=C_DARKGRAY, font=F14)

    # Column 2: For Spec Authors
    d.rounded_rectangle([350, 55, 660, 420], radius=8, fill=C_LBLUE, outline=C_RED, width=2)
    d.rounded_rectangle([350, 55, 660, 100], radius=8, fill=C_RED, outline=C_RED)
    d.text((365, 68), "2. 仕様書を書く人へ", fill=C_WHITE, font=F16B)

    d.text((365, 115), "■ 安全のための前提条件を文章で追記", fill=C_NAVY, font=F16B)
    d.text((365, 142), "・Pythonのコードだけでなく", fill=C_DARKGRAY, font=F14)
    d.text((365, 162), "  「このシステムが前提としているルール」", fill=C_DARKGRAY, font=F14)
    d.text((365, 182), "  を文章として仕様書に書く", fill=C_DARKGRAY, font=F14)

    d.text((365, 215), "■ 数学的な証明（Lean/Coq）と紐づける", fill=C_NAVY, font=F16B)
    d.text((365, 242), "・証明で使われた前提と仕様書の記述を", fill=C_DARKGRAY, font=F14)
    d.text((365, 262), "  リンクさせて、第三者が確認できるように", fill=C_DARKGRAY, font=F14)
    d.text((365, 282), "  しておく", fill=C_DARKGRAY, font=F14)

    d.text((365, 315), "■ 監査しやすい仕様書の書き方へ", fill=C_NAVY, font=F16B)
    d.text((365, 342), "・外部の監査やLLMが見落とさないよう", fill=C_DARKGRAY, font=F14)
    d.text((365, 362), "  要件をわかりやすく整理する", fill=C_DARKGRAY, font=F14)

    save(im, "fig_s10_takeaways.png")

if __name__ == "__main__":
    make_fig_s2()
    make_fig_s3()
    make_fig_s4()
    make_fig_s5()
    make_fig_s7()
    make_fig_s9()
    make_fig_s10()
