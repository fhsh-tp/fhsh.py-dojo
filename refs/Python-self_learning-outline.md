# **108課綱核心素養：高一 Python 與演算法實戰課綱（Judge 導向詳盡版）**

**適用對象**：高中一年級（零基礎、無先修經驗）

**核心基調**：程式語言（Python）只是一種與電腦溝通的「工具」。我們的重點不在於背誦語法，而在於理解「**人們發明這個概念是為了解決什麼問題？**」，並透過「**輸入 (Input)** ![][image1] **處理 (Process)** ![][image1] **輸出 (Output)**」的 Judge 解題思維，鍛鍊解決問題的演算法邏輯。

**教學原則**：用現實生活的問題帶出技術需求，絕不為了教語法而教語法。前三模組嚴格控制教學深度打底內功，模組四則釋放 Python 的強大火力以應付 APCS 檢定。

## **模組一：與電腦溝通的基礎（輸入、處理與輸出的藝術）**

**對應教材**：《為你自己學 Python》第 1\~5 章 / 演算法：什麼是演算法、流程圖。

### **章節 1-1：寫在最前面與學習、開發環境介紹（建立溝通橋樑）**

* **概念溯源（為什麼發明它？）**：電腦只懂 0 與 1，人類講自然語言。我們需要一個翻譯官（直譯器）和一個書桌（開發環境）來把人類的問題翻譯給電腦聽。  
* **具體教學內容**：  
  * 本 Judge 系統的使用
  * 說明在自己電腦使用時的 IDE（Integration Development Environment）是什麼；介紹有哪些 IDE 以及業界常見 IDE（推薦 VScode），以及線上的 IDE（推薦 Google Colab）。
  * print() 與 input()：最基礎的 I/O（輸入與輸出）觀念。  
* **教到什麼程度（教學邊界）**：  
  * **只教**基本的執行、存檔與 I/O。  
  * **絕對不教**虛擬環境（venv）、環境變數設定。能跑最重要。  
* **【Judge 解題實戰】**：  
  * **題目：** 哈囉，世界！  
  * **Input：** 一個字串 ![][image2]（使用者的名字）。  
  * **Output：** 輸出 Hello, \[S\]\!。藉此確認學生懂得如何讀取輸入並印出指定格式。

### **章節 1-2：變數、數字與文字（給生活事物貼標籤）**

* **概念溯源（為什麼發明它？）**：人類的記憶力有限，且電腦記憶體位址（如 0x7FFF...）太反人類。變數的發明是為了解決「狀態儲存」的問題；而不同資料型態（文字、數字）則是為了決定資料「能做什麼運算」。  
* **具體教學內容**：  
  * 變數宣告、基礎型別（int, float, str）。  
  * 資料型別轉換（如 int()）、基本的四則運算與取餘數（%）。  
* **教到什麼程度（教學邊界）**：  
  * **只教**加減乘除、除法取整（//）、取餘數。  
  * **絕對不教**字串的底層編碼（Unicode/Byte）。  
* **【Judge 解題實戰】**：  
  * **題目：** 飲料店的收銀機（A+B Problem 的變形）。  
  * **Input：** 兩行輸入，第一行為珍珠奶茶的數量（整數），第二行為每杯單價（整數）。  
  * **Output：** 輸出總金額。

### **章節 1-3：布林值與流程控制（人生的十字路口）**

* **概念溯源（為什麼發明它？）**：如果程式只能「由上往下」執行，電腦就只是個智障型計算機。條件判斷（If-Else）的發明，讓電腦擁有了「根據不同情況做出不同決策」的能力。  
* **具體教學內容**：  
  * 布林值（True/False）、比較運算子與邏輯運算子（and, or, not）。  
  * 畫出判斷邏輯的「流程圖（Flowchart）」。  
* **教到什麼程度（教學邊界）**：  
  * **只教**最多兩層的巢狀 if。  
  * **絕對不教** \== 與 is 的底層記憶體位址差異。  
* **【Judge 解題實戰】**：  
  * **題目：** 閏年判斷器（經典邏輯題）。  
  * **Input：** 一個西元年份 ![][image3]。  
  * **Output：** 如果是閏年輸出 Leap Year，否則輸出 Common Year。

