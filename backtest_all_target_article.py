# 回測所有標的文
# 抓取ptt所有標的文
import pandas as pd

from config import csv_path, xlsx_path
from db_connect import conn
from utils import get_stock_code_from_title, back_test_stock_code_and_date

ori_df = pd.read_sql("SELECT * FROM info WHERE category = '標的'", conn)

df = ori_df.copy()
# 抓出標的代碼
df['target_code'] = df['title'].apply(get_stock_code_from_title)

# 去掉部分標的代碼為空的資料
df = df[df['target_code'].notnull()].reset_index(drop=True)

# 去掉回文的標的文
df = df[df['is_re'] != 1].reset_index(drop=True)

# 判斷標題是否有含'空'字，否則都判定為做多，去掉做空的標的文
df = df[~df['title'].str.contains('空')].reset_index(drop=True)

# 用回測的方式去找出標的的報酬率
profit_df = back_test_stock_code_and_date(df[['target_code', 'date_format']], 'target_code', 'date_format')

# 暫時儲存起來
profit_df.to_csv(csv_path + 'profit_df.csv', encoding='BIG5', index=False)
# profit_df = pd.read_csv('profit_df.csv', encoding='BIG5')

# 合併回原本的資料
result = df.merge(profit_df, on=['target_code', 'date_format'], how='left')

# 儲存
result.to_csv(csv_path + 'target_article_profit.csv', encoding='UTF-8', index=False)
# xlsm格式
result.to_excel(xlsx_path + 'target_article_profit.xlsx', index=False)
# result = pd.read_csv('target_article_profit.csv', encoding='UTF-8')
