<a href="https://www.buymeacoffee.com/tsunglung" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="30" width="120"></a>

Home assistant for Uber Eats


使用本整合, 必須由你承擔任何風險.

## 安裝

你可以使用 [HACS](https://hacs.xyz/) 來安裝此整合元件. 步驟如下 custom repo: HACS > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `tsunglung/UberEats` > Category: Integration

或是手動複製 `uber_eats` 到你的設定資料夾 (像是 /config) 下的 `custom_components` 目錄.

然後重新啟動 HA.


# 前置作業

你必須取得 Cookie 令牌. 如果你遇到 http_result 500 的問題，你必須要重新取得令牌。

**1. 取得步驟**

1. 開啟開發者工具 (使用 Google chrome/Microsoft Edge) [Crtl+Shift+I / F12]
2. 打開 應用程式 頁面，找到儲存空間。
3. 打開 [Uber Eats](https://www.ubereats.com) 的網站, 登入你的帳號密碼.
4. 在 Cookie 欄位, 搜尋 "sid" (可能會有多個項目，選擇第一個)
5. 複製在" 值" 欄位下, 一段很長的字串, 像 "QA.GA1adsm2S50n;2xlmbbG9....=" (使用滑鼠並複製到剪貼簿, 或是記事本)

![grabbing](grabbing.png)

# 設定

**2. 使用 Home Assistant 整合**

1. 使用者介面, 設定 > 整合 > 新增整合 > Uber Eats
   1. 如果整合沒有出在清單裡，請重新整理網頁
   2. 如果重新整理網頁後，整合還是沒有出在清單裡，請您清除瀏覽器的快取
2. 輸入 帳號和 Cookie 值
3. 如果輸入都正確，就可以創建自動化，廣播外送進度到通訊軟體和 HomePod mini。


打賞

|  LINE Pay | LINE Bank | JKao Pay |
| :------------: | :------------: | :------------: |
| <img src="https://github.com/tsunglung/UberEats/blob/master/linepay.jpg" alt="Line Pay" height="200" width="200">  | <img src="https://github.com/tsunglung/UberEats/blob/master/linebank.jpg" alt="Line Bank" height="200" width="200">  | <img src="https://github.com/tsunglung/UberEats/blob/master/jkopay.jpg" alt="JKo Pay" height="200" width="200">  |