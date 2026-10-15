<div class="cover">
<p class="eyebrow">CSS2026 / BWS ブロックチェーンワークショップ</p>
<h1>仕様どおりに実装すれば<br>安全か</h1>
<p class="subtitle">イーサリアムのコンセンサス仕様に明示されない<br>安全性の前提条件（予備調査）</p>
<p class="authors"><strong>村上 大岳</strong>（愛知総合工科高校）<br>神波 真聖・柳浜 万里（Nyx Foundation）<br>釘宮 由成（Independent Researcher）</p>
<p class="cover-claim">安全性の証明から前提を取り出し、確認項目にする。</p>
<p class="agenda-line">背景 ── 従来の問題点 ── 仮説 ── この研究の優位性</p>
</div>

Note:
村上です。
本日は、イーサリアムを例に、共通仕様から作られる複数のソフトの確認方法をお話しします。
研究の提案は、安全性の証明から前提を取り出して、仕様を読むだけでは拾いにくい確認項目を補うことです。
背景、従来の問題点、仮説、この研究の優位性の順で話します。

---

<p class="section-tag">背景</p>

## 「同じ仕様書」なのに、動きが違う

<p>ブロックチェーンの話の前に、エンジニアなら見覚えのある状況から始めます。</p>

<p class="label">例：身近な「仕様 × 複数実装」</p>
<table>
<thead><tr><th>分野</th><th>共通の仕様</th><th>複数の実装</th><th>ズレた所</th></tr></thead>
<tbody>
<tr><td>ブラウザ</td><td>HTML/JSの仕様</td><td>Chrome・Firefox・<strong>Safari</strong></td><td>Safariだけ表示がずれる</td></tr>
<tr><td>Cコンパイラ</td><td>言語規格</td><td>GCC・Clang・MSVC</td><td>未定義動作・拡張で結果が違う</td></tr>
<tr><td>SQL</td><td>標準SQL</td><td>MySQL・PostgreSQL・SQLite</td><td>方言があり、移植すると壊れる</td></tr>
</tbody>
</table>
<p class="message">書いてある所のズレはテストで潰せる。<mark>残るのは、書いていない所</mark>。<br>── もしこのズレが、<strong>資産を扱う基盤</strong>で起きたら？</p>

Note:
まず身近な例から入ります。ブラウザ、Cコンパイラ、SQL。どれも共通の仕様や規格があって、複数の実装がある。
そして「仕様どおりに書いたはずなのに、片方でだけ動かない」という経験は、たいていのエンジニアが持っているはずです。
大事なのは、ズレが出る場所です。仕様に明確に書いてある部分は各実装とも正しく作られます。
ズレが生まれるのは、仕様が書いていない部分、つまり解釈の余地や暗黙の前提があるところです。
では、このズレが資産を扱う基盤で起きたらどうなるか。次のスライドから、実際の対象であるイーサリアムを見ます。

---

<p class="section-tag">背景</p>

## 「だったら実装を1つに統一すれば？」

<img class="diagram diversity-visual" style="height: 240px; margin: 8px auto; display: block;" src="figs/diagram-client-diversity.svg" alt="単一実装の単一障害点（全滅リスク）と複数実装の多様性による耐障害性の対比図">
<p class="takeaway" style="margin-top: 12px; padding: 10px 18px; font-size: 24px;">多様性そのものが安全機構。<br>ただし<strong>「共通の前提」が共有されていなければ、多様性は機能しない。</strong></p>
<p class="message" style="margin: 12px 0 6px; font-size: 26px;">前提は研究者の間では共有済み。届いていないのは<strong>実装者・監査者</strong>。</p>

Note:
単一実装は単一障害点になります。
イーサリアムはあえて複数の独立実装を動かす多様性を安全機構にしました。
しかし、全チームが共通の前提を共有していなければ多様性は機能しません。
その前提が現場に届いていない、この断絶が今日の主題です。

【質問時用メモ】
・「公式バイナリに統一すれば？」への回答：単一実装でもアップグレード過渡期は新旧が同居し事実上の複数実装状態になる。実際Bitcoinも2013年に新旧バージョンのルール差でチェーン分裂事故（BDB事故）を経験している。
・前提の所在：前提は研究者の間（Casper FFG論文やLean証明）には厳密に存在するが、実装者・監査者の読む仕様書やテストに落ちてきていない。

---

<p class="section-tag">背景</p>

## イーサリアムについて

<div class="visual-story">
<img class="web-illustration" src="figs/web-connected-world.svg" alt="unDraw Connected world：世界各地がつながるネットワークのイラスト">
<div class="story-copy"><div class="brand-lockup"><img class="ethereum-logo" src="figs/ethereum.svg" alt="Ethereum 公式カラーロゴ"><h3>Ethereum</h3></div><p class="lead">世界中の第三者が運用する、<br>取引・プログラム実行の基盤。</p><p>全員が<mark>同じ取引履歴</mark>を保存・確認する。<br>管理者ではなく数学に依存。<br>だから、善良な参加者は<br><strong>全員同じ動きをしなければならない。</strong></p></div>
</div>
<p class="source">解説：<a href="https://ethereum.org/en/developers/docs/nodes-and-clients/">ethereum.org</a> ／ 公式Ethereumロゴ：<a href="https://ethereum.org/en/assets/">brand assets</a> ／ イラスト：Katerina Limpitsouni, <a href="https://undraw.co/illustration/connected-world_anke">unDraw</a></p>

Note:
イーサリアムは、世界中の第三者が運用するコンピュータで、取引やプログラムの実行結果を共有する基盤です。
全員が同じ取引履歴を保存し、互いに確認します。
中央の管理者を置かず、計算と経済的なインセンティブの仕組みに依存して動きます。
全員で決めるので、善良な参加者は全員が同じ動きをしなければなりません。
ここで重要なのは、この基盤を動かすソフトが、一つのチームが作った一種類のものではないという点です。

---

<p class="section-tag">背景</p>

## そもそも仕様書って、どうできてるの？

<p>具体例：<strong>参加者の投票で「確かな履歴」を全員同じ結果に決める</strong>システムの仕様書。</p>

<div class="grid">
<div class="panel"><p class="label">システムがやること</p><p>① 参加者は「この履歴が正しい」と投票し続ける<br>② 約6.4分（エポック）ごとに全員が同じ手順で集計<br>③ <strong>総支持の2/3超</strong>で「確かな履歴」にマーク</p></div>
<div class="panel"><p class="label">仕様書ではこう書いてある（実物抜粋）</p><div class="proof-code tight"><div>class Checkpoint(Container):  <span class="muted">#「確かな履歴」＝時刻＋指紋</span></div><div>justification_bits: Bitvector[4]  <span class="muted"># 確定判定の履歴</span></div><div>def process_epoch(state):  <span class="muted"># エポックごとの集計</span></div></div><p class="small">型・フィールド・関数まで定義した、実行可能な疑似コード級の詳細設計。</p></div>
</div>
<p class="message">全チームが<strong>この同じ文書を読んで</strong>、実装を書く。</p>
<p class="source">ethereum/consensus-specs（公開・版管理）。抜粋はbeacon-chain.mdの定義の簡略化。</p>

Note:
具体例として、参加者の投票で「確かな履歴」を全員同じ結果に決めるシステムを見ます。
左の手順——参加者が投票し続け、約6.4分ごとに全員が同じ手順で集計し、総支持の3分の2超で確かな履歴にマークする——これがこのシステムのやることです。
右が実物の抜粋です。
「確かな履歴」はCheckpointという型で、時刻と履歴の指紋の組。
集計はprocess_epochという関数。
確定判定の履歴はjustification_bitsという4ビットのフィールドで、これはのちの実例にも繋がるので覚えておいてください。
このように仕様書は、型・フィールド名・更新手順まで疑似コードで定義した、極めて詳細な文書です。
実行も可能で、仕様から生成されるテストデータが各実装の検査に使われます。
全チームがこの一つの文書を読んで実装を書きます。
次の図でその関係を見ます。

---

<p class="section-tag">背景</p>

## 厳密なのは「手順」。「いつ安全か」は書いていない

<p>「疑似コードまで書かれた仕様なら、ズレないのでは？」<br>——厳密に定義されているのは<strong>どう動くか</strong>。抜けているのは<strong>いつ正しいか</strong>。</p>

