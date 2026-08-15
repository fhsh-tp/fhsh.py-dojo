# WRONG_ANSWER：沒看穿「燒壞的格子不算自由度」，直接算 2^n
n, k = map(int, input().split())
print(pow(2, n, 1000000007))
