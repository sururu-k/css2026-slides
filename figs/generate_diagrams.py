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

F14 = get_font(14)
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
C_WHITE = (255, 255, 255)
C_DARKGRAY = (51, 65, 85)

def save(im, name):
    path = os.path.join(OUT, name)
    im.save(path)
    print(f"Saved: {name} ({os.path.getsize(path)} bytes)")

# -------------------------------------------------------------
# FIG 2: S2 Ethereum Multi-Client Architecture
# -------------------------------------------------------------
def make_fig_s2():
    w, h = 680, 440
    im = Image.new("RGB", (w, h), C_WHITE)
    d = ImageDraw.Draw(im)

    # Title card: Specification
    d.rounded_rectangle([20, 170, 170, 270], radius=10, fill=C_BLUE, outline=C_BLUE)
    d.text((35, 195), "Ethereum", fill=C_WHITE, font=F18B)
    d.text((35, 225), "共通仕様書", fill=C_WHITE, font=F16B)

    # Execution Clients Section
    d.rounded_rectangle([230, 20, 650, 210], radius=8, fill=C_LGRAY, outline=C_BORDER)
    d.text((245, 30), "実行層 (Execution) クライアント", fill=C_NAVY, font=F16B)
    
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
        x = 245 + col * 130
        y = 65 + row * 65
        d.rounded_rectangle([x, y, x + 120, y + 55], radius=6, fill=C_WHITE, outline=C_BLUE, width=2)
        d.text((x + 10, y + 8), name, fill=C_NAVY, font=F16B)
        d.text((x + 10, y + 30), f"言語: {lang}", fill=C_GRAY, font=F14)

    # Consensus Clients Section
    d.rounded_rectangle([230, 230, 650, 420], radius=8, fill=C_LBLUE, outline=C_BLUE)
    d.text((245, 240), "合意層 (Consensus) クライアント (本研究対象)", fill=C_NAVY, font=F16B)
    
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
        x = 245 + col * 130
        y = 275 + row * 65
        d.rounded_rectangle([x, y, x + 120, y + 55], radius=6, fill=C_WHITE, outline=C_RED, width=2)
        d.text((x + 10, y + 8), name, fill=C_NAVY, font=F16B)
        d.text((x + 10, y + 30), f"言語: {lang}", fill=C_GRAY, font=F14)

    # Connecting arrows
    d.line([170, 220, 230, 115], fill=C_BLUE, width=3)
    d.line([170, 220, 230, 325], fill=C_BLUE, width=3)

    save(im, "fig_s2_clients.png")

# -------------------------------------------------------------
# FIG 3: S3 Casper FFG Accountable Safety & Quorum Overlap
# -------------------------------------------------------------
def make_fig_s3():
    w, h = 680, 440
    im = Image.new("RGB", (w, h), C_WHITE)
    d = ImageDraw.Draw(im)

    # Title header
    d.text((20, 15), "Casper FFG 帰責可能な安全性 (Accountable Safety)", fill=C_NAVY, font=F18B)

    # Left Circle: Quorum A (2/3)
    d.ellipse([50, 70, 350, 370], outline=C_BLUE, width=4)
    d.text((100, 120), "ブロック A 確定", fill=C_BLUE, font=F16B)
    d.text((110, 150), "クォーラム A\n(2/3 以上)", fill=C_NAVY, font=F14)

    # Right Circle: Quorum B (2/3)
    d.ellipse([270, 70, 570, 370], outline=C_ORANGE, width=4)
    d.text((410, 120), "ブロック B 確定", fill=C_ORANGE, font=F16B)
    d.text((410, 150), "クォーラム B\n(2/3 以上)", fill=C_NAVY, font=F14)

    # Intersection Area
    d.ellipse([210, 130, 410, 310], fill=C_LBLUE, outline=C_BLUE)
    d.text((250, 175), "必ず重なる！", fill=C_RED, font=F16B)
    d.text((235, 205), "交差部 ≥ 1/3", fill=C_NAVY, font=F16B)
    d.text((225, 235), "(二重投票者)", fill=C_DARKGRAY, font=F14)

    # Bottom Explanation Box
    d.rounded_rectangle([20, 380, 660, 430], radius=6, fill=C_LGRAY, outline=C_BORDER)
    d.text((30, 392), "【安全性の定理】 二重投票者は必ず検出・資産没収 (Slash) される", fill=C_RED, font=F14)
    d.text((30, 410), "⇒ 前提条件「スラッシングが正常作動」が崩れると確定覆り (Chain Split)", fill=C_NAVY, font=F14)

    save(im, "fig_s3_accountable_safety.png")

