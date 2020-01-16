# Q-Trader

An implementation of Q-learning applied to (short-term) stock trading. The model uses 20 day windows of closing prices to determine if the best action to take at a given time is to buy, sell or sit.
使用Q-learning 去模擬、最佳化短期股票交易。
讀入前20天的收盤價，讓機器去判斷此時間的最佳操作，應該要買(Buy)、賣(Sell)、或是不動(sit)

As a result of the short-term state representation, the model is not very good at making decisions over long-term trends, but is quite good at predicting peaks and troughs.
此模型無法針對長期投資做出預測，但是可以根據歷史股價，學習出目前股價應為高峰或是低谷

## Results

Some examples of results on test sets:
![^GSPC 2011] Profit of $306070.068.
使用GSPC 2011來做模擬操作，得到的收益是$306070.068.


## Running the Code

To train the model, download a training and test csv files from [Yahoo! Finance](https://ca.finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC) into `data/`
The model at "modelk" dir
歷史股價資料資料 (CSV檔)從Yahoo! Finance下載
而預先Train 好的model在 "modelk" 資料夾

若要重新Train Model :
 
```
python train "0052" 20 100
```

Then when training finishes (minimum 200 episodes for results):
使用Train 好的結果，來模擬GSPC_2011的投資: 
```
python evaluate.py ^GSPC_2011 model_ep60
```

## References

[Deep Q-Learning with Keras and Gym](https://keon.io/deep-q-learning/) - Q-learning overview and Agent skeleton code