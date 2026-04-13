---
layout: doc
title: Appendix
description: 模組二關鍵字補充表與 AI 圖片規格附錄
chapter: 2
---

# 模組二：關鍵字補充表

延續模組一的關鍵字表，以下是模組二新登場的 Python 關鍵字與內建函式。

## 新增關鍵字

| 關鍵字 | 中文簡述 | 首次登場 | 示例 |
|--------|----------|----------|------|
| `for` | 固定次數或逐元素迭代的迴圈 | 2-1 ✅ | `for i in range(10):` |
| `in` | 成員判斷，也是 `for` 迴圈的語法搭配詞 | 2-1 ✅ | `for x in range(5):` |
| `while` | 條件成立就持續執行的迴圈 | 2-2 ✅ | `while n > 0:` |
| `break` | 立刻跳出目前所在的迴圈 | 2-3 ✅ | `if found: break` |
| `continue` | 跳過本次迭代，直接進入下一輪 | 2-3 ✅ | `if n % 2 == 0: continue` |

## 新增內建函式與語法

| 語法 | 說明 | 登場章節 |
|------|------|----------|
| `range(n)` | 產生 0 到 n-1 的整數序列 | 2-1 ✅ |
| `range(start, stop)` | 產生 start 到 stop-1 的整數序列 | 2-1 ✅ |
| `range(start, stop, step)` | 以自訂步長產生整數序列 | 2-1 ✅ |
| `print(..., end="")` | 印出後不換行（覆蓋預設換行符） | 2-4 ✅ |
| `f"{value:4}"` | f-string 格式化：數值右對齊佔 4 格 | 2-4 ✅ |

---

## Image Specification Appendix

### 圖 1
- **類型**：四格漫畫（Hook）
- **意圖**：用「罰寫 100 遍」對比「for loop 兩行搞定」的荒謬反差，引發學生對迴圈的興趣
- **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: a stick figure teacher pointing at a blackboard with speech bubble saying 罰寫「我不會上課睡覺」100遍, panel 2: student stick figure at desk writing furiously surrounded by papers with speech bubble saying 第37遍...手好痠..., panel 3: another student stick figure at a computer typing casually with speech bubble saying for i in range(100) 搞定, panel 4: first student staring in disbelief while second student leans back relaxed with speech bubble saying 這就是 Python 的力量 and first student has speech bubble saying 你犯規
- **備註**：第二格的紙張要有誇張的散落效果，第四格呈現鮮明對比（一個累癱 vs 一個悠哉）

### 圖 2
- **類型**：概念圖（Explanation）
- **意圖**：用視覺化方式說明「有縮排 = 在迴圈裡面」和「沒縮排 = 在迴圈外面」的區別
- **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: a stick figure pointing at a box labeled for loop 的範圍 with an arrow showing code with indentation inside the box with speech bubble saying 有縮排的在裡面, panel 2: same stick figure pointing at code without indentation outside the box with speech bubble saying 沒縮排的在外面, panel 3: a confused student stick figure looking at code with mixed indentation with speech bubble saying 所以 indent 很重要？, panel 4: the teacher stick figure nodding firmly with speech bubble saying Python 靠 indent 決定誰歸誰管
- **備註**：要有清楚的「框線」區隔迴圈範圍內外

### 圖 3
- **類型**：四格漫畫（Comparison）
- **意圖**：用三種 range 用法的對比，讓學生一眼看出 range(n)、range(start, stop)、range(start, stop, step) 的差異
- **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: a stick figure teacher with a whiteboard showing range(5) and numbers 0 1 2 3 4 with speech bubble saying range(5) 從0到4, panel 2: whiteboard showing range(2, 6) and numbers 2 3 4 5 with speech bubble saying range(2,6) 從2到5, panel 3: whiteboard showing range(0, 10, 3) and numbers 0 3 6 9 with speech bubble saying range(0,10,3) 每次跳3, panel 4: a student stick figure with lightbulb above head with speech bubble saying 原來 range 有三種寫法 and teacher with speech bubble saying 包頭不包尾 記住了
- **備註**：每格的白板上要清楚標示數字序列，用箭頭標注 start/stop/step 的對應關係