<div class="grid">
<div class="panel"><p class="label">仕様が定義するもの</p><p>型・フィールド・更新手順<br>実行可能な疑似コード<br>→ <strong>「どう動くか」（HOW）</strong></p></div>
<div class="panel"><p class="label">仕様に書いていないもの</p><p>その手順が安全に機能する条件<br>想定している状況・適用範囲<br>→ <strong>「いつ正しいか」（WHEN）</strong></p></div>
</div>
<p class="message">＝ <strong>doc に事前条件のない関数</strong>を、<br>各チームが読んで実装している状態。</p>
<p class="small">コードは正確に読める。でも「この前提を満たさない呼び出しは無効」という契約が書かれていない——あの感覚です。</p>

Note:
「疑似コードまである詳細な仕様なら、ズレようがないのでは？」と思われるかもしれません。実際、仕様書は「どう動くか」については極めて厳密です。
型も手順も実行できるほど詳細に書いてあります。
でも、ソフトウェアでいう「この関数の事前条件は何か」——その手順がいつ安全に機能するかという契約は、仕様には書かれていません。
実装経験があれば分かると思いますが、コード自体は完璧に読めても、「callerはnullを渡してはいけない」「このリストはソート済み前提」という条件がdocに無い関数は、
読み手ごとに前提の補い方が変わります。
全実装がまさにその状態にあります。
その「書いていない前提」がどこにあるか、実際の例で見ていきます。次の図では、この共通仕様から複数の実装がどう作られるかを見ます。

---

<p class="section-tag">背景</p>

## 一つの共通仕様から、別々のソフトが作られる

<p>実装者は<strong>仕様書を読んでコードを書く</strong>。別々の言語の実装が、同じネットワークで動く。</p>
<img class="architecture-visual" src="figs/illustration-clients.svg" alt="共通仕様からLighthouse、Nimbus、Teku、Lodestarへ分岐。Rust、Nim、Java、TypeScriptの各言語名の下にも公式言語ロゴを表示">
<p class="message">共通仕様をもとに、独立した実装が共存する<strong>多実装環境</strong>。</p>
<p class="source">合意を担当する4実装を例示。このソフトをクライアントと呼ぶ。実装・言語ロゴは公式素材（出典・権利者は補足と <code>figs/logo-sources.json</code>）。</p>

Note:
たとえば、RustのLighthouse、NimのNimbus、JavaのTeku、TypeScriptのLodestarがあります。
上がソフトのロゴ、言語名の下が言語のロゴです。
開発の形は、共通の仕様書を読んで、それぞれのチームが自分の言語でコードを書く、というものです。
こうして作られた実装が、同じネットワークに参加します。
「1つのC++コアを各言語でラップすればいいのでは？」という疑問は当然です。
あえて独立チーム・別言語でフルスクラッチするのは、1つのゼロデイやコンパイラバグで全実装が共倒れするのを防ぐためです。
N-version programming、多様性そのものが安全機構です。
これを多実装環境と呼びます。
今回のクライアントという語は、このネットワークを動かすソフトです。
そこで開発者や監査者は、何を基準に別々の実装を確認するのでしょうか。
その前に——ずれると、なぜまずいのかを先に見ます。

---

<p class="section-tag">背景</p>

## 「食い違い」は、なぜ特別に危険なのか

<p style="margin: 6px 0 10px;">普通のソフトのバグは「利用者の問題」。<br>ここで壊れるのは、<strong>「全員が同じ履歴を持つ」という合意そのもの</strong>。</p>
<img class="diagram split-visual" style="height: 240px; margin: 6px auto; display: block;" src="figs/diagram-chain-split.svg" alt="暗黙前提の解釈差によるチェーン分裂（Chain Split）と資産喪失の危機を示す図解">
<p class="takeaway" style="margin-top: 10px; padding: 10px 18px; font-size: 24px;">各実装が「仕様どおり」に動くだけでは不十分。<br><strong>暗黙前提のわずかなズレが、不可逆なチェーン分裂を引き起こす。</strong></p>
<p class="small" style="margin-top: 6px;">「分裂し得る」と分類された修正は実際に公開されている——後の実例で紹介。</p>

Note:
先に「なぜこれが大事か」を言います。
普通のソフトのバグは、そのソフトを使う人だけが困ります。
ところがコンセンサス実装のずれは別格です。
この基盤が売っている商品は「全員が同じ履歴を持つこと」、つまり一致そのものだからです。
もし実装AとBが、それぞれ別の履歴を「確定」、つまり覆せないと記録したら、履歴は二つに裂けます。
確定済みのはずの取引が一方で消え、担保を預けた参加者の資産も危険にさらされます。
言い換えれば、数兆円が消し飛び得る話です。
実際に「分裂し得る」と分類された修正は公開されており、後で実例を見ます。
つまり「全部の実装が本当に同じ判断をするか」は、品質管理の範囲を超えた、基盤の存亡の問題です。
では人々は何で揃えているのか——次に監査の出発点を見ます。

---

<p class="section-tag">背景</p>

## 開発・監査の出発点は、共通の仕様書

<p>実際の仕様書の抜粋。<strong>どの入力で、どの状態をどう更新するか</strong>が書かれている。<br>
文脈：約6.4分ごとの集計処理の中で、<strong>票の支持が厚い履歴を「確か」とマークする</strong>部分。</p>

```python
if previous_epoch_target_balance * 3 >= total_active_balance * 2:
    #   「前の期間に集まった支持の重み」×3  ≧  「有権者全員の重み」×2
    #   = 支持が全体の 2/3 以上か？ という判定（×3・×2 は分数の整数化）
    state.current_justified_checkpoint = Checkpoint(
        epoch=previous_epoch, root=get_block_root(state, previous_epoch)
    )
    state.justification_bits[1] = 0b1   # 「正当化した」という履歴を4bitに記録
```

<p class="source">原典：<a href="https://github.com/ethereum/consensus-specs/blob/2359a5e/specs/phase0/beacon-chain.md#justification-and-finalization">consensus-specs @ 2359a5e</a>。このコードは票の支持を状態に反映する部分。EIP-3675 はこの詳細仕様を参照する。</p>

Note:
合意を担当するソフトの詳細仕様は、consensus-specsという公開文書です。
文章と、処理を定義するPythonのコードからなります。
開発者はこの疑似コードを読んで、RustやNimなど自分の言語で同じ処理を書きます。
なお1行目の「支持する重み×3 ≥ 総重み×2」が、あの「2/3の支持」の判定です。
×3と×2は、分数の3分の2を整数だけで比較するための書き方です。
変数名を覚える必要はありませんが、このように数値はコードにあるのに、「どの状態のどの集合を数えているか」は行の中に名前がありません。
そして最終行で更新している justification_bits こそが、のちの実例で出てくる Nimbus #461 がずらした状態そのものです。
覚えておくと繋がります。
仕様から要求された処理を列挙し、各実装がそのとおり動くか確認する。
これが今の標準的なやり方です。
ここで当然、「仕様に忠実に準拠していれば十分ではないか？」という疑問が湧きます。次でその理由をお話しします。
その疑問は正しく、そして重要です。
次で応えます。

---

<p class="section-tag">従来の問題点</p>

## 「分かる」と「書いていない」は、別の層

<p>さきほどの式を読み解くと、<strong>2つの層</strong>に分かれます。</p>

<div class="grid">
<div class="panel"><p class="label">仕様書で「分かる」もの</p><p>×3 ≧ ×2 という計算・更新手順<br>変数が何を指すか（定義を辿れば追える）<br>→ <strong>手順と意味は書いてある</strong></p></div>
<div class="panel"><p class="label">仕様書のどこにも「書いていない」もの</p><p>この判定が<strong>いつ安全に効くか</strong>——<br>どの名簿・どの分岐状況・どんな出席率を<br>想定した保証か、という<strong>前提条件</strong><br>→ <mark>文章のどこにも出てこない</mark></p></div>
</div>
<p class="small">「よく読めば分かる」「仕様に書き足せばいい」——どちらも正しい。<br>
ただし仕様書をいくら精読しても、文章に無い前提は出てきません。<br>
書き足すにも「何を書くか」の確かな一覧が必要。抜け漏れなしの一覧は<strong>証明の中にだけ</strong>ある。</p>

<p class="small">監査の確認項目は<strong>仕様の文章から作られる</strong>。書かれていない条件は誰が見る？</p>

Note:
さきほどの式は写せます。変数の中身も、仕様書の中で定義を辿れば追えます。ここは正直に言います、意味は書いてあるんです。
書いていないのはその先です。
この判定がいつ安全に効くのか——どの名簿を数え、どんな分岐状況・出席率を想定した保証なのかという前提条件は、仕様書のどこにも出てきません。
前後をいくら読んでも見つからない。それが証明の仮説にだけ書かれています。
「仕様書をよく読めばいい」「じゃあ仕様にその前提を書き足せばいい」——どちらも方向は正しいです。ただ仕様書をいくら精読しても、文章に無いものは出てきません。
そして書き足す側にも、何を書くべきかの確かな一覧はありません。散文の書き足しはもう一度の翻訳で、設計から仕様への翻訳で前提が落ちたのと同じ漏れが起きます。
抜け漏れなしの一覧は証明の中にだけあります。
仕様から要求された処理を列挙し、各実装がそのとおり動くか確認する。これが今の標準的なやり方です。
では、なぜ仕様に準拠しているだけでは防げないのか。次のスライドでその構造を説明します。