# -------------------------------------------------------------
# FIG 4: S4 EIP & Executable Specification Example
# -------------------------------------------------------------
def make_fig_s4():
    w, h = 680, 440
    im = Image.new("RGB", (w, h), C_WHITE)
    d = ImageDraw.Draw(im)

    d.text((20, 15), "イーサリアム仕様書 (consensus-specs / EIP) の構造", fill=C_NAVY, font=F18B)

    # Upper panel: Prose specification
    d.rounded_rectangle([20, 50, 660, 160], radius=8, fill=C_LGRAY, outline=C_BORDER)
    d.text((35, 60), "1. 自然言語による手順記述 (Prose Description)", fill=C_NAVY, font=F16B)
    d.text((35, 90), "「検証者の投票を集計し、総ステーキング量の 2/3 以上の同意が得られた場合、", fill=C_DARKGRAY, font=F14)
    d.text((35, 115), "  該当チェックポイントを正当化 (Justified) および確定 (Finalized) 処理する。」", fill=C_DARKGRAY, font=F14)
    d.text((35, 138), "※ 特徴: ステップ毎の手順はあるが「なぜ安全か (大域的前提)」は書かれない", fill=C_RED, font=F14)

    # Lower panel: Python Executable Spec Code
    d.rounded_rectangle([20, 180, 660, 420], radius=8, fill=C_NAVY, outline=C_NAVY)
    d.text((35, 192), "2. 実行可能な Python テストコード (Executable Python Spec)", fill=C_LBLUE, font=F16B)
    
    code_lines = [
        "def process_justification_and_finalization(state: BeaconState) -> None:",
        "    # Calculate matching balance",
        "    matching_target_balance = get_matching_target_balance(state)",
        "    total_active_balance = get_total_active_balance(state)",
        "    ",
        "    # Check 2/3 threshold (Quorum arithmetic)",
        "    if matching_target_balance * 3 >= total_active_balance * 2:",
        "        state.current_justified_checkpoint = Checkpoint(...)",
        "        # ... Update finalization checkpoint state"
        "    # NOTE: Quorum overlap & safety premises are nowhere asserted in code!"
    ]
    for i, line in enumerate(code_lines):
        color = C_WHITE
        if "#" in line:
            color = C_GRAY
        if "matching_target_balance * 3" in line:
            color = (253, 224, 71) # Yellow highlight
        if "NOTE:" in line:
            color = (252, 165, 165) # Red highlight
        d.text((35, 225 + i * 19), line, fill=color, font=F14)

    save(im, "fig_s4_eip_spec.png")

