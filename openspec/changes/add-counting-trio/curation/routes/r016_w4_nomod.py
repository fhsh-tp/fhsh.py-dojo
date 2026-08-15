# WRONG_ANSWER：忘記取餘數，直接輸出完整大整數
# 註：Python 3.11 起 int -> str 有 4300 位上限，n-k 大時這行會丟 ValueError
n, k = map(int, input().split())
print(2 ** (n - k))
