## 1. 補 reference_solution 與 Purpose

- [x] 1.1 記錄基準:pnpm build:pools 後取 docs/public/pools/password-check.bin 的 sha256(池檔實際名稱以 ls docs/public/pools/ 為準),供 1.3 比對池 byte-identical。驗證:hash 已輸出留存。
- [x] 1.2 在 docs/challenge/password-check.md frontmatter 新增 reference_solution(落實 spec「Reference solution covers password-check in content regression」):讀密碼、讀 K,for 迴圈逐行讀猜測,猜對印 OK 並 break,否則 for-else 印 LOCKED;不多讀任何行。驗證:pnpm test --run scripts/content-regression.test.ts 顯示 password-check 由 skip 轉為實跑且通過。
- [x] 1.3 驗證池內容不變(落實 spec「Pool generation request unchanged by the new field」):以 buildPoolRequest 對「現檔」與「移除 reference_solution 的副本」各建一次產生請求,序列化後逐位元組比對必須相同(加密池檔含隨機 nonce,檔案 hash 不可比,1.1 的基準僅供發現此事實的過程紀錄);同時把 openspec/specs/password-check-pool-gen/spec.md 的 Purpose 由 TBD 佔位補為正式描述。驗證:兩份請求序列化相同;Purpose 段無 TBD 字樣;pnpm test --run 全綠。