---

<p class="section-tag">従来の問題点</p>

## 「仕様に準拠すれば良い」のでは？

<p>その通り——<strong>全チームがそうしています</strong>。<br>問題は単なる準拠ミスではなく、<strong>同じ記述でも解釈が分かれてしまうこと</strong>にあります。</p>

<div class="grid">
<div class="panel"><p class="label">ふつうの層：手順の記述</p><p>仕様が「この操作をこうする」と具体的<br>ずれる ＝ <strong>誰かのミス</strong><br>→ レビュー・テストで見つかる</p></div>
<div class="panel"><p class="label">今回の層：条件の記述（数学に近い）</p><p>「〜の2/3」「その時点の〜」と条件を書く<br>ずれる ＝ <strong>別々の妥当な読み</strong><br>→ 全員「仕様準拠」なのに結果が違う</p></div>
</div>

<p class="message">「どの解釈が正しいか」は、<strong>仕様の文章だけでは裁定できない</strong>。</p>
<p class="small">Cの規格にも未定義動作はあるが、「どの集合を数えるか」が実装ごとに分かれる種類のずれは、手順が具体的な層では起きにくい。</p>

Note:
全員が仕様に準拠しています。
問題は準拠ミスではなく、同じ記述でも別々の妥当な解釈が生まれることです。
手順のズレはテストで見つかりますが、数学的な条件文は全員が仕様準拠のまま結果が分かれてしまいます。
仕様の文章だけでは裁定できません。

【質問時用メモ】
・「C言語など一般的な仕様準拠と何が違う？」への回答：Cの規格にも未定義動作はあるが、「どの集合を数えるか」が実装ごとに分かれる種類のズレは、手順が具体的な層では起きにくい。「〜の2/3」「その時点の〜」のような数学的条件文特有の失敗モード。

---

<p class="section-tag">従来の問題点</p>

## 安全性の核心：クォーラム交差の前提

<p style="margin: 6px 0 10px;">「仕様どおり」なのに結果が分かれる理由：<br>合意仕様は<strong>数学的な安全性定理（クォーラム交差）</strong>に依存している。</p>
<img class="diagram votes-visual" style="height: 230px; margin: 6px auto; display: block;" src="figs/illustration-votes.svg" alt="同じ参加者集合と同じ票の重みなら、2つの3分の2の支持集合は少なくとも3分の1重なる。面積比は数量を表さない模式図">
<p class="takeaway" style="margin-top: 10px; padding: 10px 18px; font-size: 24px;">定理は「同じ参加者集合・同じ重み」を前提に安全を保証。<br><strong>この前提が仕様の文章に書かれていなければ、各実装で解釈が分かれてしまう。</strong></p>
<p class="small" style="margin-top: 6px;">どれだけ算術（2/3）を正しく実装しても、前提が満たされなければ安全性は保証されない。</p>

Note:
合意仕様の安全性を支えるのはクォーラム交差定理です。
2/3以上の支持が2つあれば、必ず1/3以上が重複し、履歴の二重確定を防ぎます。
しかしこの定理は「同じ参加者集合・同じ重み」を前提にしています。
この前提は仕様書には書かれていません。

【質問時用メモ】
・「なぜ仕様書に書かれない？」への回答：仕様書には「2/3以上の支持」という計算手順（HOW）は書かれているが、「どの参加者集合を分母とすべきか」という前提条件（WHEN）は定理側にしかないため。

---

<p class="section-tag">従来の問題点</p>

## なぜ、仕様を読むだけでは見えないのか

<img class="pipeline-visual" src="figs/diagram-spec-pipeline.svg" alt="3者の会話。理論家「前提Pなら、この動きで安全」（証明 P⇒Q）。仕様書「こう動いてね」（手順Sのみ）。実装者・監査者「前提がない。いつ正しいの？」（基準はSだけ）。前提Pを持つのは上流だけで、届く道は2つとも閉ざされている。仕様経由は転記で落ち、直接読むにも証明はLeanで下流は読めない">
<p class="message"><strong>根本原因：</strong>仕様が成り立つ<strong>前提条件</strong>が、<br>実装者・監査者からは<strong>読めない</strong>。</p>
<p class="small">「証明」＝「この条件を満たせば保証が必ず成り立つ」を<strong>機械が検算</strong>した文書（Lean）。<br><strong>機械が受理した時点で、仮説に抜け漏れはない</strong>——書くべき前提の確かな一覧は証明の中にだけある。</p>
<p class="source">図は説明用の模式図。設計の安全性議論はCasper FFG・Gasper等の研究に、仕様はconsensus-specs（EIP）に存在。証明の機械化がgasper-lean4。</p>

Note:
なぜ前提が仕様書にないのか。
根本原因は、理論家は「前提Pなら安全Q（WHEN）」を証明し、仕様書は「こう動け（HOW）」と手順しか書かない構造ギャップにあります。
証明は専門言語のLeanで書かれており、現場の実装者・監査者には前提が届かないのです。

【質問時用メモ】
・「仕様書に前提を書き足せば？」への回答：散文の書き足しは第二の翻訳で前提脱落が再発する。抜け漏れなしの一覧は証明の中にだけある。
・「spec-testsで共有できているのでは？」への回答：spec-testsは特定入出力（HOW）を見るだけで前提（WHEN）のアサーションがなくブラックボックス。

---

<p class="section-tag">従来の問題点</p>

## 問題の入口：確認できるのは、仕様に出たものだけ

<p>さきほどの確認の流れをもう一度見る。<br>確認項目は<strong>仕様の文章から列挙する</strong>——つまり、こうなる：</p>

<div class="flow">
<div class="panel"><h3>仕様に書いてある</h3><p>手順・計算・状態の更新</p><p class="actor">→ 確認項目になる。誰かが見る</p></div>
<div class="arrow">vs</div>
<div class="panel"><h3>仕様に書いていない</h3><p>前提・適用条件・表現の限界</p><p class="actor">→ 項目にならない。誰も見ない</p></div>
</div>
<p class="message">計算が正しく書かれていても、その<strong>前提</strong>が文章に出ていなければ、<br><strong>監査チェックリストの「行」にすら載らない。</strong></p>
<p class="small">では実際に、文章に出ていない条件はあるのか——次は具体例です。</p>

Note:
前提が届かない結果、監査やテストの現場で何が起きているのか。
確認項目は仕様の文章から作られるので、文章に書いてある「手順」は項目になり、誰かが見ます。
一方、文章に書いていない「前提」は項目にならず、結果として誰も見ません。
現場は「仕様に書いてある手順（HOW）」しか確認できない見え方の限界を抱えています。
もし正しさに必要な前提条件（WHEN）が文章に出ていなかったら、その条件は監査の対象にすらなりません。
では実際に、仕様に出ていない条件はあるのでしょうか。
次に具体的な例を二つ見ます——一つは仮想例、もう一つは実際に起きた修正です。

---

<p class="section-tag">従来の問題点</p>

## 「2/3」は合っている。でも、何の2/3か？

<p>仕様：「総重みの2/3が支持すれば、<strong>正当化</strong>＝確かとみなす」<br>→　監査：「2/3の計算があるか」　→　コードは2/3（算術記述の一致を確認）</p>
<p class="small">コードが書くのは「名簿の計算手順」。<br><strong>その計算が安全を保証する前提（どの集合関係・どんな出席を想定したか）</strong>は書いていない。<br>同じ手順を写しても、<strong>前提の共有が崩れれば同じ方向に間違える</strong>。</p>
<p class="label">仮想例（説明用）：8人・等しい重みで集計（色付き＝支持、白＝対象内で非支持、灰＝対象外）</p>
<img class="scenario-visual" src="figs/scenario-denominators.svg" alt="実装Aは1〜6を、実装Bは3〜8を有権者（分母）とする（破線枠）。同じ仕様でも使う名簿が違うと分母がずれる。両方4/6だが分母も分子も重ならない">
<p class="message">両方とも4/6 ＝ 2/3。でも母集団が違えば、<strong>同じ保証は使えない。</strong></p>

