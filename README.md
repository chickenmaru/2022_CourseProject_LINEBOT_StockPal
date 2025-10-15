# Overview
This project is a LINE chatbot that provides users with information about stocks and recent news. The bot is built with Python using the `Flask` and `LineBotSdk` libraries for the chatbot functionality, and `Selenium`, `BeautifulSoup`, and other data-processing libraries to scrape and handle external data.

The bot supports several features, including:
- **Displaying a command panel:** Users can type "開啟面板" to see a list of available commands.
- **Fetching daily stock data:** Users can query for a specific stock by its code to get a table of recent trading data.
- **Searching for a stock code:** Users can input a company's name to find its corresponding stock code.
- **Comparing stocks:** The bot can provide a comparison of a given stock with its peers in the same industry.
- **Retrieving recent tech articles:** The bot scrapes and provides a list of the latest technology articles from The Initium.
- **Displaying hot topics:** The bot generates a word cloud of popular discussion topics from the PTT Stock board and sends it as an image.
- **Echoing messages:** If a user's message doesn't match a command, the bot will "sing" the message back by adding musical notes (♫♪♬) between the characters.

# Features and Commands

| Command | Description |
| :--- | :--- |
| `開啟面板` | Displays a menu with all available commands. |
| `查詢今日股票交易` | Prompts the user to enter a stock code to get its daily trading volume and price information. |
| `查詢公司股票代碼` | Prompts the user to enter a company name to find its stock code. |
| `查詢公司同業比較` | Prompts the user to enter a stock code and provides a comparison with similar companies. |
| `查詢今日科技文章` | Retrieves the latest technology articles from a news source. |
| `查詢近期熱門話題` | Generates and displays a word cloud of hot topics from the PTT Stock board. |
| (Any other text) | The bot will "sing" the message back by adding musical notes. |

# Technical Details

## `main.py`
This file sets up the core LINE bot application using `Flask`. It handles incoming messages from the LINE platform via a webhook. The `pretty_echo` function is the main logic for processing user messages and directing them to the appropriate functions in `grab.py`. It uses a `worknum` variable to manage multi-step conversations (e.g., waiting for a stock code after a query command).

## `grab.py`
This file contains the web scraping and data processing logic.
- **`run_article()`:** Scrapes the latest tech articles from The Initium and formats them into a Flex Message template for LINE.
- **`run_stock(stockNO)`:** Fetches daily stock data from the Taiwan Stock Exchange (TWSE) API using the provided stock number. It then uses `pandas` to format the data and `matplotlib` to save the dataframes as images, which are uploaded to Imgur for display in the LINE chat.
- **`search_stockNO(companyName)`:** Uses `Selenium` to search for a company's stock code on a financial website.
- **`search_hot_topic()`:** Scrapes titles from the PTT Stock board, processes the text using `jieba` for word segmentation, and creates a word cloud image using the `WordCloud` library. The image is then uploaded to Imgur.
- **`compare(companyNum)`:** Scrapes and compares key financial data for a list of companies that are peers to the one provided by the user. The peer list is hardcoded in the `companyList` variable.
- **`store_pandas_picture(df,name)` and `upload_picture_to_imgur(name)`:** Helper functions to convert a `pandas` DataFrame into an image file and upload it to Imgur, returning a shareable link.