## **模組二：整理與征服大資料（資料結構與迴圈的協奏曲）**

**對應教材**：《為你自己學 Python》第 6\~9 章 / 演算法：陣列、雜湊表、線性搜尋、氣泡排序。

### **章節 2-1：迴圈（讓電腦當免費勞工）**

* **概念溯源（為什麼發明它？）**：人類最討厭重複性的枯燥勞動，而這正是機器的強項。迴圈解決了「同一套邏輯需要對不同資料重複執行無數次」的問題。  
* **具體教學內容**：  
  * for i in range() 的定次數迴圈。  
  * while 條件迴圈、break 提早結束與 continue 跳過。  
* **教到什麼程度（教學邊界）**：  
  * **只教**基本計數與條件中止。  
* **【Judge 解題實戰】**：  
  * **題目：** 3N+1 猜想（Collatz Conjecture）。  
  * **Input：** 一個正整數 ![][image4]。  
  * **Output：** 根據 3N+1 規則，輸出變換到 1 總共需要幾個步驟（使用 while 迴圈計算）。

### **章節 2-2：串列與線性搜尋（排隊與點名）**

* **概念溯源（為什麼發明它？）**：當有 100 個學生的成績時，宣告 score1 到 score100 是愚蠢的。陣列（List）解決了「同類別大量資料的統一管理與循序存取」問題。  
* **具體教學內容**：  
  * List（串列）的新增、讀取與 Zero-based 索引值。  
  * **【演算法】線性搜尋（Linear Search）**：最直觀的尋找資料方式。  
* **教到什麼程度（教學邊界）**：  
  * **只教**一維串列及最基礎的切片。  
  * **絕對不教**串列推導式（保留至模組四才教），嚴格要求學生老實寫 for 迴圈。  
* **【Judge 解題實戰】**：  
  * **題目：** 尋找最大值與位置。  
  * **Input：** 第一行為資料筆數 ![][image4]。第二行為以空白分隔的 ![][image4] 個整數。  
  * **Output：** 輸出最大值以及它所在的索引值（Index）。

### **章節 2-3：串列進階與氣泡排序（名次怎麼排？）**

* **概念溯源（為什麼發明它？）**：雜亂無章的資料是沒有價值的。「排序」解決了「如何讓資料有結構、可預期」的問題，是所有高效演算法的基石。  
* **具體教學內容**：  
  * 變數交換（a, b \= b, a）、雙重迴圈。  
  * **【演算法】氣泡排序法（Bubble Sort）**：實作與理解 O(N^2) 的代價。  
* **教到什麼程度（教學邊界）**：  
  * **只教**氣泡排序。因為它最直觀，最適合教導「交換」與「狀態追蹤」。  
* **【Judge 解題實戰】**：  
  * **題目：** 頒獎典禮（氣泡排序實戰）。  
  * **Input：** ![][image4] 個學生的成績。  
  * **Output：** 將成績由大到小排序後輸出（嚴禁使用內建 .sort()）。

### **章節 2-4：字典、元組與雜湊表（秒殺查找的魔法）**

* **概念溯源（為什麼發明它？）**：當資料量達到百萬筆，從頭找起會讓程式卡死。字典（雜湊表 Hash Map）的發明是為了解決「如何利用 Key 瞬間（O(1)）找到 Value」的效能問題。  
* **具體教學內容**：  
  * Dict（字典）的 Key-Value 結構。  
  * 對比 List 的線性搜尋與 Dict 的雜湊查找速度差異。  
* **教到什麼程度（教學邊界）**：  
  * **重點放在 Dict** 的新增與查詢。  
* **【Judge 解題實戰】**：  
  * **題目：** 字母出現頻率統計（Word Count）。  
  * **Input：** 一段英文字串。  
  * **Output：** 依字母順序輸出每個字母出現的次數。  
  * **題目：** 落單的數字（Single Number \- 常規版）。  
  * **Input：** 一串數字，其中除了「一個數字」只出現一次外，其他數字皆出現「兩次」。  
  * **Output：** 請用 Dict 計算每個數字出現的次數，找出那個落單的數字（為模組四的位元魔法鋪陳）。