Note:
仮想例です。実装AとBはどちらも仕様どおり2/3の算術を計算しています。
しかし参照する名簿（分母）がズレていれば、算術は正しくても安全性の保証は崩壊します。
差分テストでは拾えない共通前提のズレです。

【質問時用メモ】
・「実際のEthereumでこんな単純な分母ズレが起きるのか？」への回答：8人の図は説明用の模式例。実際のEthereumではバリデータ集合は数十万人規模でエポックごとに動的に変動し、フォーク発生時は枝ごとに別々の有効バリデータ名簿が存在する。どの名簿を分母とすべきかの前提が共有されていないと、まさにこの仮想例と同じ原理でズレが生じる。

---

<p class="section-tag">従来の問題点</p>

## 実例：計算は合った。でも状態がずれた

<p class="small">※前提の非明示が直接の原因とは示していない。<strong>同じ処理領域の修正の重大さを示す動機づけの例</strong>。</p>
<p class="label">監査が見たもの</p>
<p>「2/3の計算があるか」→ コードには2/3があった。<mark>ヨシ</mark></p>
<p class="label">実際に起きたこと（Nimbus #461）</p>
<div class="bitstrip"><span class="bitname">justification_bits</span><div class="bit">1</div><div class="bit">0</div><div class="bit stale">0</div><div class="bit stale">1</div><span class="stale-label">← 古いビットが残った</span></div>
<p>正当化履歴を保持する4bitの更新で上位ビットが残り、<strong>「確定」の判定に使う状態がずれた</strong>。<br>確定＝覆せない履歴とみなすこと。<br>実バグDBでは<strong>履歴の分裂（chain split）に至り得る</strong>と分類。</p>
<p class="message">算術は正しい。壊れていたのは、<strong>計算に渡す状態</strong>。</p>
<p class="source">Nimbus PR #461（公開・修正済、ethereum-vuln-dataset の impact_type=chain_split）。ずれた状態は、先ほどの仕様抜粋の最終行 justification_bits。</p>

Note:
実際に起きたNimbusの事故です。
2/3の計算は仕様どおりで監査もパスしていました。
しかし正当化履歴を扱う4bitマスクの暗黙前提が漏れ、チェーン分裂の危機に至りました。
壊れていたのは計算式ではなく、計算に渡す状態の暗黙前提でした。

【質問時用メモ】
・「前提の非明示がこのバグの直接原因（因果）なのか？」への回答：因果関係を直接立証するものではなく、同一の処理領域（justification_bitsの更新）に監査の盲点があったという位置的共起の例示。
・「Lighthouse #4576との違いは？」への回答：Lighthouseはデータ移行時のロック処理（並行処理バグ）であり、合意の安全性前提とは無関係（区別してスライド34で説明）。

---

<p class="section-tag">仮説</p>

## 仕様どおりの実装は、証明の前提まで満たさない

<p>証明は<mark>保証書</mark>と同じ構造。条件内は保証、<strong>条件外は対象外</strong>。</p>
<img class="scope-visual" src="figs/diagram-guarantee-scope.svg" alt="証明は保証書。「前提Pを満たすなら安全Qを保証」とあるが、届くのはPを満たす実装だけ。満たさない実装は保証対象外。どちらの実装にも同じ「仕様どおり」の印が押されている">
<div class="route"><span>問題</span><strong>同じ「仕様どおり」でも、前提が満たされるかは仕様を読むだけでは区別がつかない</strong></div>
<div class="route"><span>仮説</span><strong>前提には、仕様に書かれていないものがある</strong></div>
<div class="route"><span>提案</span><strong>証明から取り出して、確認項目として渡す</strong></div>
<div class="route"><span>その先</span><strong>監査者・実装者が前提まで確認 → ずれを早く摘み、履歴の分裂と資産損失を減らす</strong></div>
<p class="source">図は説明用の模式図。Lean＝証明を機械が検査する言語。入力：Ethereumの安全性をLean 4で形式化した <strong>gasper-lean4 の証明</strong>。</p>

Note:
証明は保証書と同じ構造です。
前提を満たす領域にだけ保証が効きます。
しかし仕様を読むだけでは、前提を満たしているか区別がつきません。
そこで、安全性の証明から前提を直接取り出して現場へ渡す、というのが本研究の提案です。

【質問時用メモ】
・「なぜ仕様を満たしても保証対象外になり得るのか？」への回答：仕様書は「こう動け」という手順（HOW）を教えるが、「証明が要求する数学的前提（WHEN）をそのコードが満たしているか」は仕様書には検証できないため。保証書の条件外で動かしてもエラーにはならないが、定理の保証（不可逆な確定）は失われる。

---

<p class="section-tag">提案</p>

## 足すのは「証明 → 前提 → 確認候補」の経路

<p>証明の中の「前提」という資産が、Leanの中に留まったまま。<br><strong>理論家の成果をエンジニアへ橋渡しし、有効性を試した。</strong></p>

<div class="route"><span>従来の入力</span><strong>仕様の記述 → 確認項目</strong></div>
<div class="flow extraction-flow">
<div class="panel purple"><h3>安全性の証明</h3><p>条件 ⇒ 保証</p><p class="actor">理論家の成果</p></div>
<div class="arrow">→</div>
<div class="panel"><h3>前提を抽出</h3><p><strong>定理の前提を列挙</strong></p><p class="actor">構文的・LLM不使用</p></div>
<div class="arrow">→</div>
<div class="panel blue"><h3>確認候補へ変換</h3><p>仕様・コードと対応付け</p><p class="actor">研究側が翻訳</p></div>
</div>
<p class="message">証明の専門家だけの成果を、<strong>実装者・監査者が参照できる前提一覧</strong>にする。</p>
<p class="small">実装者・監査者はLeanを読まず、<strong>翻訳済みの一覧を受け取る</strong>。抽出した条件には原典の定理への参照を残す。</p>

Note:
従来の仕様から項目を作る経路に加え、Lean 4の形式証明から前提を抽出する経路を追加します。
現場のエンジニアがLeanを読む必要はありません。研究側が日本語の確認候補へ変換して手渡します。

【質問時用メモ】
・「現場にLeanの学習コストを強いるのか？」への回答：現場はLeanを読まない。研究側が定理シグネチャから抽出・日本語化し、仕様箇所と紐付けたチェックリスト（またはJSON）を渡す。
・「前提の抽出にLLMは使っているのか？」への回答：抽出は一切LLM不使用。Lean 4の構文木（AST）から定理の型シグネチャ（コロン手前の仮説括弧群）を決定的にパースするため、捏造（ハルシネーション）は0%。LLMは後段の仕様明示判定のみで使用。
・「理論家に新たな負担を強いるのか？」への回答：強いない。前提は既存の形式証明の中にすでに正確に記述されているため、そこから機械的に取り出すだけ。

---

<p class="section-tag">提案</p>

## 提案手法のスコープ：何をして、何をしていないか

<p>「要は、仕様に足りない情報を証明から足して、確認項目はAIに作らせる話？」<br>半分正しいです。<strong>どこを機械化し、どこを信用しないか</strong>が設計の要点です。</p>

<table>
<thead><tr><th>工程</th><th>方法</th><th>なぜそうするか</th></tr></thead>
<tbody>
<tr><td>前提の抽出</td><td><strong>機械的・LLM不使用</strong></td><td>生成させると、証明に存在しない前提が混ざる。定理文の構文を読むだけなら捏造が起きない</td></tr>
<tr><td>仕様への明示判定</td><td><strong>LLM＋照合器（複数）</strong></td><td>文章の言い換えを機械だけでは拾えない。ただし判定は一致度であり正解ラベルではない</td></tr>
<tr><td>確認候補の実効性</td><td><strong>未検証</strong></td><td>監査で実際にバグを拾えるかは、まだ示していない（正直な限界）</td></tr>
</tbody>
</table>
<p class="message">証明からの一次情報だけは人の翻訳に委ねず、<br><strong>抜け漏れなくそろった一覧を出す</strong>のが貢献です。</p>

Note:
設計の要点は、どこを機械化し、どこを信用しないかです。
前提の抽出にはLLMを使わず決定的な構文解析で行い捏造を防ぎます。
一方、実際の監査でバグを拾えるかの実効性検証は今後の課題であり、本研究では「仕様書に前提が定量的に欠落している事実」の解明に集中しています。

【質問時用メモ】
・「要するにAIに確認項目を作らせる研究か？」への回答：半分正しく半分誤り。明示判定にはLLM群を使うが、前提の抽出には生成AIを一切使わない。生成AIに前提を抽出させると存在しない前提を幻覚するため、定理の構文を機械的に読むことで完全かつ捏造のない一覧を保証している。
・「実バグを検出できたのか？」への回答：本研究（予備調査）ではバグ検出実効性の定量的評価は未実施。今回は仕様と証明の乖離を測定したMeasurement Study（測定研究）であり、検出性能の評価は今後の課題。