# -------------------------------------------------------------
# FIG 5: S5 Lean Premise Extraction Example
# -------------------------------------------------------------
def make_fig_s5():
    w, h = 680, 440
    im = Image.new("RGB", (w, h), C_WHITE)
    d = ImageDraw.Draw(im)

    d.text((20, 15), "証明からの前提抽出と仕様照合 (具体例: CHK-GEN-09)", fill=C_NAVY, font=F18B)

    # Left: Lean 4 Formalization
    d.rounded_rectangle([20, 55, 325, 415], radius=8, fill=C_LBLUE, outline=C_BLUE, width=2)
    d.text((35, 65), "Lean 4 形式証明 (定理)", fill=C_BLUE, font=F16B)
    d.text((35, 90), "theorem no_k_finalized_...", fill=C_NAVY, font=F14)
    
    d.rounded_rectangle([30, 115, 315, 230], radius=6, fill=C_WHITE, outline=C_RED, width=2)
    d.text((40, 125), "【定理の前提条件 (Hypothesis)】", fill=C_RED, font=F14)
    d.text((40, 150), "¬ q_intersection_slashed", fill=C_NAVY, font=F16B)
    d.text((40, 180), "「クォーラム交差の二重投票者が", fill=C_DARKGRAY, font=F14)
    d.text((40, 200), " 未処罰で放置されていないこと」", fill=C_DARKGRAY, font=F14)

    d.text((35, 245), "  ↓ 決定的抽出 (LLM不介在)", fill=C_NAVY, font=F14)
    d.rounded_rectangle([30, 275, 315, 400], radius=6, fill=C_WHITE, outline=C_BLUE)
    d.text((40, 285), "MUST-ESTABLISH 判定項目", fill=C_NAVY, font=F14)
    d.text((40, 310), "「相反する2ブロックの確定が", fill=C_DARKGRAY, font=F14)
    d.text((40, 330), " 同一高さで両立しないための", fill=C_DARKGRAY, font=F14)
    d.text((40, 350), " 前提条件を検査せよ」", fill=C_DARKGRAY, font=F14)

    # Arrow between panels
    d.polygon([(335, 235), (365, 220), (365, 250)], fill=C_RED)
    d.line([(330, 235), (365, 235)], fill=C_RED, width=3)

    # Right: EIP Specification Search
    d.rounded_rectangle([375, 55, 660, 415], radius=8, fill=C_LGRAY, outline=C_BORDER, width=2)
    d.text((390, 65), "EIP / consensus-specs 照合結果", fill=C_NAVY, font=F16B)
    
    d.rounded_rectangle([385, 100, 650, 300], radius=6, fill=C_WHITE, outline=C_BORDER)
    d.text((395, 110), "全89ファイル全文検索結果:", fill=C_NAVY, font=F14)
    d.text((395, 135), "・`quorum` 単語: 0件 (不在)", fill=C_RED, font=F14)
    d.text((395, 160), "・`q_intersection_slashed`: 0件", fill=C_RED, font=F14)
    d.text((395, 185), "・大域的安全不変条件記述: 0件", fill=C_RED, font=F14)
    d.text((395, 220), "状態更新の手続き(2/3計算)はあるが", fill=C_DARKGRAY, font=F14)
    d.text((395, 245), "前提条件としての明示なし", fill=C_DARKGRAY, font=F14)

    # Result Box
    d.rounded_rectangle([385, 320, 650, 400], radius=6, fill=(254, 226, 226), outline=C_RED, width=2)
    d.text((420, 335), "7 判定器 全会一致", fill=C_RED, font=F16B)
    d.text((435, 365), "「非明示 (非E)」", fill=C_RED, font=F18B)

    save(im, "fig_s5_extraction.png")

# -------------------------------------------------------------
# FIG 7: S7 Result Pie Chart & Abstract Premise Comparison
# -------------------------------------------------------------
def make_fig_s7():
    w, h = 680, 440
    im = Image.new("RGB", (w, h), C_WHITE)
    d = ImageDraw.Draw(im)

    d.text((20, 15), "検証結果: 証明前提 57件中 48件 (84.2%) が仕様に非明示", fill=C_NAVY, font=F18B)

    # Left: High Impact Pie Chart (drawn with arcs/polygons)
    # Pie center: (180, 200), radius 120
    # 84.2% Non-explicit (48/57) -> 303 degrees
    # 15.8% Split (9/57) -> 57 degrees
    # 0% Explicit (0/57)
    
    d.pieslice([50, 80, 290, 320], start=0, end=303, fill=C_RED, outline=C_WHITE)
    d.pieslice([50, 80, 290, 320], start=303, end=360, fill=C_GRAY, outline=C_WHITE)

    # Center Donut Hole for modern aesthetic
    d.ellipse([105, 135, 235, 265], fill=C_WHITE, outline=C_WHITE)
    d.text((135, 175), "84.2%", fill=C_RED, font=F24B)
    d.text((132, 210), "仕様に未記載", fill=C_NAVY, font=F14)

    # Legend under pie
    d.rectangle([40, 340, 60, 355], fill=C_RED)
    d.text((70, 338), "7判定器 全会一致で「非明示 (非E)」: 48件 (84.2%)", fill=C_NAVY, font=F14)
    
    d.rectangle([40, 365, 60, 380], fill=C_GRAY)
    d.text((70, 363), "判定に割れあり (部分明示/状態のみ): 9件 (15.8%)", fill=C_DARKGRAY, font=F14)

    d.rectangle([40, 390, 60, 405], fill=C_GREEN)
    d.text((70, 388), "7判定器 全会一致で「明示 (E)」: 0件 (0%)", fill=C_GREEN, font=F16B)

    # Right: Abstract vs Concrete Comparison Panel
    d.rounded_rectangle([320, 60, 660, 420], radius=8, fill=C_LGRAY, outline=C_BORDER)
    d.text((335, 75), "「抽象的・要件として不十分」の具体例", fill=C_NAVY, font=F16B)

    d.rounded_rectangle([330, 110, 650, 240], radius=6, fill=C_WHITE, outline=C_BORDER)
    d.text((340, 120), "【仕様書 (EIP/specs) にある記述】", fill=C_NAVY, font=F14)
    d.text((340, 145), "・個別の状態更新手続き（局所ルール）", fill=C_DARKGRAY, font=F14)
    d.text((340, 170), "・`is_slashable_attestation_data`", fill=C_BLUE, font=F14)
    d.text((350, 195), "「同エポックでの二重投票はスラッシュ」", fill=C_DARKGRAY, font=F14)
    d.text((350, 215), " → *個々のノードの局所的な処理動作のみ*", fill=C_GRAY, font=F14)

    d.rounded_rectangle([330, 255, 650, 400], radius=6, fill=C_WHITE, outline=C_RED, width=2)
    d.text((340, 265), "【形式証明が要求する前提条件】", fill=C_RED, font=F14)
    d.text((340, 290), "・システム全体の大域的安全不変条件", fill=C_NAVY, font=F14)
    d.text((340, 315), "・`q_intersection_slashed`", fill=C_RED, font=F14)
    d.text((350, 340), "「全クォーラム交差部において二重投票者が", fill=C_DARKGRAY, font=F14)
    d.text((350, 360), "  未処罰のまま放置されないこと」", fill=C_DARKGRAY, font=F14)
    d.text((350, 380), " → *仕様書にはこの大域的保証の記述が不在*", fill=C_RED, font=F14)

    save(im, "fig_s7_chart.png")

