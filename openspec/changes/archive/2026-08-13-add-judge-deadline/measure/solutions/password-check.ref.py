password = input()
k = int(input())
for _ in range(k):
    if input() == password:
        print('OK')
        break
else:
    print('LOCKED')
