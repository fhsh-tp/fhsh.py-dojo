#!/usr/bin/env zsh
# 渲染觀測：對抽樣題目頁量四件事，把原始數字寫成 jsonl。
#
#   zsh openspec/changes/latex-challenge-notation/measure/render_observe.sh
#   BASE=http://localhost:4173 zsh .../render_observe.sh    # 換站台
#
# **這支只觀測，不判讀。** 斷言牆在 render_assert.py。兩支拆開的理由：重跑觀測會得到
# 新的數字（版面高度受字型載入時機影響），斷言牆不該跟著漂。
#
# 量測項目
# ========
# 1. mjx_count      —— 題敘面板裡的 mjx-container 個數
# 2. source_leaks   —— innerText 裡出現的 LaTeX 原始碼字串（應為空陣列）
# 3. bare_dollars   —— innerText 裡的錢字號個數（貨幣頁面才該大於 0）
# 4. line_test      —— 行內公式最多的那個區塊元素的高度 vs 行高 × 公式數
#                      這是 29e381c 那條 CSS 修正的回歸症狀：修正沒生效時，
#                      一個含 N 個行內公式的段落會從 1 行變成 N+1 行。
#
# 連不上站台時，紀錄裡的 status 會是 UNREACHABLE 並帶上原因。**不得**把連線失敗
# 記成「頁面沒有公式」——那會把設定錯誤說成內容壞掉。

set -u

BASE=${BASE:-http://localhost:5173}
OUT=${OUT:-$(dirname "$0")/render-verification.jsonl}

PAGES=(
  # 已完成的試點，含大量行內公式，是 line_test 的主要觀測對象
  pinball-track-predict
  exhibit-route-rebuild
  quadratic-discriminant
  # 本次轉換的四個高密度頁
  prize-order-code
  rank-code-backfill
  pillbox-reminder
  ap-layout-plan
  # 邊界案例
  movie-ticket          # 貨幣錢字號與數學錢字號同頁
  bmi-classifier        # 中文與公式混排
  print-farm-schedule   # 字面圖形留在反引號裡
  marquee-display-count # 約束原本被誤包在反引號裡
  target-sum            # 同頁有 ≤ 與 ≥
)

: > "$OUT"

JS='(() => {
  const doc = document.querySelector(".prose") || document.querySelector(".vp-doc") || document.querySelector("main") || document.body;
  const text = doc.innerText || "";
  const LEAKS = ["\\\\le", "\\\\ge", "\\\\times", "\\\\cdots", "\\\\cdot", "\\\\lfloor", "\\\\text{", "^{"];
  const containers = [...doc.querySelectorAll("mjx-container")];
  const inline = containers.filter((c) => getComputedStyle(c).display !== "block");

  // 逐一量出每個「含 2 個以上行內公式」的區塊佔了幾行。
  // MathJax 把變數渲染成數學斜體（例如 𝑁 = U+1D441），那是代理對；直接 slice 會從
  // 代理對中間切斷、產生孤兒代理字元，Python 端就丟 UnicodeEncodeError、整筆觀測靜默
  // 消失。所以摘要文字用 code point 為單位切，再清掉殘存的孤兒代理字元。
  const excerpt = (el) => Array.from(el.innerText || "").slice(0, 70).join("").replace(/[\uD800-\uDFFF]/g, "");
  const blocks = [];
  for (const el of doc.querySelectorAll("p, li, td, th")) {
    if (el.querySelector("p, li, td, th")) continue;   // 只量葉節點，避免巢狀重複計算
    const n = el.querySelectorAll("mjx-container").length;
    if (n < 2) continue;
    const cs = getComputedStyle(el);
    let lh = parseFloat(cs.lineHeight);
    if (!isFinite(lh)) lh = parseFloat(cs.fontSize) * 1.5;
    blocks.push({ tag: el.tagName.toLowerCase(), formulas: n, height: el.offsetHeight,
                  line_height: lh, lines: +(el.offsetHeight / lh).toFixed(2), text: excerpt(el) });
  }
  // tightest：行數最少的那一塊。CSS 修正生效時，一定找得到含多個公式卻只佔 1 行的區塊，
  //           這是「行內就是行內」的直接證據。
  // densest ：公式最多的那一塊。修正失效時它會膨脹到至少 公式數 + 1 行。
  const byLines = [...blocks].sort((a, b) => a.lines - b.lines);
  const byCount = [...blocks].sort((a, b) => b.formulas - a.formulas);

  return JSON.stringify({
    // 題敘面板的字數。整站殼層（只有導覽列、沒有內容）約 25 字元；判讀端用這個
    // 把「站台起錯了」跟「公式沒渲染」分開。踩過一次：`vitepress dev docs` 會去讀
    // 到另一份設定檔，端出一個沒有內容也不噴錯的殼，12 頁全數量到 mjx_count 0，
    // 看起來就像轉換把公式弄壞了。
    doc_len: text.length,
    mjx_count: containers.length,
    inline_count: inline.length,
    svg_display: [...doc.querySelectorAll("mjx-container > svg")].slice(0, 3).map((s) => getComputedStyle(s).display),
    source_leaks: LEAKS.filter((s) => text.includes(s)),
    bare_dollars: (text.match(/\$/g) || []).length,
    multi_formula_blocks: blocks.length,
    tightest: byLines[0] || null,
    densest: byCount[0] || null,
  });
})()'