### 圖 4
- **類型**：四格漫畫（Comparison）
- **意圖**：用 for 已知次數 vs while 未知次數的對比，讓學生直覺理解兩種迴圈的差異
- **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: a stick figure teacher pointing at a whiteboard with for i in range(10) written on it with speech bubble saying for loop 跑10次 很明確, panel 2: a student stick figure raising hand with speech bubble saying 那如果不知道要跑幾次呢, panel 3: teacher replacing the whiteboard text with while N != 1 with speech bubble saying while loop 跑到條件不成立, panel 4: student with lightbulb above head with speech bubble saying 原來一個數次數 一個看條件
- **備註**：第一格和第三格要有白板上的程式碼清楚可見，第四格學生表情要有「恍然大悟」感

### 圖 5
- **類型**：四格漫畫（Warning）
- **意圖**：用無窮迴圈的災難場景，讓學生對「忘記更新條件」印象深刻
- **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: a student stick figure typing while True with speech bubble saying while 條件... 寫好了, panel 2: computer screen showing output 5 5 5 5 5 with lines scrolling endlessly and student with speech bubble saying 等等 怎麼停不下來, panel 3: student panicking with sweat drops pressing keyboard frantically with speech bubble saying 停啊！！怎麼關？！, panel 4: teacher stick figure calmly pointing at code with speech bubble saying 你忘記更新變數了 and student collapsed on desk
- **備註**：第二格的螢幕要有「無限滾動」的視覺效果，第三格學生表情要極度驚慌

### 圖 6
- **類型**：四格漫畫（Comparison）
- **意圖**：用「煞車」和「快轉」的生活比喻，讓學生一眼記住 break 和 continue 的差異
- **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: a stick figure driving a car in a loop track with speech bubble saying 迴圈開始 gogogo, panel 2: same stick figure slamming brakes with speech bubble saying break！緊急煞車！ and car screeching to a halt, panel 3: a different scene showing a stick figure watching a video and pressing fast-forward button with speech bubble saying 這段不想看 continue, panel 4: both stick figures side by side with speech bubble break = 整個不跑了 and continue = 跳過這一輪
- **備註**：第二格要有煞車的動態效果（煞車痕、車子傾斜），第三格要有快轉的 ⏭ 符號

### 圖 7
- **類型**：四格漫畫（Analogy）
- **意圖**：用「教室點名找小明」的場景說明 break 的實際用途
- **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: teacher stick figure with attendance list calling out with speech bubble saying 1號 到 2號 到 找小明找小明, panel 2: teacher continues calling with speech bubble saying 3號...不是 4號...不是 and looking increasingly tired, panel 3: a student raising hand excitedly with speech bubble saying 我就是小明！, panel 4: teacher relieved with speech bubble saying break！找到了不用繼續 and throwing the attendance list
- **備註**：第四格老師的「扔名單」動作要誇張，表示終於可以停了

### 圖 8
- **類型**：四格漫畫（Analogy）
- **意圖**：用「批改考卷跳過白卷」的場景說明 continue 的跳過邏輯
- **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: teacher stick figure grading a stack of papers with speech bubble saying 改考卷改考卷, panel 2: teacher picks up a blank paper with speech bubble saying 這張是白卷？, panel 3: teacher tosses the blank paper aside with speech bubble saying continue！跳過 改下一張, panel 4: teacher continuing to grade the next paper normally with speech bubble saying 這張有寫 來改分數
- **備註**：第三格要有紙張被丟到旁邊的動態效果，第四格回到正常批改狀態

### 圖 9
- **類型**：四格漫畫（Hook）
- **意圖**：用「在教室每排每個座位貼標籤」的日常任務，讓學生直覺感受到「兩層重複」的結構需求，引發對巢狀迴圈的好奇心
- **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: a student stick figure standing in front of a classroom grid of seats labeled Row 1 through Row 3 with speech bubble saying 老師叫我幫每個座位貼標籤, panel 2: student going to first row and labeling seats 1-1 1-2 1-3 with speech bubble saying 第一排先貼完, panel 3: student moving to second row continuing to label seats with increasingly tired expression and speech bubble saying 第二排接著貼, panel 4: student looking exhausted but proud in front of all labeled seats with speech bubble saying 這就是 Nested Loop 外層管排 內層管座位
- **備註**：座位格要清楚排列成網格狀，讓兩層重複的結構一目了然；第四格的領悟表情要有「恍然大悟」感