---

<p class="section-tag">提案</p>

## 実例：定理に書かれた「条件」の部分を取り出す

<div class="grid" style="margin-bottom: 10px;">
<div><h3 style="margin: 0 0 8px;">定理文の、コロンの手前を抜き出す</h3><div class="proof-code tight" style="padding: 8px 12px; font-size: 15px;"><div class="muted">theorem quorum_intersection_weight_lower</div><div class="muted">　{ qL qR vL vR : … }  -- 部品（除外）</div><div>　( hqLsub : <mark>qL ⊆ vL</mark> )</div><div>　( hqRsub : <mark>qR ⊆ vR</mark> )</div><div>　( hqLwt : <mark>τ.two_third (wt stake vL) ≤ wt stake qL</mark> )</div><div>　( hqRwt : <mark>τ.two_third (wt stake vR) ≤ wt stake qR</mark> )</div><div class="muted">　: 結論（保証）</div></div><p class="small" style="margin: 4px 0 0; font-size: 18px;">括弧群＝前提（Leanでは仮説）。構文的に列挙し実体条件を選別。</p></div>
<div class="premise-list"><h3 style="margin: 0 0 8px;">取り出される前提の意味</h3><div class="premise" style="padding: 6px 10px; margin-bottom: 6px; font-size: 20px;"><p style="margin: 0;"><strong>① 参加者集合の包含：</strong><br>支持した参加者が、その側の集計対象に含まれる。</p></div><div class="premise" style="padding: 6px 10px; margin-bottom: 6px; font-size: 20px;"><p style="margin: 0;"><strong>② クォーラムの重み閾値：</strong><br>その対象の総重みに対して、2/3以上の重みが支持する。</p></div><p class="small" style="margin: 4px 0 0; font-size: 18px;">この条件を、<strong>両側（フォーク双方）</strong>で満たす必要がある。</p></div>
</div>
<p class="message" style="margin: 10px 0 6px; font-size: 28px;">「2/3」という数字だけでなく、<br><strong>どの参加者集合・どの重みを使うか</strong>まで前提に含まれる。</p>
<p class="source" style="margin-top: 6px;">原典：<a href="https://github.com/NyxFoundation/gasper-lean4/blob/7650709/GasperBeaconChain/Core/Theories/SlashableBound.lean">quorum_intersection_weight_lower / gasper-lean4 @ 7650709</a>。原ソースの仮説4式を示す。日本語は説明用の要約。</p>

Note:
実際のGasperの安全性定理です。左の数式を覚える必要はありません。
コロンの手前にある括弧群から、「支持者が集計対象に含まれるか」「総重みの2/3以上が支持したか」という2つの実体条件を、決定的な構文解析で取り出します。

【質問時用メモ】
・「波括弧 { } と丸括弧 ( ) の違いは？」への回答：波括弧はLeanの暗黙引数（型やモデルのパラメータ・部品）であり、実体的な検証条件ではないため機械的に除外。丸括弧内の実体条件のみを抽出。
・「両側の参加者集合が同一であることを要求しているのか？」への回答：同一を常に要求する定理ではない。異なる参加者集合であっても、その交差関係（包含と重なり）に応じて下限を評価する定理であり、動的バリデータ変動を数学的に扱える。

---

<p class="section-tag">提案</p>

## 前提を、監査で扱える確認候補へ変換する

<div class="grid tl">
<div><p class="label">人が読む形（確認一覧）</p><table>
<thead><tr><th>取り出した条件</th><th>確認候補（例）</th></tr></thead>
<tbody>
<tr><td>支持者が集計対象に含まれる</td><td>票の出所と参加者集合が対応しているか。</td></tr>
<tr><td>対象の総重みの2/3以上が支持</td><td>分母と分子の重みを、どの状態から計算しているか。</td></tr>
<tr><td>集合の関係に応じて保証を評価</td><td>参加者の入れ替わり時に、どの集合・重みをモデル化しているか。</td></tr>
</tbody>
</table></div>
<div><p class="label">ツールが読む形（SPECA等の入力）</p><pre class="json-snippet"><code class="language-json">{
 "property_id": "CHK-GEN-09",
 "severity": "CRITICAL",
 "lean_status": "descends-from-proved",
 "lean_artifact": "AccountableSafety.lean#…",
 "spec_reference": "beacon-chain.md#…",
 "lean_must_establish": [
  "¬ q_intersection_slashed …",
  "k_finalized …", "justified …" ]
}</code></pre></div>
</div>
<p class="message">人には<strong>確認一覧</strong>、監査ツールには<strong>JSON</strong>を渡す。<br>どちらも、条件・原典の定理・仕様の参照先がつながっている。</p>
<p class="small">右は実際の成果物形式（実データ）。左の対応付けは使い方の例で、バグ検出性能は別途検証する。</p>

Note:
取り出した前提を、人間用の確認一覧と、監査ツール（SPECA等）用のJSONに変換します。
現場のエンジニアが読むのは左側の日本語一覧だけで十分です。
前提条件・原典の定理・仕様書の参照先が1本のパイプラインで結ばれます。

【質問時用メモ】
・「descends-from-provedとはどういう意味か？」への回答：「この確認項目自体が検証済み」という意味ではなく、「証明済みの定理から機械変換で降りてきた」という来歴（provenance）を示す。誤読を避けるため derived-unverified への改名も妥当な指摘。
・「重要度（CRITICAL等）はどう決めているのか？」への回答：仕様書の記述量ではなく、安全性定理の依存関係（不成立時にチェーン分裂が起きるか等）の数学的構造から決定。
・「現場への丸投げでは？」への回答：生の前提ではなく、重要度・仕様参照先・分類を同梱して渡す。現場に残る作業は「自チームのコードのどこで担保するか」の割当のみ。

---

<p class="section-tag">仮説の検証</p>

## 抽出した前提は、仕様に明示されているか

<div class="flow">
<div class="panel purple"><span class="number">17</span><h3>対象の定理</h3><p class="small">定理ごとに仮説を列挙<br>原典と照合</p></div>
<div class="arrow">-></div>
<div class="panel"><span class="number">57</span><h3>延べ前提条件</h3><p class="small">複数の条件を対応付け<br>同一概念の反復を含む</p></div>
<div class="arrow">-></div>
<div class="panel blue"><span class="number">89</span><h3>仕様ファイル</h3><p class="small">文章の安全性要件と照合</p></div>
</div>
<div class="grid"><div class="panel"><h3>前提の抽出</h3><p>証明の仮説から機械的に列挙。<br>LLMで自由生成しない。</p></div><div class="panel"><h3>明示の判定</h3><p>キーワード照合器と6種類のLLM。<br>仕様の文章に等価な安全性要件があるか。<br>操作的に書かれた要件も「明示」と判定。</p></div></div>
<p class="source">gasper-lean4 @ 7650709 / consensus-specs @ 2359a5e。57は重複を含む延べ件数。</p>

Note:
抽出した延べ57件の前提が、89の仕様ファイルの文章に安全性要件として明示されているかを照合しました。
判定にはキーワード照合器に加え、6種類のLLM群を併用し、操作的な手順として書かれた要件も「明示」とカウントして客観的に自動判定しました。

【質問時用メモ】
・「57件は何の数か？」への回答：確認項目に対応付けた前提の延べ数。独立した要件数でもバグ数でもない。同じ概念の反復を整理すると10概念。
・「判定器のバイアスや利益相反は？」への回答：キーワード照合器は著者設計のため利益相反を否定できない。そのため独立した6つのLLM（GPT-4o, Claude等）を並行動作させた。判定器間の一致度は0.913（PABAK 0.826）と高いが、人手正解ラベルとの照合は今後の課題。
・「判定の基準は？」への回答：「厳密に同一の数学的記述があるか」ではなく「操作的な手順であっても同等の安全性要件が文章から読み取れるか」という甘めの基準で判定している。

---

<p class="section-tag">この研究の優位性</p>

## 10概念中7概念は、仕様の文章に非明示と判定

<img class="result-visual" src="figs/chart-premises.svg" alt="48/57件、84.2%のドーナツ図と57マス。青48マスは全自動判定で非明示、橙9マスは判定が分かれた" style="height:250px">
<div class="route"><span>具体例</span><strong>証明の中心概念は仕様側で別名に分散（supermajority等）——用語レベルでも断絶</strong></div>
<p class="message">仕様からの項目作りだけでは、<br><strong>証明の前提を拾いきれない可能性</strong>を示した。</p>
<p class="small">延べ57件中48件（84.2%）が非明示。「明示」と全員一致した条件は0件。<br>同一前提が多定理で繰り返し要求される＝<strong>根幹を支える急所</strong>の裏付け。実装のバグ数ではない。</p>