# -------------------------------------------------------------
# FIG 9: S9 Bug Co-occurrence & Concrete Incidents
# -------------------------------------------------------------
def make_fig_s9():
    w, h = 680, 440
    im = Image.new("RGB", (w, h), C_WHITE)
    d = ImageDraw.Draw(im)

    d.text((20, 15), "仕様の前提欠落領域と一致する過去の重大バグ事例", fill=C_NAVY, font=F18B)

    # Core Finding Card
    d.rounded_rectangle([20, 50, 660, 120], radius=8, fill=(254, 242, 242), outline=C_RED, width=2)
    d.text((35, 60), "【核心的発見】 仕様書で前提条件が漏れている領域 (正当化・確定処理) に", fill=C_RED, font=F16B)
    d.text((35, 88), "                   過去の重大な実運用バグが集中的に発生している！", fill=C_RED, font=F16B)

    # Concrete Bug 1: Nimbus PR#461
    d.rounded_rectangle([20, 140, 330, 420], radius=8, fill=C_WHITE, outline=C_BLUE, width=2)
    d.rounded_rectangle([20, 140, 330, 180], radius=8, fill=C_BLUE, outline=C_BLUE)
    d.text((35, 150), "実バグ例 1: Nimbus PR#461", fill=C_WHITE, font=F16B)
    
    d.text((35, 195), "■ 障害内容: チェーン分岐 (Chain Split)", fill=C_RED, font=F14)
    d.text((35, 220), "■ 原因領域: `justification_bits` 処理", fill=C_NAVY, font=F14)
    d.text((35, 245), "■ 詳細:", fill=C_NAVY, font=F14)
    d.text((45, 270), "正当化ビットフラグの整数", fill=C_DARKGRAY, font=F14)
    d.text((45, 292), "オーバーフローにより、確定", fill=C_DARKGRAY, font=F14)
    d.text((45, 314), "判定チェックポイントがズレて", fill=C_DARKGRAY, font=F14)
    d.text((45, 336), "ノード間で合意が崩壊。", fill=C_DARKGRAY, font=F14)
    d.text((35, 370), "⇒ 修正: ビット演算の境界チェック追加", fill=C_GREEN, font=F14)

    # Concrete Bug 2: Lighthouse PR#4576
    d.rounded_rectangle([350, 140, 660, 420], radius=8, fill=C_WHITE, outline=C_BLUE, width=2)
    d.rounded_rectangle([350, 140, 660, 180], radius=8, fill=C_BLUE, outline=C_BLUE)
    d.text((365, 150), "実バグ例 2: Lighthouse PR#4576", fill=C_WHITE, font=F16B)
    
    d.text((365, 195), "■ 障害内容: ファイナリティ計算不整合", fill=C_RED, font=F14)
    d.text((365, 220), "■ 原因領域: `finality` エポック境界", fill=C_NAVY, font=F14)
    d.text((365, 245), "■ 詳細:", fill=C_NAVY, font=F14)
    d.text((375, 270), "エポック境界での Attestation", fill=C_DARKGRAY, font=F14)
    d.text((375, 292), "集計処理のエッジケースにより", fill=C_DARKGRAY, font=F14)
    d.text((375, 314), "確定状態の計算結果がクライアント", fill=C_DARKGRAY, font=F14)
    d.text((375, 336), "間で乖離。", fill=C_DARKGRAY, font=F14)
    d.text((365, 370), "⇒ 修正: 確定状態遷移ロジックの再構築", fill=C_GREEN, font=F14)

    save(im, "fig_s9_bugs.png")

