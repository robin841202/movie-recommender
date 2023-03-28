# 基於Word Embedding的電影推薦系統
![01](https://user-images.githubusercontent.com/22574508/228192680-fbdb7ddc-69c1-40fa-8ffa-adf28f8df8be.jpg)
## 資料來源
-   使用Python爬蟲將IMDB前top250部電影資訊爬下來儲存為csv檔，並顯示於網頁

## 使用的技術及套件
-   BeautifulSoup
-   Django Framework
-   Word Embedding

## 推薦系統
- 將部分電影資訊轉換為 *詞嵌入(word embedding)*
  - 電影類型
  - 導演
  - 演員
  - 電影情節
-   利用 *餘弦相似(cosine similarity)* 比較相似度，並推薦前20部電影
![02](https://user-images.githubusercontent.com/22574508/228192728-31ea4091-df78-4950-aadf-74fd5bda1687.jpg)
![03](https://user-images.githubusercontent.com/22574508/228192737-93113f8a-d6c1-4698-bf24-1fa717173483.jpg)

