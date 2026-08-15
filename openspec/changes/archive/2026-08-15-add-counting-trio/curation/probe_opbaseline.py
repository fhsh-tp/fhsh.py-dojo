import sys

# 量測基線的「受量測對象」，不是量測腳本——所以它跟 routes/ 一樣留在 curation/，
# 由 plan015.py 以與各路線完全相同的方式跑一次，量出兩條地板（本檔只做讀入與輸出，
# 沒有任何演算法）：
#   * op 地板  -> measure/routes015.json 的 op_measurement_harness_baseline
#   * 牆鐘地板 -> measure/routes015.json 的 process_start_floor_cpython_ms，
#                用來把「最貴單筆牆鐘」拆成「啟動地板 + 演算法增量」。
# （舊註解說它是用來量 runpy 外殼約 2 萬 op 的開銷；op 計數收編到 verify/judge_ops.py
#   之後已不再走 runpy，外殼只剩個位數 op，該說法不成立，故重寫。）
n = int(sys.stdin.readline())
sys.stdout.write(str(n))