# -------------------------------------------------------------
# FIG 10: S10 Practical Takeaways for Implementers & Spec Authors
# -------------------------------------------------------------
def make_fig_s10():
    w, h = 680, 440
    im = Image.new("RGB", (w, h), C_WHITE)
    d = ImageDraw.Draw(im)

    d.text((20, 15), "実践的提言: 実装者と仕様執筆者はどうすべきか？", fill=C_NAVY, font=F18B)

    # Column 1: For Implementers
    d.rounded_rectangle([20, 55, 330, 420], radius=8, fill=C_LGRAY, outline=C_BLUE, width=2)
    d.rounded_rectangle([20, 55, 330, 100], radius=8, fill=C_BLUE, outline=C_BLUE)
    d.text((35, 68), "1. クライアント実装者への提言", fill=C_WHITE, font=F16B)

    d.text((35, 115), "■ 仕様手順の「なぞり書き」を脱却", fill=C_NAVY, font=F16B)
    d.text((35, 142), "・仕様コードの動作通りに書くだけでは", fill=C_DARKGRAY, font=F14)
    d.text((35, 162), "  安全性不変条件の破れを防げない", fill=C_DARKGRAY, font=F14)

    d.text((35, 195), "■ 形式証明由来の前提を明示アサート", fill=C_NAVY, font=F16B)
    d.text((35, 222), "・`q_intersection_slashed` などの", fill=C_DARKGRAY, font=F14)
    d.text((35, 242), "  大域的前提条件をコード内でランタイム", fill=C_DARKGRAY, font=F14)
    d.text((35, 262), "  アサーションとして埋め込む", fill=C_DARKGRAY, font=F14)

    d.text((35, 295), "■ 57の前提リストを監査・PBTに活用", fill=C_NAVY, font=F16B)
    d.text((35, 322), "・本研究が抽出した 57 条件を", fill=C_DARKGRAY, font=F14)
    d.text((35, 342), "  Property-Based Testing (Fuzzing)", fill=C_DARKGRAY, font=F14)
    d.text((35, 362), "  やコード監査のチェックリストに利用", fill=C_DARKGRAY, font=F14)

    # Column 2: For Spec Authors
    d.rounded_rectangle([350, 55, 660, 420], radius=8, fill=C_LBLUE, outline=C_RED, width=2)
    d.rounded_rectangle([350, 55, 660, 100], radius=8, fill=C_RED, outline=C_RED)
    d.text((365, 68), "2. 仕様書執筆者への提言", fill=C_WHITE, font=F16B)

    d.text((365, 115), "■ 大域的安全前提 (Invariant) の明記", fill=C_NAVY, font=F16B)
    d.text((365, 142), "・状態遷移コード (Python) だけでなく", fill=C_DARKGRAY, font=F14)
    d.text((365, 162), "  「システムが依存する安全性の前提」", fill=C_DARKGRAY, font=F14)
    d.text((365, 182), "  を仕様文書に要件として明記する", fill=C_DARKGRAY, font=F14)

    d.text((365, 215), "■ 形式証明 (Lean/Coq) との連携強化", fill=C_NAVY, font=F16B)
    d.text((365, 242), "・証明の仮定 (Hypothesis) と仕様書", fill=C_DARKGRAY, font=F14)
    d.text((365, 262), "  の要件定義を相互参照可能なリンクで", fill=C_DARKGRAY, font=F14)
    d.text((365, 282), "  結びつける構造を作る", fill=C_DARKGRAY, font=F14)

    d.text((365, 315), "■ 監査者のための要件明確化", fill=C_NAVY, font=F16B)
    d.text((365, 342), "・LLM監査や第三者監査が前提条件を", fill=C_DARKGRAY, font=F14)
    d.text((365, 362), "  見落とさない仕様記述形式への刷新", fill=C_DARKGRAY, font=F14)

    save(im, "fig_s10_takeaways.png")

if __name__ == "__main__":
    make_fig_s2()
    make_fig_s3()
    make_fig_s4()
    make_fig_s5()
    make_fig_s7()
    make_fig_s9()
    make_fig_s10()
