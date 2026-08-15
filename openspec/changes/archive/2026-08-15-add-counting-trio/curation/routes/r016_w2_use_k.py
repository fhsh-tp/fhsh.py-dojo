# WRONG_ANSWER：把自由度看成 k 而不是 n-k
n, k = map(int, input().split())
print(pow(2, k, 1000000007))