Note:
測定結果です。延べ57件中48件（84.2%）、概念数で見ると10概念中7概念が、仕様書に非明示と判定されました。全員一致で明示とされた条件は0件です。
仕様書を読むだけでは、安全性を支える前提の8割以上が現場に届かないという実態が明らかになりました。

【質問時用メモ】
・「割れた3概念（9件）は何だったのか？」への回答：justified・finalized・votes_from_target_vset_propertyの3つ。仕様書に状態変数（state.current_justified_checkpoint等）として存在するため、「状態の定義」と「安全性要件としての明示」の境界で判定が割れた。
・「単にquorumという単語が仕様にないだけでは？」への回答：単語の有無ではなく、証明の中心概念が仕様側ではsupermajorityやtotal_active_balanceといった別名に分散し、理論と仕様の間で用語レベルの断絶があることが本質。
・「48件のバグを見つけたという意味か？」への回答：違う。バグ数ではなく「仕様の文章から項目を作る従来の監査では、証明の前提の8割がチェックリストから抜け落ちる」という構造的測定結果。

---

<p class="section-tag">適用の一例</p>

## 前提を確認する領域に、実際の修正もある

<p class="small">次は、集計結果を保存する状態の扱い。<strong>Nimbus #461</strong>：4ビットの履歴に余分な桁が残る。</p>
<div class="grid">
<div class="panel orange"><div class="label">修正前 / PR差分</div><pre><code class="language-nim">state.justification_bits =
  state.justification_bits shl 1</code></pre><p>左へずらすだけ。</p><p class="small"><code>1000 → 10000</code></p></div>
<div class="panel blue"><div class="label">修正後 / PR差分</div><pre><code class="language-nim">const JUSTIFICATION_BITS_LENGTH = 4
state.justification_bits =
  (state.justification_bits shl 1) and
  cast[uint8](
    (2^JUSTIFICATION_BITS_LENGTH) - 1)</code></pre><p class="small">下位4ビットだけ残す。<br><code>1000 → 0000</code></p></div>
</div>
<p class="message">計算手順に加え、<strong>状態の表現範囲</strong>も確認する。</p>
<p class="source"><a href="https://github.com/status-im/nimbus-eth2/pull/461/files">Nimbus PR #461</a>（2019年、改行のみ調整）。同一ラベルへの位置的共起のみで、因果は主張しない。</p>

Note:
抽出した前提領域は、Nimbus PR #461で実際にチェーン分裂危機を引き起こした修正領域（justification_bitsの更新）と位置的に一致していました。
壊れていたのは計算式ではなく、状態のビットマスクという暗黙前提でした。

【質問時用メモ】
・「前提漏れがNimbusバグの直接原因（因果）なのか？」への回答：因果関係を直接立証するものではなく、同一の処理領域（justification_bitsの更新）に監査の盲点があったという位置的共起の例示。
・「Lighthouse #4576との違いは？」への回答：Lighthouseはデータ移行時のロック処理（並行処理バグ）であり、合意の安全性前提とは無関係（区別してスライド33で説明）。
・「本手法はこのバグを再検出できるのか？」への回答：現時点では未検証。過去バグに対する回帰的検証実験を計画中。

---

<p class="section-tag">実務への展開</p>

## 前提ごとに「誰が何を確認するか」を決める

<p>ここからは次の行動。<strong>取り出した前提を、仕様・コードへ対応付け、<br>担当と確認方法を割り当てる</strong>。</p>

<div class="grid">
<div class="panel blue"><h3>実装で確認する</h3><p>票の出所と集計対象の対応。<br>総重み・支持重みの計算。<br>状態の表現範囲。</p><p class="small">コード・テスト・レビューへ。</p></div>
<div class="panel purple"><h3>モデル・環境として確認する</h3><p>参加者の入れ替わり。<br>想定する違反者の規模。<br>どの条件下の保証を使うか。</p><p class="small">設計・運用・証明の適用範囲へ。</p></div>
</div>
<p class="message"><strong>すべての前提を単一のassertに変換するわけではありません。</strong><br>条件の意味に応じて、確認の責任と手法を正しく割り当てます。</p>

Note:
取り出した前提をどう実務へ展開するか。
すべての前提を単一のassertに変換するわけではありません。
コードが担保すべき不変条件と、運用や設計が担保すべき環境仮定へ、責任を正しく割り振ります。

【質問時用メモ】
・「現場に丸投げでは？」への回答：渡すのは生の前提の羅列ではなく、分類（実装要件か環境仮定か）・重要度・定理参照・仕様アンカーを同梱した項目。現場に残る作業は分析ではなく組織に応じた担当の割当。組織ごとにアーキテクチャが異なる以上、割当自体を中央集権的に機械化することは本質的にできない。

---

<p class="section-tag">実務への展開</p>

## 実装者：前提をテスト・レビューへ落とす

<div class="grid">
<div class="panel"><h3>例：集計の分母は前提で名指しされた集合か</h3><p>証明から取り出した仮説を、<br>そのまま不変条件にする。</p><p class="small">Leanの仮説 <code>q ⊆ v</code>・<code>2/3·wt(v) ≤ wt(q)</code> と1対1。<br>どの定理由来かをコメントに残す。</p></div>
<div class="panel blue"><div class="label">提案するテスト例 / 関数名は仮・実現可能性の実演</div><pre><code class="language-python">def test_denominator(state, epoch):
    v = validators(state, epoch)
    tally = tally(state, epoch)
    # 前提: q ⊆ v
    assert tally.voters &lt;= set(v)
    # 前提: 2/3·wt(v) ≤ wt(q)
    assert 3 * tally.wt &gt;= 2 * total_wt(v)</code></pre></div>
</div>
<p class="message">前提 → 対応する状態・処理 → テスト／レビュー。</p>

Note:
実装者の使い方です。
証明から取り出した仮説を、そのまま単体テストや不変条件のアサーションとしてコードに落とし込みます。
どの定理に由来するかの参照コメントを残すことで、仕様の背景にある数学的保証とコードが直結します。

【質問時用メモ】
・「右側のテストコードは実在するのか？」への回答：説明用の疑似コードであり、関数名等は仮のもの。Leanの仮説（q ⊆ v, 2/3 wt(v) ≤ wt(q)）と1対1に対応するテストがPython/Rust等で直感的に書けることを示す実現可能性の実演。
・「テストの自動生成はしないのか？」への回答：自動生成は可能だが、本研究の主眼は「確認すべき前提一覧の供給」。生成器の検証は別課題。

---

<p class="section-tag">実務への展開</p>

## 仕様を書く人：対応表は仕様の外に置く

<table>
<thead><tr><th>記すもの</th><th>投票集計を例にした記述案</th></tr></thead>
<tbody>
<tr><td><strong>手順</strong></td><td>支持する重みを集計し、閾値と比較する。</td></tr>
<tr><td><strong>対象・状態の前提</strong></td><td>どの参加者集合を対象に、どの状態の総重みを分母に使うかを参照できるようにする。</td></tr>
<tr><td><strong>保証との接続</strong></td><td>仕様本文は手順に留め、証明・モデルとの対応表を<strong>別成果物</strong>として置く。</td></tr>
<tr><td><strong>環境の仮定</strong></td><td>参加者の入れ替わりや攻撃者の規模を、実装の処理要件とは区別して記す。</td></tr>
</tbody>
</table>
<p class="message">実装者が<strong>「何を・どこで・どう確認するか」</strong>をたどれる仕様へ。</p>

Note:
仕様策定者への提案です。
仕様書本文はシンプルな手順記述にとどめ、証明との対応表を別成果物として横に置くことで関心の分離を保ちます。
これにより、仕様の読みやすさを損なわずに実装者が前提をたどれるようになります。

【質問時用メモ】
・「仕様書の中に直接書けばいいのでは？」への回答：仕様書に学術的な注釈や定理の数式を埋め込むと、実装手順書としての可読性とシンプルさが失われる。仕様本文（手順）と対応表（数学的前提）を別成果物として分離することが、エンジニアリングと理論の双方にとって最も持続可能。
・「書き足すだけなら従来と同じでは？」への回答：出所が異なる。人間の記憶や解釈で書き足すのではなく、機械検査済みの形式証明から抽出した仮説を一次情報とするため、抜け漏れのない対応表が保証される。

---

<p class="section-tag">実務への展開</p>

