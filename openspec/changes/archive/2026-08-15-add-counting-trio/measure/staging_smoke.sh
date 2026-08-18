#!/bin/zsh
# staging e2e 冒煙測試：對已部署的站台跑完三題的完整使用者旅程。
#
# usage:
#   BASE=https://staging.fhsh-py-dojo.pages.dev zsh measure/staging_smoke.sh
#   （預設就是上面這個 BASE；要驗生產站改傳 BASE 即可）
#
# 輸出：measure/staging-e2e.jsonl（逐筆原始觀測）。
# 判讀請跑 measure/staging_e2e_assemble.py——那支才是斷言牆，這支只負責觀測。
# 兩件事刻意分開：觀測腳本重跑會拿到新的牆鐘數字，斷言牆不該跟著漂移。
#
# 為什麼要對 staging 而不是本機 dev server：本機 `vitepress dev` 不送 COOP/COEP，
# 沒有 SharedArrayBuffer 就沒有中斷，apcs015 那條必死路線在那裡量到的不是同一個量。
#
# 每一步都自帶失敗訊號。本 repo 早先有腳本把每個指令導向 /dev/null，於是呼叫到
# 不存在的子指令也會靜默通過——這裡不允許任何一步安靜地失敗。

set -u
# 必須 export：下面的 measure.sh 是另起一個 zsh 跑的，它自己也讀 BASE 且預設值是
# http://localhost:8788。不 export 的話七次提交會全部連到本機的空 port，
# 而且失敗訊息只會說 "open failed"，看不出是打錯站台。
export BASE=${BASE:-https://staging.fhsh-py-dojo.pages.dev}
HERE=${0:a:h}
OUT=$HERE/staging-e2e.jsonl
export AGENT_BROWSER_SESSION=${AGENT_BROWSER_SESSION:-ct-staging}

: > $OUT
rec() { print -r -- "$1" | tee -a $OUT }

# eval 的傳輸層會把 payload 重新加引號，直接比對字面量會永遠比不中。
# 交給 Python 解到看見物件為止，不要在 shell 裡猜。
unwrap() {
  python3 -c '
import json, sys
v = sys.stdin.read().strip()
for _ in range(3):
    v = json.loads(v)
    if isinstance(v, dict):
        print(json.dumps(v, ensure_ascii=False)); break
else:
    sys.exit("unparseable payload")
'
}

typeset -A SLUG
SLUG[apcs015]=ap-layout-plan
SLUG[apcs016]=marquee-display-count
SLUG[apcs017]=fair-token-exchange

# ---------------------------------------------------------------- 上架 ------
agent-browser open "$BASE/apcs-challenges" >/dev/null || { rec '{"check":"listing","status":"FAILED","reason":"open failed"}'; exit 1 }
agent-browser wait --load networkidle >/dev/null 2>&1
TXT=$(agent-browser eval "document.body.innerText" 2>&1) || { rec '{"check":"listing","status":"FAILED","reason":"eval failed"}'; exit 1 }
for probe in apcs015 apcs016 apcs017 基地台佈點規劃 跑馬燈顯示計數 園遊會代幣兌換; do
  if print -r -- "$TXT" | grep -q -- "$probe"; then
    rec "{\"check\":\"listing\",\"probe\":\"$probe\",\"status\":\"OK\"}"
  else
    rec "{\"check\":\"listing\",\"probe\":\"$probe\",\"status\":\"FAILED\",\"reason\":\"not found in listing body text\"}"
  fi
done

# ------------------------------------------------------------ /c/ 別名 ------
for id in apcs015 apcs016 apcs017; do
  agent-browser open "$BASE/c/$id" >/dev/null || { rec "{\"check\":\"alias\",\"id\":\"$id\",\"status\":\"FAILED\",\"reason\":\"open failed\"}"; continue }
  # 別名在前端解析，載入當下的 URL 還不是最終值，必須輪詢而不是讀一次。
  FINAL=""
  for _ in {1..30}; do
    U=$(agent-browser get url 2>&1)
    case $U in (*${SLUG[$id]}*) FINAL=$U; break;; esac
    sleep 1
  done
  if [[ -n $FINAL ]]; then
    rec "{\"check\":\"alias\",\"id\":\"$id\",\"status\":\"OK\",\"final_url\":\"$FINAL\"}"
  else
    rec "{\"check\":\"alias\",\"id\":\"$id\",\"status\":\"FAILED\",\"reason\":\"never reached ${SLUG[$id]}\",\"last_url\":\"${U}\"}"
  fi
done

# ---------------------------------------------------------------- 掛載 ------
for id in apcs015 apcs016 apcs017; do
  agent-browser open "$BASE/challenge/${SLUG[$id]}" >/dev/null || { rec "{\"check\":\"mount\",\"id\":\"$id\",\"status\":\"FAILED\",\"reason\":\"open failed\"}"; continue }
  ED=""; BTN=""
  for _ in {1..60}; do
    R=$(agent-browser eval "!!document.querySelector('.cm-content')" 2>&1)
    [[ $R == *true* ]] && ED=1 && break
    sleep 1
  done
  # 編輯器掛上不等於提交鈕已進無障礙樹：冷頁面上後者明顯晚到，
  # 讀一次快照就斷言會在一個其實沒問題的頁面上誤報。
  for _ in {1..60}; do
    SNAP=$(agent-browser snapshot 2>&1) || break
    BTN=$(print -r -- "$SNAP" | grep "提交" | head -1 | grep -oE "e[0-9]+" | head -1)
    [[ -n ${BTN:-} ]] && break
    sleep 1
  done
  BODY=$(agent-browser eval "document.body.innerText" 2>&1)
  BADGE=no; print -r -- "$BODY" | grep -qi -- "$id" && BADGE=yes
  if [[ -n $ED && -n ${BTN:-} && $BADGE == yes ]]; then
    rec "{\"check\":\"mount\",\"id\":\"$id\",\"slug\":\"${SLUG[$id]}\",\"status\":\"OK\",\"editor\":true,\"submit_button\":true,\"id_badge\":true}"
  else
    rec "{\"check\":\"mount\",\"id\":\"$id\",\"slug\":\"${SLUG[$id]}\",\"status\":\"FAILED\",\"editor\":${ED:-null},\"submit_button\":\"${BTN:-none}\",\"id_badge\":\"$BADGE\"}"
  fi
done

# ---------------------------------------------------------------- 提交 ------
# 六條正解路線 + 一條必死路線。少了那條必死路線，這一整節就只證明了
# 「會過的會過」，證不出成本鑑別還活著——沒有負向控制就等於沒有檢查。
submit() {  # submit <slug> <solution> <label>
  zsh $HERE/measure.sh "$1" "$2" "$3" \
    | python3 -c 'import json,sys; r=json.loads(sys.stdin.read()); r["check"]="submit"; print(json.dumps(r, ensure_ascii=False))' \
    | tee -a $OUT
}
S=$HERE/solutions
submit ap-layout-plan        $S/s015_reference.py      015-reference
submit ap-layout-plan        $S/s015_rowscan_plain.py  015-rowscan-plain
submit ap-layout-plan        $S/s015_rowscan_helper.py 015-rowscan-helper
submit ap-layout-plan        $S/s015_rowscan_sum.py    015-rowscan-sum
submit marquee-display-count $S/s016_reference.py      016-reference
submit fair-token-exchange   $S/s017_reference.py      017-reference
submit ap-layout-plan        $S/s015_cellscan.py       015-cellscan-NEGATIVE

# ---------------------------------------------------------------- 洩題 ------
# 只掃 <script src> 是不夠的：VitePress 用動態 import() 拉路由 chunk，
# 那種探針會在一個其實從 chunk 洩出去的頁面上回報乾淨。掃頁面實際抓過的
# 每一個 js/mjs/json 資源。
LEAK_JS='(async () => {
  const urls = performance.getEntriesByType("resource").map(e => e.name)
    .filter(u => /\.(js|mjs|json)(\?|$)/.test(u));
  let hay = document.documentElement.outerHTML;
  let fetched = 0; const failed = [];
  for (const u of urls) { try { hay += await (await fetch(u)).text(); fetched++; } catch (e) { failed.push(u); } }
  const probes = {"015_blocked_fn":"def blocked(side)","015_comment":"逐列累加",
                  "016_working":"working = working * 2","017_step":"step = step * 3",
                  "generator_key":"sys.stdout.write"};
  const hits = {};
  for (const [k,v] of Object.entries(probes)) hits[k] = hay.includes(v);
  return JSON.stringify({check:"leak", slug: location.pathname, resources: urls.length,
                         fetched, failed, bytes: hay.length, hits});
})()'
for id in apcs015 apcs016 apcs017; do
  agent-browser open "$BASE/challenge/${SLUG[$id]}" >/dev/null || { rec "{\"check\":\"leak\",\"id\":\"$id\",\"status\":\"FAILED\",\"reason\":\"open failed\"}"; continue }
  agent-browser wait --load networkidle >/dev/null 2>&1
  sleep 3
  agent-browser eval "$LEAK_JS" 2>&1 | unwrap | tee -a $OUT