## **模組三：抽象化與工具封裝（製造解決問題的武器）**

**對應教材**：《為你自己學 Python》第 10\~13 章 / 演算法：二分搜尋、遞迴。

### **章節 3-1：函數基礎與二分搜尋（終極密碼）**

* **概念溯源（為什麼發明它？）**：不斷複製貼上相同的程式碼會導致災難。「函數」解決了「程式碼重用（DRY）」與「邏輯黑盒子化」的問題。  
* **具體教學內容**：  
  * def 定義函數、參數傳遞與 return 回傳值。  
  * **【演算法】二分搜尋法（Binary Search）**：體會排序後資料帶來的 O(log N) 搜尋威力。  
* **教到什麼程度（教學邊界）**：  
  * **只教**基礎參數與單一回傳值。  
* **【Judge 解題實戰】**：  
  * **題目：** 二分搜尋尋寶。  
  * **Input：** 第一行為已排序的 100 個數字。第二行為目標數字 ![][image5]。  
  * **Output：** 輸出目標數字在陣列中的 Index（嚴禁使用 .index()）。

### **章節 3-2：遞迴初探（大問題化小問題）**

* **概念溯源（為什麼發明它？）**：遞迴解決了「如何用同樣的邏輯，不斷縮小問題範圍直到能直接解答（Base Case）」的問題。  
* **具體教學內容**：  
  * 函數呼叫自己。畫出「呼叫堆疊（Call Stack）」。  
* **教到什麼程度（教學邊界）**：  
  * **只教**純遞迴。讓學生體會算費氏數列 ![][image6] 時電腦會卡住（鋪墊模組四的 DP 外掛）。  
* **【Judge 解題實戰】**：  
  * **題目：** 費氏數列（Fibonacci）。  
  * **Input：** 一個正整數 ![][image4]。  
  * **Output：** 輸出費氏數列的第 ![][image4] 項。

### **章節 3-3：錯誤處理與防呆機制（面對不完美的真實世界）**

* **概念溯源（為什麼發明它？）**：錯誤處理機制（Exceptions）解決了「當發生非預期狀況時，程式如何優雅地恢復，而不是直接崩潰」的問題。  
* **具體教學內容**：  
  * try...except 語法與 ValueError, EOFError（處理 APCS 常見的 EOF 測資）。

## **模組四：遺珠與外掛（APCS 解題的進階軍火庫）**

**模組定位**：前三模組我們為了建立紮實的運算思維，刻意不教偷吃步。但進入 APCS 程式競賽，**時間與執行效率就是一切**。本模組將解鎖 Python 那些「前面沒教，但在實戰中極度方便、能大幅節省程式碼與運算時間」的內建神兵，並一窺計算機底層的魔法。

### **章節 4-1：語法糖、位元魔法與控制流進階（少打字、少出錯）**

* **APCS 痛點**：複雜的資料處理如果全用基礎迴圈寫，不僅慢還容易超時（TLE）或超空間（MLE）。有時候，利用電腦底層的特性（二進位）可以暴力輾壓問題。  
* **外掛清單**：  
  * **手動進制轉換與 bin(), hex()**：APCS 常考的進制轉換，除了內建函數，學習用 int("1010", 2\) 秒殺字串轉十進位。  
  * **位元運算（Bitwise）的黑魔法**：重點介紹 & (AND), | (OR), \<\< (左移乘二) 以及 **最暴力的 ^ (XOR)**。  
    * **【震撼教育】落單的數字（Single Number \- O(1) 空間終極版）**：回顧 2-4 用 Dict 解的題目。如果在 APCS 被限制「不准用額外記憶體」，Dict 就報廢了。教導學生利用 XOR a ^ a \= 0 的計概特性，只要把陣列全部 XOR 起來，成對的數字全部抵銷為 0，留下來的那個就是答案！進階探討如何抓出「兩個相異的 single number」。  
  * **List Comprehension（串列推導式）**：讀取一行多個整數的標準起手式 \[int(x) for x in input().split()\]，一行秒殺。  
  * **lambda 匿名函數**：配合自訂排序，例如 data.sort(key=lambda x: x\[1\]) 直接針對二維陣列的第二個元素排序。  
  * **for...else 語句**：優雅的搜尋失敗處理。迴圈「沒有被 break 提早結束」時就會執行 else，省去宣告 is\_found \= False。  
  * **巢狀迴圈進階與 match...case**：Python 3.10+ 的 Switch Case，讓狀態機（State Machine）極度乾淨。

