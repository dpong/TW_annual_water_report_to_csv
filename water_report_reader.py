import pdfplumber
import pandas as pd  # pandas是超神的資料處理套件，學起來早1年畢業。
import os  # 為了創建資料夾

# 取得測站資料
def get_head(year):
    head_df = all_df.loc[:1]
    head_df = head_df.dropna(how='all',axis=1)
    title = head_df.at[1,14]
    title = title.split('\n')
    if not os.path.exists('{}/station/{}'.format(year,title[0])):
        os.makedirs('{}/station/{}'.format(year,title[0]))
    head_df.to_csv('{}/station/{}/測站資料.csv'.format(year,title[0]), index = False, header = False)
    return title[0]

# 取得日流量資料
def get_daily(year,title):
    daily_df = all_df.loc[2:7]
    daily_df = daily_df.dropna(how='all',axis=1)
    daily_df.to_csv('{}/station/{}/日流量.csv'.format(year,title), index = False, header = False)

# 取得年流量資料
def get_annaul_sum(year,title):
    annual_sum_df = all_df.loc[9:10]
    annual_sum_df = annual_sum_df.dropna(how='all',axis=1)
    annual_sum_df.to_csv('{}/station/{}/年度統計.csv'.format(year,title), index = False, header = False)

# 取得平均月流量統計資料
def get_monthly_statistic(year,title):
    monthly_statistic_df = all_df.loc[12:14]
    monthly_statistic_df = monthly_statistic_df.dropna(how='all',axis=1)
    monthly_statistic_df.rename(columns={
        0:'月份',
        1:'1',
        3:'2',
        4:'3',
        6:'4',
        8:'5',
        10:'6',
        11:'7',
        13:'8',
        15:'9',
        16:'10',
        19:'11',
        20:'12'
    },inplace=True)
    monthly_statistic_df.to_csv('{}/station/{}/歷年月資料統計.csv'.format(year,title), index = False, header = True)

# 取得歷年統計資料
def get_all_statistic(year,title):
    all_statistic_df = all_df.loc[15:16]
    all_statistic_df = all_statistic_df.dropna(how='all',axis=1)
    all_statistic_df.to_csv('{}/station/{}/歷年統計資料.csv'.format(year,title), index = False, header = False)

# 當執行這個檔案的時候，下面的code才會執行。如果是其他程式call這個檔案則不會執行。
if __name__=='__main__':
    file_name = '2010_water_report_copy.pdf'  # 年份不同的話，自己改檔案名稱
    year = file_name[:4]
    year = str(int(year) - 1911)
    pdf = pdfplumber.open(file_name)
    station_number = len(pdf.pages)

    # 循環執行上面的def，建立巢狀資料夾。
    for i in range(station_number):
        page = pdf.pages[i]
        table = page.extract_table()
        all_df = pd.DataFrame(table)
        title = get_head(year)
        get_daily(year,title)
        get_annaul_sum(year,title)
        get_monthly_statistic(year,title)
        get_all_statistic(year,title)
        print('年份: ' + year
        + ' | 測站: ' + title
        + ' | 完成！')
    