## 共通仕様から作る、他のシステムでも考えられる

<div class="grid three">
<div class="panel"><h3>分散合意<br>Raft / Paxos</h3><p>メンバーシップ動的変更</p><p class="hypothesis"><strong>確認候補：</strong><br>新旧構成の共存期でも、<br>クォーラム交差の前提が<br>満たされているか。</p></div>
<div class="panel"><h3>BFT合意<br>Tendermint 等</h3><p>有権者集合の動的変動</p><p class="hypothesis"><strong>確認候補：</strong><br>各エポックでアクティブな<br>有権者集合の定義が<br>全実装で一致しているか。</p></div>
<div class="panel"><h3>分散プロトコル<br>形式仕様モデル</h3><p>ネットワーク環境前提</p><p class="hypothesis"><strong>確認候補：</strong><br>部分同期性や通信順序の<br>数学的前提がコードの<br>仮定と合致しているか。</p></div>
</div>
<p class="message">「共通仕様＋独立した複数実装」を持つシステム全般で、<strong>証明の前提を抽出する枠組み</strong>が有効。</p>
<p class="source">単一仕様とマルチクライアント構成を持つ分散システム一般への適用可能性の考察。</p>

Note:
このアプローチはイーサリアムに限りません。
Raftの動的メンバーシップ変更や、Tendermintの有権者集合変動など、「単一の仕様と複数の独立実装」を持つ分散システム全般に拡張可能です。

【質問時用メモ】
・「他システムでの検証はしたのか？」への回答：現時点ではイーサリアム（Gasper）での予備調査のみ。TendermintやHotStuffなど、形式仕様と複数クライアントを持つBFT系プロトコルへの適用を今後の研究計画として位置づけている。

---

<p class="section-tag">まとめ</p>

## 証明の成果を、現場が参照できる形へ

<img class="architecture-visual" style="height: 240px; margin: 6px auto; display: block;" src="figs/diagram-proof-handoff.svg" alt="証明の成果を現場が参照できる形へ：形式証明から抽出された前提条件を、現場が使えるテスト項目・監査チェックリストへ変換するパイプライン">
<p class="takeaway" style="margin-top: 10px; padding: 12px 18px; font-size: 24px;"><strong>形式手法の成果を現場の実務へ還元：</strong><br>現場のエンジニア全員がLeanを習得する必要はありません。<br>前提条件の自動抽出が、研究と実装・監査をつなぐインターフェースになります。</p>
<p class="source" style="margin-top: 8px;">提案アーキテクチャ：定理証明（Lean 4）からテスト・監査チェックリストへの前提条件抽出パイプライン</p>

Note:
本研究の意義は、形式手法の成果を専門家だけのものにせず、現場の実装・監査へ還元するパイプラインを確立した点にあります。
エンジニア全員がLeanを勉強する必要はありません。前提の自動抽出が、理論と現場をつなぐインターフェースになります。

【質問時用メモ】
・「今後の具体的な検証計画は？」への回答：①著者から独立した人手正解ラベルによる判定精度の検証、②ethereum-vuln-datasetの過去バグ（Nimbus PR #461等）に対する項目の再演・再検出実験、③他プロトコルへの展開。

---

<p class="section-tag">まとめ</p>

## まとめ：安全性の証明から、前提を取り出そう

<p class="summary">仕様を読むだけの確認に、<br>証明が要求する前提を足す。</p>
<div class="grid three">
<div class="panel"><h3>提案</h3><p>定理の前提を機械抽出し、<br>確認候補へ変換する。</p></div>
<div class="panel blue"><h3>調査結果</h3><p>延べ57件中48件は、<br>仕様の文章に非明示と判定。</p></div>
<div class="panel"><h3>次の行動</h3><p>前提を仕様・コードへ対応付け、<br>担当と確認方法を決める。</p></div>
</div>
<p class="small"><strong>今後：</strong>人手の正解ラベルによる検証、実バグでの再検出実験、他のBFT系への展開。<br>ご清聴ありがとうございました。</p>

Note:
まとめです。仕様書だけでは84.2%の前提が欠落しています。
定理証明から前提を取り出し、実装・監査のチェック項目へ渡すことで、共通仕様の解釈ズレとチェーン分裂を未然に防ぎます。
ご清聴ありがとうございました。質疑応答に移ります。

【質問時用メモ】
・質疑応答全般の想定問答は補足スライドおよび materials/想定問答.md を参照。

---

<p class="section-tag">補足</p>

## 補足：仮想例は、何を示しているか

<table>
<thead><tr><th></th><th>集計対象</th><th>支持者</th><th>対象に対する割合</th></tr></thead>
<tbody><tr><td>実装A</td><td>1, 2, 3, 4, 5, 6</td><td>1, 2, 3, 4</td><td>4/6 = 2/3</td></tr><tr><td>実装B</td><td>3, 4, 5, 6, 7, 8</td><td>5, 6, 7, 8</td><td>4/6 = 2/3</td></tr></tbody>
</table>
<p>支持者の重なりは0人。全8人に対しては、両方とも4/8。</p>
<div class="panel"><p>同じ全体を使う場合の「重なりは1/3以上」という直感を、<br>違う分母の集計に無条件で適用できない。</p></div>
<p class="small">集計部分を切り出した仮想例。この対象選択が仕様に準拠するとも主張していない。Ethereumの確定には投票間の関係・状態更新・検証など追加の条件があり、実ネットワークの事故を再現していない。</p>

Note:
（補足スライドのため発表中はスキップ。質問時に表示）

【質問時用メモ】
・仮想例は「2/3の計算だけでは、全体の定義や参加者の入れ替わりを確認できないこと」を示すための原理的解説。
・異なる集合を使うこと自体が常に違反なのではなく、原典の定理は異なる参加者集合も扱い、集合の交差に応じた下限を与える。
・この仮想例の集計対象は4人で重なるが支持者は0人で重なる。その場合に1/3の重なりを無条件で期待することが誤り。

---

<p class="section-tag">補足</p>

## 補足：原典の定理と、抽出する仮説

<table>
<thead><tr><th>定理・補題</th><th>保証の意味</th></tr></thead>
<tbody>
<tr><td><code>quorum_intersection_weight_lower</code></td><td>二つの支持者集合の重なりを、参加者集合の重なりと閾値から下側に評価する。本編の抽出例。</td></tr>
<tr><td><code>k_safety'</code></td><td>両立しない履歴が確定したなら、二つの支持集合の交差がモデル上の違反判定の対象になる。</td></tr>
<tr><td><code>slashable_bound</code></td><td>違反判定対象の重みを、参加者の入れ替わりも含めて下側に評価する。</td></tr>
<tr><td><code>no_k_finalized_justified_same_height</code></td><td>指定した前提のもとで、確定した記録と別の支持された記録は同じ高さに並ばない。CHK-GEN-09の母定理。</td></tr>
</tbody>
</table>
<p class="source">gasper-lean4 @ 7650709。確定を支える投票ルールは Casper FFG と呼ばれる。定理の成立と、実装・現実へのモデルの適用は区別する。</p>

Note:
（補足スライドのため発表中はスキップ。質問時に表示）

【質問時用メモ】
・本編の例はSlashableBound.leanにある定理の仮説（包含2式、重み閾値2式）。
・57件は確認項目に対応付けたmust-establish一覧の延べ件数であり、原典の全仮説行の単純総和ではない。
・定理を検査するLeanのカーネルが受理しても、モデルが現実を忠実に表すことまで自動保証されるわけではない（忠実性ギャップ）。

---

<p class="section-tag">補足</p>

## 補足：結果の意味と、まだ評価していないこと

<div class="grid">
<div class="panel"><h3>測ったこと</h3><p>証明由来の前提が、<br>仕様の文章に安全性要件として<br>明示されているか。</p></div>
<div class="panel orange"><h3>まだ測っていないこと</h3><p>実装のバグ数。<br>追加項目のバグ検出性能。<br>他分野でも同じ割合になるか。</p></div>
</div>
<p class="small">延べ57件・10概念。48件（7概念）は非明示に一致、9件は判定が分かれた。判定器はすべて自動で、正式な人手評価は今後の課題。判定器間の一致率は0.913（PABAK 0.826）だが、判定器「間」の一致であって正解との一致ではない。判定器の設計者は著者であり利益相反も否定できない。</p>
<p class="small">非明示は「コードにも存在しない」とは限らない。前提には実装で保つ条件、脅威モデルの仮定、証明の補助条件が含まれる。仕様には安全性の帰結を非形式に述べる文書（弱件性・高速確定）はあるが、分解された前提を検査可能な要件としては与えていない。</p>