done

# 洩題探針的正向控制：這兩條字串一定在頁面上。若它們也是 false，
# 上面那一片乾淨只證明了探針壞掉。
agent-browser open "$BASE/challenge/${SLUG[apcs015]}" >/dev/null
agent-browser wait --load networkidle >/dev/null 2>&1; sleep 3
agent-browser eval '(async () => {
  const urls = performance.getEntriesByType("resource").map(e => e.name)
    .filter(u => /\.(js|mjs|json)(\?|$)/.test(u));
  let hay = document.documentElement.outerHTML;
  for (const u of urls) { try { hay += await (await fetch(u)).text(); } catch (e) {} }
  return JSON.stringify({check:"leak_control", bytes: hay.length, control: {
    title_zh: hay.includes("基地台佈點規劃"),
    body_prose: hay.includes("列差"),
    py_marker_present_somewhere: hay.includes("import sys")}});
})()' 2>&1 | unwrap | tee -a $OUT

# -------------------------------------------------------------- 新鮮度 ------
# 部署的必須是本次 change 的**最終**決策，不是中途草稿。少了這一節，
# 一份過期的 CDN 副本可以通過上面每一道檢查。
agent-browser eval 'JSON.stringify((function(){
  var t = document.body.innerText;
  return {check:"freshness", slug:"ap-layout-plan",
    n_bound_1000: t.indexOf("1000") >= 0,
    no_n_bound_3000: t.indexOf("3000") < 0,
    perf_note_ops: t.indexOf("超出單筆測資的執行量上限") >= 0,
    perf_note_not_time: t.indexOf("超出時間限制") < 0,
    table_k3: t.indexOf("28") >= 0};
})())' 2>&1 | unwrap | tee -a $OUT

# 答案表要收斂在 k=1..3。這一條刻意只讀「邊長 k」那張表：
# 整頁搜尋會命中範例輸出區塊，那裡本來就該有 k=4、k=5 的答案。
agent-browser eval 'JSON.stringify((function(){
  var tables = Array.from(document.querySelectorAll("table"));
  var t = tables.filter(function(x){ return x.innerText.indexOf("邊長 k") >= 0; })[0];
  if (!t) return {check:"freshness_table", found:false};
  var rows = Array.from(t.querySelectorAll("tbody tr")).map(function(tr){
    return Array.from(tr.children).map(function(td){ return td.textContent.trim(); });
  });
  return {check:"freshness_table", found:true, tables:tables.length, rows:rows};
})())' 2>&1 | unwrap | tee -a $OUT

print -r -- "--- 觀測完成，共 $(wc -l < $OUT | tr -d ' ') 筆 → $OUT"
print -r -- "--- 判讀請跑： python3 $HERE/staging_e2e_assemble.py"
