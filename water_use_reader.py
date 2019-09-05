import pdfplumber
import pandas as pd
import os

# 這邊的檔案超靠背，縣市名稱改變就算了，‘臺’、‘台’不分，而且讀出來的數據格式還會不同，非常可怕

# 取得民生用水資料
def get_ppl_usage():
    file_name = '99_ppl_water_use.pdf'  # 單位是立方公尺/年
    pdf = pdfplumber.open(file_name)
    page = pdf.pages[0]
    table = page.extract_table()
    all_df = pd.DataFrame(table)
    df = pd.DataFrame()
    df['County']= all_df[1]
    df['Usage'] = all_df[10]
    all_county = []
    all_usage = []
    for i in range(3,11,2):
        county = df.at[i,'County']
        county = county.split('\n')
        usage = df.at[i,'Usage']
        usage = usage.split('\n')
        all_county += county
        all_usage += usage
    mod_df = pd.DataFrame(all_county,columns=['County'])
    mod_df['PPL_Usage'] = pd.DataFrame(all_usage)
    mod_df.drop([20],inplace=True)  #drop 澎湖
    mod_df.at[1,'County'] = '新北市' 
    mod_df = mod_df.set_index('County')
    area_df = pd.read_csv('county_area.csv')
    area_df = area_df.set_index('county')
    mod_df = mod_df.join(area_df)
    mod_df.to_csv('data.csv')
    #後面工人智慧處理一下縣市整併和名稱的問題

# 取得工業用水資料
def get_industry_usage():
    file_name = '99_industy_water_use.pdf'  # 單位是百萬立方公尺/年
    number = [7,6,8,2]  
    pdf = pdfplumber.open(file_name)
    c_name = []
    data = []
    for j in range(len(pdf.pages)-1):
        page = pdf.pages[j]
        table = page.extract_table()
        all_df = pd.DataFrame(table)
        for i in range(number[j]):
            name = all_df.at[1,4+i*2]
            if name == '面積':
                name = all_df.at[0,4+i*2]
                area = all_df.at[2,4+i*2].split(',')
                usage = all_df.at[2,5+i*2].split(',')
            else:
                area = all_df.at[3,4+i*2].split(',')
                usage = all_df.at[3,5+i*2].split(',')
            if len(area)>1:
                area = [area[0]+area[1]]
            if len(usage)>1:
                usage = [usage[0]+usage[1]]
            area = float(area[0])  #公頃
            area *= 10000  #平方公尺
            usage = float(usage[0])  #百萬立方公尺/year
            usage *= 1000000 #立方公尺
            
            withdraw = usage / area  #m/m2/year
            c_name.append(name)
            data.append(withdraw)
    d = {'County':c_name, 'Usage':data}
    data = pd.DataFrame(d)
    data.to_csv('data_industy.csv')
    
# 取得農業用水資料
def get_agri_usage():
    file_name = '99_agriculture_water_use.pdf'  # 單位是立方公尺/年
    pdf = pdfplumber.open(file_name)
    page = pdf.pages[0]
    table = page.extract_table()
    all_df = pd.DataFrame(table)
    all_df.drop([0,8,15,23,24,27,28],inplace=True)
    all_df.drop(columns=[0],inplace=True)
    all_df.reset_index(inplace=True)
    all_df.to_csv('farm.csv')

    
    all_df['water'] = 0
    page = pdf.pages[1]
    table = page.extract_table()
    df = pd.DataFrame(table)
    df.drop([0,1,2,10,16,20,23,24,25],inplace=True)
    df.drop(columns=[0,2,3,4,5],inplace=True)
    df.reset_index(inplace=True)
    df.to_csv('agri_water.csv')

# 資料整合輸出，接下來用geopandas那邊來讀取
def data_union():
    df = pd.read_csv('union.csv')
    df['Total'] = df['PPL_usage(m/m2/year)']+df['Industry_usage(m/m2/year)']+df['Agri_usage(m/m2/year)']
    df.to_csv('union_total.csv')
    


if __name__=='__main__':
    data_union()