for slug in "${PAGES[@]}"; do
  url="$BASE/challenge/$slug"
  if ! agent-browser open "$url" >/dev/null 2>&1; then
    print -r -- "{\"slug\":\"$slug\",\"status\":\"UNREACHABLE\",\"reason\":\"agent-browser open 失敗：$url\"}" >> "$OUT"
    continue
  fi
  # 輪詢到 MathJax 渲染完成為止。固定 sleep 會誤判：首次載入時 Pyodide／WASM／編輯器
  # 都在搶資源，2 秒後量到的 mjx_count 可能還是 0，判讀端就會把「還沒渲染完」說成
  # 「這頁沒有公式」。attempts 記進紀錄裡，慢的頁面看得見，不是被靜靜重試掉。
  attempts=0
  raw=""
  while (( attempts < 12 )); do
    (( attempts += 1 ))
    sleep 1
    raw=$(agent-browser eval "$JS" 2>&1 | tail -1)
    # agent-browser 把回傳值再包一層 JSON 字串，所以引號是跳脫過的（\"mjx_count\":3）。
    # 樣式寫成未跳脫的形式會永遠比對不中，於是每一頁都輪詢到上限、attempts 全是 12，
    # 看起來像「整站都很慢」。\\? 讓兩種形式都吃得到。
    if print -r -- "$raw" | grep -qE '\\?"mjx_count\\?":[1-9]'; then break; fi
  done
  print -r -- "$raw" | python3 -c "
import json, sys
slug, attempts = '$slug', $attempts
raw = sys.stdin.read().strip()
try:
    inner = json.loads(raw)          # agent-browser 把回傳值再包一層 JSON 字串
    if isinstance(inner, str):
        inner = json.loads(inner)
    inner['slug'] = slug
    inner['status'] = 'OK'
    inner['attempts'] = attempts
except Exception as exc:
    inner = {'slug': slug, 'status': 'UNPARSEABLE', 'reason': str(exc),
             'attempts': attempts, 'raw': raw[:400]}
# 一定要寫出一筆。任何例外都要變成可見的紀錄，不能讓某一頁靜默消失——
# 少一筆的觀測檔看起來就像那一頁「沒問題」。
try:
    line = json.dumps(inner, ensure_ascii=False)
except Exception as exc:
    line = json.dumps({'slug': slug, 'status': 'UNSERIALIZABLE', 'reason': str(exc)}, ensure_ascii=False)
print(line)
" >> "$OUT"
done

count=$(wc -l < "$OUT" | tr -d ' ')
expected=${#PAGES[@]}
print -r -- "觀測完成，$count 筆寫入 $OUT（預期 $expected 頁）"
if [[ "$count" != "$expected" ]]; then
  print -r -- "⚠️  筆數與頁數不符——有頁面連紀錄都沒寫出來，判讀前先查這個。"
  exit 1
fi
