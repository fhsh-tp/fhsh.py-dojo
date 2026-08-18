# REFERENCE：三參數 pow —— 出貨用正解
n, k = map(int, input().split())
print(pow(2, n - k, 1000000007))