### 圖 10
- **類型**：概念圖（Explanation）
- **意圖**：用視覺化流程圖說明外層迴圈每跑一次、內層就完整跑一遍的執行順序，建立「行列掃描」的心智模型
- **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: two nested loop symbols with outer labeled i and inner labeled j with teacher stick figure pointing and speech bubble saying 外層 i 每前進一步, panel 2: inner loop j shown running fast from 1 to 5 with multiple motion lines and speech bubble saying 內層 j 就跑完一整圈, panel 3: a diagram showing Row 1 filling completely before Row 2 starts with sweep arrow and speech bubble saying 先填滿 i等於1 再填 i等於2, panel 4: completed grid pattern with student having lightbulb moment and speech bubble saying 原來是先行後列 一行一行填完
- **備註**：流程箭頭要清楚標示外層跟內層的掃描方向，用不同顏色或粗細區分

### 圖 11
- **類型**：四格漫畫（Analogy）
- **意圖**：用電影院服務員逐排逐座位點名的場景，具象化「外層管排、內層管座位」的巢狀迴圈執行邏輯
- **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: a movie theater usher stick figure with clipboard standing at entrance with speech bubble saying 開始對號入座點名, panel 2: usher at Row 1 pointing seat by seat calling 1-1 1-2 1-3 with audience raising hands and speech bubble saying 第一排點完, panel 3: usher moving to Row 2 starting the same process with speech bubble saying 第二排開始, panel 4: usher finishing all rows looking triumphant with speech bubble saying 這就是 for row in rows 加 for seat in row 的 Nested Loop
- **備註**：電影院座位配置要清楚排列，每排點名的順序用箭頭或框線標示；第四格的總結文字要清楚對應程式碼結構

### 圖 12
- **類型**：四格漫畫（Tutorial）
- **意圖**：展示學生用三行程式碼就印出九九乘法表的驚喜過程，強化「巢狀迴圈威力」的印象
- **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: student stick figure looking at a blank multiplication table grid with worried expression and speech bubble saying 81格要一格一格算嗎, panel 2: teacher holding up 3 fingers with confident expression and speech bubble saying 只需要三行程式碼, panel 3: code snippet showing nested for loops on a screen with speech bubble saying for i for j print i times j, panel 4: completed 9x9 multiplication table appearing on screen with student having a shocked jaw-drop expression and speech bubble saying 竟然真的三行搞定
- **備註**：第四格的乘法表要有清楚的格線和數字，學生的驚愕表情要誇張；第三格的程式碼要清晰可讀

### 圖 13
- **類型**：四格漫畫（Recap）
- **意圖**：讓學生感受到「我在模組二真的學了很多東西」的成就感，用四個迴圈工具的學習旅程做總結
- **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: stick figure at starting line looking nervous with speech bubble saying 模組二開始 什麼都不會, panel 2: same stick figure now holding a for loop sign with range written on it and a confident smile with speech bubble saying 2-1 for loop range 搞定重複, panel 3: stick figure holding break and continue signs in both hands with speech bubble saying 2-2 while 2-3 break continue 全學會, panel 4: stick figure standing proudly in front of a nested loop diagram with graduation cap on head and speech bubble saying 2-4 Nested Loop 也會了 模組二完成
- **備註**：四格要有明確的成長弧線，從緊張到自信；最後一格的驕傲感要強，學士帽是里程碑象徵

### 圖 14
- **類型**：四格漫畫（Hook）
- **意圖**：用「被一百筆資料淹沒」的荒謬場景，製造認知懸念，讓學生期待模組三的串列解決方案
- **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: teacher stick figure pointing at assignment board with speech bubble saying 讀入全班100個成績 算平均, panel 2: student starting to type code showing score1 score2 score3 on screen with a pained expression and speech bubble saying score1 score2 score3..., panel 3: student completely buried under a mountain of papers labeled score1 through score100 only head visible with speech bubble saying 我寫到score47了還沒完, panel 4: teacher holding up a bracket symbol representing a list with a bright smile and speech bubble saying 模組三 一個串列 一行搞定 and student poking head out with wide eyes saying 什麼？
- **備註**：第三格的「被資料淹沒」要有誇張的堆疊效果，只露出頭部；第四格的「串列」符號要清楚（方括號 []），反差要鮮明