### **章節 4-2：演算法內建神兵（不要重複造輪子）**

* **APCS 痛點**：在考場上親手寫二分搜尋或優先佇列，一旦邊界條件寫錯就會拿到 WA (Wrong Answer)。  
* **外掛清單**：  
  * **bisect（內建二分搜尋）**：不用再自己刻 left \<= right！bisect.bisect\_left(arr, target) 絕對無 Bug。  
  * **heapq（最小積堆 / 優先佇列）**：當要求「隨時取出最小值」，min() 每次 O(N) 會直接 TLE。heapq 瞬間 O(log N) 取出，貪婪演算法必備。

### **章節 4-3：數學、組合與圖論的加速器（外鄉人戰法）**

* **APCS 痛點**：排列組合或動態規劃（DP）如果從零開始刻 DFS 遞迴陣列，程式碼很長且極易出錯。  
* **外掛清單**：  
  * **math 標準庫**：直接呼叫 math.gcd() 算公因數；math.comb() 算組合。  
  * **itertools（暴力破解外掛）**：利用 permutations (排列) 與 combinations (組合) 自動生成所有可能。遇到 ![][image7] 的測資，直接暴力破解無往不利。  
  * **functools.lru\_cache（一秒無痛 DP）**：回顧 3-2 計算費氏數列會卡死，只要在遞迴函數上一行加上 @lru\_cache(maxsize=None)，Python 自動加上記憶化搜尋（Memoization），O(2^N) 瞬間變 O(N)！  
  * **graphlib.TopologicalSorter**：工作排程依賴問題，免刻 Kahn's Algorithm，直接餵給圖論模組幫你解出拓撲排序。

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAXCAYAAADpwXTaAAAAl0lEQVR4XmNgGAWjgHpAQUGhEF2MbAA0bKGMjIwqujhZQE5OzlpeXn4bujjZAGhYNtDQNHRxBqCThWRlZaVIxUADlwLxWhAbbhgwDDqBgstJxUCXnQTS/4B0PZLbSAdA36gADdoLCj90OZIA0CccQIOuSEtLy6DLkQyABqUAcTG6OFkAaNB+IMWCLk4WABomiS42CgYBAABUyybk/x0YCgAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAYCAYAAAAh8HdUAAABO0lEQVR4Xu2SvStGURzHz4O8hLLcbum+1tWtK6nHIMliEmVkUzI9g8HiHzBSkvgLLHabnk1ZhMUkWZXByOLl87udR+f8MlqUb30793xffuc+57nG/Fk04jieS9O0mWVZvwjsR6MoGtDBGgQ3YBsewjP4RHGV9b4sy2GdN0mSbGNeEhrpaEwfQ/uAV262BoVxjHdCE9pDv4B7Wu+c8hkEwZD27KsuaV2MIynBHbZdyvu+EA/czrItCZ8JncL1oij6dNZFg9AWhVenLDzH69FhD2EYDhJc5Dfus75JkWELOmfyPJ/UmoBwy5ZankEhxGh7ogX6jJQ4dcozEFYwHnjs9gxTn3SA92jUbcq0YzttzdXZz6K/wKar10C8JrDJegdv4C48gbc/XoAAY1rWqqp65cuW/4bCvM794zfwBevtS6FR+ne9AAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAXCAYAAAAC9s/ZAAAA/UlEQVR4XmNgGAUM8vLyTkB8D4QVFBRuAek7QHwTyOZAVgfkXwKKPwDi2yC1cnJyzsjyDECBeqDEfyDegiIBBUBxLyD+AMQ9QKyILs+gpKQkB5T4B8RfxMXFudHk+IEuOAWUM0QWxwBARYdArgDSEUjCLEDX7QCKeyOJYQdAjelQAzYhic0EGpCHrA4nkJaWFgYa8AuEZWRkhIB0CRBPRleHFwA1bAa5AmjrBhAbKMSMrgYvAGqMARkAxJfV1dV50eUJAqDGpVADNNHliAJAjU+B+CW6OFFAUVFRH2r7WnQ5vEBWVtYWqOk6EL8H4m9A/AWI7wKxFbraUTAsAQDxq0BRFZzSeQAAAABJRU5ErkJggg==>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAYCAYAAAD3Va0xAAABT0lEQVR4Xu2TPy8EURTFl62oREQx5v8kRETjAyiWDyBEqV2ytUYn0agkEo1KI/HnS0goSIgIiUYioqGj2SjE8rvrjX1zZ7bQz0lO5s0559737ptMpVLiXwiCoAYf4Qt8hfsFmUv4BB9Mdktn/uD7/iGBd9jyPC9RdjUMw3V46rruiPKyIHRLk1X4XbQj/iabLWo9gyiKxggewwGaNOGb4zj9dgbtLEmSYVvLgQbLBBtmvSunYvd66jNOH9p1p6ILCB3AcVlTNCmNZNTUp+kM2k6nogsI3aj3E2nGyNPmfQMu2Jkc0vuxNYrmzanautwPdzZkZ3IgvJLej4Uq4zyjf8ZxPMrzSvl50OiIookCfU1OBc9Zb2tfo4fgvTy1IaPgfZgR57SfASdZInjHsld7Avw9/C++5KD22iAwG/z+V7KjUH6Nms6hTcELrZcoAX4AaIRUBIoI1u0AAAAASUVORK5CYII=>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAYCAYAAAD3Va0xAAABU0lEQVR4Xu2TPy8EURTFh02IRCSK6eZ/BsnQCI1CYhsKvfgCRKOi0ql8A1FQiIhSdCQ+gZ7EWlZEoZNYho7ftW/luQxR25OcvPfOPffsfZO3jtPCn+D7/ngYhhfwGtbMeh5F0VTTw37V6FV4GQTBhp3xCZgPML3GcTypazQOUqvj2WYtI7Vpzwcw3ME8y7IOpZcJOoKJrX+LJEn6ZRp4bOucl+Cm53ldtl4Ifm3OBK3I2XXdbvY7XGVBe38ETbsmaIxvNMB6SsiJ9v0KGm9hnclmWPcJqUgw5xHtLQT37zPTvNC4hlRiXTTalvYXgqZ5aZK30tTSNO2RCWFOvdf2FwLzngTxMEeVvm6mWrb1QoSN9/PAtmTrBA+ZoBrHdrv2BZiGxcz4h7omoHYmda49q2vvoDARNv5f9/AZPhF2wzotdb5RJ/sr+CjTwhxWHTV1C/8ab8xiXmpfbBc0AAAAAElFTkSuQmCC>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD8AAAAYCAYAAABN9iVRAAAC9UlEQVR4Xu2WW4iNURTH54KQJIzLuX3nhmZcikkZ5GGGRyXXUbwiL1IioYQpXhQpJg8uTW6RUh6Ny5SjSBrFwxRjSngiGR4Y47fO2d85a9acmebpnBrfv/59e//X5az17b2/sysqAgQI8N/C87xG+A5+gp9hWxGf57Abdjnf09an1IjH41uo44TVQVUsFluLrQWfvTxnW4dBIOAGjt/g32g0mjLmahIdhU8ikUjY2EoO6gtR51fquan1urq6cei34f1EIrGKnvYz/ggbtN8gkKgTp32wv9jKYj9Jsk1WLweo7w7ss80z34X+JRQKTVS+LbCL4RjlWgBvaR6Bt+AUHHvlreoEArSOVCo1Q2vlAAuwjVqOwZ+2ebSXaPe0hv9qWVCeK7WeBwE7cdjtxq3OeYdvZ6tPkMSFiPKARZpJXY/d9h7QvFu4fp5XdAzaEtHhEa3ngeE6rJUxjS50STp9Oz/YhHauEFEeSLOc96Uyts1T9xxXd2shIlv7fLeY57WeB8ZXZv5QAuSj4ebH4QbtMxRqamom4dsuK1SM2B65/O2OD+Bim8eC2I00dsqfe6Z55g1Ss20SrVZ07ZuHf961hvN6F5DVGXfwDZiufUoJVnWqvDjqGe9rtnnGy1zzF3zN+WWbh9e0nkU894XMnneFapL0oP9OJpNzeb4w9pKCWi7DFVqzzfOC0q7Ji9qPY7LA6We1noUkkHNRRD/ogjKMz1j7MKgkXxNcM1KGw+FpNomGl7tcfYDvvdwlq9vV9kPm1LfVHbc/dnujLRdffueA1gWVGN7I0xpkm2P7JYEkXGftQ0H+Iok5BA+PlEUuVcNCXparyzYq35OM1vBpFl+O9yKty3bajuE1w6oBBgfsl7D3yZmztnKChmZJQ/Cu0eXK2ys3QF9jflVeSt4plvvjl3u8rKxQrrWNeQcHL/cf+czq5QT1ZFzt34X00iPbXtnln+kt+h6ebfBpOp2erHOMasjOoPnNNN5QX18/1toDBAgQIMBoxz+lRfHgXGAujwAAAABJRU5ErkJggg==>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD8AAAAYCAYAAABN9iVRAAADP0lEQVR4Xu2WWYiNYRjHxwyKpEnGcvaZcyxzrBnLjCQNuaApmQY3LlxYUpKIJEs05caaYozINNndkOXGkslSJI3iYiQpoQhpcmEZv+ec9zvzzuN8Z845BuH869/7fv9neZ/n/d5vycvLIYcc/lsEg8FK+BS+hK9gYxKfu/AZbDG+O7XPb0R+KBRa5PP5vNpgkB8IBKqosRa/VYyDtcMPIOAEju/hN7/fH1bmAhJtgTdSLJoRZA3y1bHeQW1LBupbjO9p+Ba2ET9B+0Sj0Z7YzsALxcXFU4lZy/wFrNC+HUAhzTitkcTJ7iz27SSr0XqmoKgx5D8Oz5Nvira7Ad8VxMyGO9yap8Zl2F57PJ7ejsZ1LWxh2t1ybQcFDSPwFCzEsRW+sxMI0JrC4fAAW8sE0ij5z8kJYxyr7emC2PVuzaPflzVsjfVmiL/rRhOwFIflZi5HUZyXOHaOei9J3B6RPoibBa/AQ+QZou2Zwq15c+PaGI/aOto40eFGW08gGD+GpTKnwFEmSbNjZyOmo+1rj+gU8o6YT8xNYnd5vV6fdsgWbs3Lxpq662yd9UeIzrjf1hPA+EBdX5MAeWmY622w2vZJBXw3wDe6wK6AW/NoFcmaRCs1m3LS1mNwnndbw3muCYjpzJt4B/S3fToDsdOIuwgbKCiq7dnCaZ66Jyq93DR/wNad5uExW48hFH9Dxp53CwUkeY7+uaSkZCjjPWVPG9yh8cH4J+qsvlvZwGmecZKtc+wjpsl6W2fNkUbfa+sxyHGQ5yKJHlsE3ma+R9szBTmGk+swvCTvEG1PF27NFxUV9UH/Iv3YOtpk8WfNdbYu6IbhkYzaIMcc2yez0BxtzxZ8Lv3k203eqxRUlZdk7VSwmi/XNvTrcrNsDb8F4s9jMtrW5U24EMNDpvkdDAbYj2D/ypHqp20/C7O5W2UjtC0VqGmzaWamtoXiX5hWjrrH0bhukE1JOAXiH375j5c7K5Tf2sqEg0Ew/o28o/U/AWq+TC1PTK0f4EfYgr7J9gvGv0yP0VcyNsJbkUikr+3zT4MTMIjm59F4RVlZWQ9t/6Vg8UL56UiHHN+BOv6vBrtew67Xp8nVOj6HHHLIoavwHRtO9sFztr2tAAAAAElFTkSuQmCC>