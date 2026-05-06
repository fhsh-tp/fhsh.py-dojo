## 1. 前置確認

- [x] 1.1 讀取全部 54 個 challenge 檔案的 `id:` frontmatter，建立 slug→現有ID 的完整對照表並確認無遺漏
- [x] 1.2 確認 `docs/shared/challenge.data.ts` 僅從 frontmatter 讀取 id，無硬編碼 ID 引用

## 2. [Req: Per-chapter ID blocks are contiguous] 重新編號 Ch1 後段（ID 26-35 → 11-20）

- [x] [P] 2.1 將 `docs/challenge/odd-even.md` 的 `id: 26` 改為 `id: 11`
- [x] [P] 2.2 將 `docs/challenge/sign-check.md` 的 `id: 27` 改為 `id: 12`
- [x] [P] 2.3 將 `docs/challenge/bmi-classifier.md` 的 `id: 28` 改為 `id: 13`
- [x] [P] 2.4 將 `docs/challenge/quadrant-classifier.md` 的 `id: 29` 改為 `id: 14`
- [x] [P] 2.5 將 `docs/challenge/triangle-classify.md` 的 `id: 30` 改為 `id: 15`
- [x] [P] 2.6 將 `docs/challenge/quadratic-discriminant.md` 的 `id: 31` 改為 `id: 16`
- [x] [P] 2.7 將 `docs/challenge/taxi-fare.md` 的 `id: 32` 改為 `id: 17`
- [x] [P] 2.8 將 `docs/challenge/movie-ticket.md` 的 `id: 33` 改為 `id: 18`
- [x] [P] 2.9 將 `docs/challenge/date-validator.md` 的 `id: 34` 改為 `id: 19`
- [x] [P] 2.10 將 `docs/challenge/vending-change.md` 的 `id: 35` 改為 `id: 20`

## 3. [Req: Challenge ID continuity across Module 2] 重新編號 Ch2 前段（ID 11-25 → 21-35）

- [x] [P] 3.1 將 `docs/challenge/number-sum.md` 的 `id: 11` 改為 `id: 21`
- [x] [P] 3.2 將 `docs/challenge/repeat-greeting.md` 的 `id: 12` 改為 `id: 22`
- [x] [P] 3.3 將 `docs/challenge/factorial.md` 的 `id: 13` 改為 `id: 23`
- [x] [P] 3.4 將 `docs/challenge/countdown.md` 的 `id: 14` 改為 `id: 24`
- [x] [P] 3.5 將 `docs/challenge/odd-numbers.md` 的 `id: 15` 改為 `id: 25`
- [x] [P] 3.6 將 `docs/challenge/range-sum.md` 的 `id: 16` 改為 `id: 26`
- [x] [P] 3.7 將 `docs/challenge/collatz-steps.md` 的 `id: 17` 改為 `id: 27`
- [x] [P] 3.8 將 `docs/challenge/digit-counter.md` 的 `id: 18` 改為 `id: 28`
- [x] [P] 3.9 將 `docs/challenge/number-reverse.md` 的 `id: 19` 改為 `id: 29`
- [x] [P] 3.10 將 `docs/challenge/first-divisor.md` 的 `id: 20` 改為 `id: 30`
- [x] [P] 3.11 將 `docs/challenge/password-check.md` 的 `id: 21` 改為 `id: 31`
- [x] [P] 3.12 將 `docs/challenge/target-sum.md` 的 `id: 22` 改為 `id: 32`
- [x] [P] 3.13 將 `docs/challenge/skip-multiples.md` 的 `id: 23` 改為 `id: 33`
- [x] [P] 3.14 將 `docs/challenge/sum-skip-fives.md` 的 `id: 24` 改為 `id: 34`
- [x] [P] 3.15 將 `docs/challenge/digit-sum-skip.md` 的 `id: 25` 改為 `id: 35`

## 4. 驗證

- [x] 4.1 掃描全部 `docs/challenge/*.md` 檔案，確認 ID 1–54 無間隔、無重複，且 Ch1=1-20, Ch2=21-54
- [x] 4.2 確認 `docs/tutor/py/ch1/*.md` 和 `docs/tutor/py/ch2/*.md` 中無直接數字 ID 引用（僅 slug 引用）