Note:
（補足スライドのため発表中はスキップ。質問時に表示）

【質問時用メモ】
・判定器間の一致率は0.913（PABAK 0.826）だが、判定器どうしの一致であり正解ラベルとの一致ではない。
・キーワード照合器の設計者は著者自身なので利益相反も否定できない。独立した6つのLLM併用は緩和策。
・仕様に非明示であることは実装の脆弱性や仕様の誤りを直接証明するものではない。

---

<p class="section-tag">補足</p>

## 補足：同じ処理領域にあることと、同じ原因は別

<div class="grid">
<div class="panel"><h3>Nimbus #461</h3><p>正当化履歴のビット処理を修正。<br>下位4ビットを残すマスクを追加。</p></div>
<div class="panel"><h3>Lighthouse #4576</h3><p>確定に伴うデータ移行で、<br>同じロックを二度取得する<br>デッドロックを修正。<span class="small">※並行処理バグで別種</span></p></div>
</div>
<p class="message">一部項目と実バグは同じ分類領域へ対応付けられる。<br>ただし領域の一致は「同じ種類のバグ」を意味しない。</p>
<p class="small">対応はデータセットの分類ラベルに基づく。コードパスの一致や、前提の非明示がバグを生んだという因果は示していない。前提の違いの仮想例とも別の話。</p>
<p class="source"><a href="https://github.com/status-im/nimbus-eth2/pull/461">Nimbus #461</a> ／ <a href="https://github.com/sigp/lighthouse/pull/4576">Lighthouse #4576</a></p>

Note:
（補足スライドのため発表中はスキップ。質問時に表示）

【質問時用メモ】
・Nimbus PR #461とLighthouse #4576は、同じ処理領域（合意・正当化）にあっても原因も障害クラスも異なる。
・Nimbusはビットマスク処理（合意状態の表現範囲）、Lighthouseはデータ移行時のロック処理（並行処理バグ）。
・位置的共起の例示であり、因果関係やバグ再検出の実効性を主張するものではない。

---

<p class="section-tag">補足</p>

## 想定される反論と答え

<table>
<thead><tr><th>反論</th><th>答え</th></tr></thead>
<tbody>
<tr><td>「単一実装なのに『実装差』は概念破綻」</td><td>2013年のBDB事故は0.7系と0.8系が<strong>同時にネットワークを走った</strong>事案。アップグレードの過渡期は事実上の複数実装状態で、「異なるルールブックのノードが同居してチェーンが裂けた」構造は本題と同型。</td></tr>
<tr><td>「理想化された前提は現場を救えない」</td><td>「1/3未満のビザンチン」「部分同期」はまさに<strong>運用で監視すべき環境前提</strong>。保証が効かない条件を現場が把握していなければ、クライアント集中リスクの警告も意味をなさない。既存の堅牢化の代替ではなく補完。</td></tr>
<tr><td>「差分ファジングで解決」</td><td>差分ファジングが見つけるのは<strong>実装間の不一致</strong>。全実装が同じ見えない前提を共有して同じ方向に間違える<strong>common-mode failure</strong>は検出できない。「正解」のオラクルは証明の前提が担う。併用するもので代替ではない。</td></tr>
<tr><td>「仕様書は手順書。前提が無いのは自明」</td><td>問題は「書かれていないこと」ではなく<strong>「確認項目の原料がどこにも無いこと」</strong>。仕様から監査項目を作る以上、そこに無い前提は検査されない。辞書の文法証明と違い、クォーラム交差の前提は実装の正当性に必須の事前契約。</td></tr>
</tbody>
</table>

Note:
（補足スライドのため発表中はスキップ。質問時に表示）

【質問時用メモ】
Q「仕様は手順書。前提が書かれてないのは自明」→ 主張は欠陥ではなく「確認項目の原料が無い」。監査項目は仕様の文章から作られる以上、そこに無い前提はチェックリストの行にならない。spec-tests合格は前提を満たす保証ではない。
Q「判定器のプロンプトが誘導」→ だからこそ一致率は「正解ラベル」ではなく「判定器間の一致度」と論文・スライドで明記。突き止めたのは「仕様書の文章と理論前提の間に、現在の自然言語処理やキーワード照合では埋められない大きな構文的・意味的断絶が存在する」という事実そのもの。
Q「Nimbusはこじつけ」→ 前提漏れが引き起こした因果は主張していない。重要なのは「まさに前提を抽出したその処理領域（justification_bitsの更新）で、実際にチェーン分裂に至る致命的バグが起きていた」という位置的共起の事実。理論的にも実装的にも最も事故が起きやすい「急所」であることが実バグの歴史からも裏付けられている。
Q「現場に丸投げ」→ 現場が一番困るのは「何を気をつければいいか分からない（未知の未知）」状態。本手法はそれを「この定理のこの条件を確認すればいい（既知の課題）」へ変換して渡す。assertか監視アラートかは組織のアーキテクチャ・運用体制で異なるため、確認責任の割当を現場が担うのは健全な「関心の分離」。
Q「前提の選別は主観的」→ 列挙は決定的、選別ルールは人が定義→認める。ルールは文書化・検査可能で項目ごと差し替え可。「明示」全員一致0件は線引きを変えても消えにくい観察。
Q「新バグは1つも見つかってない」→ 本研究はバグ探索ツールではなく「仕様と形式証明の間に生じる84.2%の前提欠落を世界で初めて測定したMeasurement Study」。物理学で言えば新粒子を見つける前に「測定器の目盛りと理論値のズレ」を明らかにした段階。この地図があるからこそ、次のステップで確度の高いバグハントが可能になる。
Q「手動マッピングはスケールしない」→ 対応表は一度作れば差分レビューで済む資産。識別子照合や埋め込み候補提示＋人間承認で段階的自動化可能。上限は形式化カバレッジ。
Q「LLM判定を誰が検証」→ 一致率は正解率ではないと明言。次は人手正解ラベルとの照合。
Q「57件は何の数」→ 重複を含む延べ数。独立要件でもバグ数でもない。概念なら10中7が非明示。
Q「証明自体が間違ってたら」→ 証明は機械検査済み。モデル→現実仕様の忠実性は人間が確認する問題で、アンカー＋ピン留めで第三者検査可能にしている。
Q「quorumが仕様に無いだけでは」→ 単語の有無ではなく、前提がsupermajority等の別名に分散し用語レベルで橋が架かっていない構造の話。
Q「仕様に書き足せばいい」→ 方向は正しい。ただし何を書くかの一次情報が無いと同じ漏れが再発する。証明の仮説は構造上抜け漏れが無い一覧。

---

<p class="section-tag">補足</p>

## 参照資料・イラスト・公式ロゴの出典

<div class="grid">
<div class="panel"><h3>仕様・証明・修正PR</h3><p class="small"><a href="https://github.com/ethereum/consensus-specs/tree/2359a5e">consensus-specs @ 2359a5e</a><br><a href="https://eips.ethereum.org/EIPS/eip-3675">EIP-3675</a><br><a href="https://github.com/NyxFoundation/gasper-lean4/tree/7650709">gasper-lean4 @ 7650709</a><br><a href="https://github.com/status-im/nimbus-eth2/pull/461">Nimbus #461</a> / <a href="https://github.com/sigp/lighthouse/pull/4576">Lighthouse #4576</a></p><p class="small">研究の対象・数値・限界は論文正本に基づく。</p></div>
<div class="panel"><h3>イラスト・ブランド素材</h3><p class="small"><a href="https://ethereum.org/en/assets/">ethereum.org / WT</a><br><a href="https://undraw.co/illustrations">unDraw / Katerina Limpitsouni</a>（<a href="https://undraw.co/license">利用条件</a>）<br><a href="https://github.com/rust-lang/rust-artwork/">Rust Foundation / Rust project</a>（<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>、変更なし）<br><a href="https://github.com/nim-lang/assets">Nim project</a> / <a href="https://dev.java/">Oracle / Java</a><br><a href="https://www.typescriptlang.org/branding/">Microsoft / TypeScript</a></p><p class="small">ロゴは各ブランドの識別用。推薦・提携を示さない。<br>取得元・ハッシュ・利用条件は <code>figs/*-sources.json</code>。</p></div>
</div>

Note:
（補足スライドのため発表中はスキップ。質問時に表示）

【質問時用メモ】
・原典と素材の出典（consensus-specs, gasper-lean4, Nimbus #461, Lighthouse #4576）。
・イラスト・ブランド素材の利用条件（unDraw, Rust Foundation CC BY 4.0, 各種ロゴ）。
・詳細ハッシュ・利用条件は figs/*-sources.json に記載。
