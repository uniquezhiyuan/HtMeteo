import datetime
import json
import numpy as np
import pandas as pd
import os
from tqdm import tqdm
import zipfile
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import shutil


class HtMeteo:
    def __init__(self, username='username', password='password'):
        self.hourly_history_meteo_data_path = './data/history'  # 逐小时数据存放目录，内含地名目录，地名目录内含数据文件
        self.daily_history_meteo_data_path = './data/history_analysis/daily_analysis'  # 逐日数据存放目录，内含数据文件
        self.monthly_history_meteo_data_path = './data/history_analysis/monthly_analysis'  # 逐月数据存放目录，内含数据文件
        self.yearly_history_meteo_data_path = './data/history_analysis/yearly_analysis'  # 逐月数据存放目录，内含数据文件
        self.forecast_data_path = f'./data/forecast'
        self.temp_data_path = f'./data/temp'
        self.work_dirs = [self.hourly_history_meteo_data_path,
                          self.daily_history_meteo_data_path,
                          self.monthly_history_meteo_data_path,
                          self.yearly_history_meteo_data_path,
                          self.forecast_data_path,
                          self.temp_data_path]
        self.username = username
        self.password = password
        self.account_info = '用户尚未认证'
        self.account_type = '普通用户'
        self.subscribe_days = 0
        self.api_key = '26262626262626262626262626'
        self.session = None  # self.login_account()
        self.location = ''
        self.years = [i for i in range(2000, 2026)]
        self.locations = [self.location]
        self.forecast_mode = 'off'
        self.history_mode = 'on'
        self.create_work_dirs()

    def create_work_dirs(self):
        for work_dir in self.work_dirs:
            p = Path(work_dir)
            p.mkdir(parents=True, exist_ok=True)
            # print(f'创建工作目录：{work_dir}······')
        print('工作目录初始化完毕。')

    def clear_data_dir(self):
        data_dir = Path('./data')
        if data_dir.exists() and data_dir.is_dir():
            shutil.rmtree(data_dir)
        # self.create_work_dirs()
        print('工作目录已清空。')

    def login_account(self):
        print(f"正在认证账户······")
        login_url = "https://app.cornicelli.net/meteo/login"
        user_center_url = f"https://app.cornicelli.net/meteo/profile"
        session = requests.Session()
        resp = session.get(login_url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')
        login_data = {
            'csrfmiddlewaretoken': csrf_token,
            'user-email': self.username,
            "user-password": self.password
        }
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'referer': 'https://app.cornicelli.net/meteo/'
        }
        login_resp = session.post(login_url, data=login_data, headers=headers)

        if login_resp.content.decode('utf-8').find('专业用户') > 0:
            print('专业用户 认证通过')
        else:
            print('专业用户 认证失败\n请检查用户名密码和网络连接状态以及专业用户订阅状态。')
            return 0
        user_center_resp = session.get(user_center_url)
        soup = BeautifulSoup(user_center_resp.text, 'html.parser')
        # 查找账户昵称
        title_div = soup.find('div', class_='datagrid-title', string='昵称')
        parent_item = title_div.parent
        content_div = parent_item.find('div', class_='datagrid-content')
        nick_name = content_div.text.strip()
        # 查找邮箱
        title_div = soup.find('div', class_='datagrid-title', string='注册邮箱')
        parent_item = title_div.parent
        content_div = parent_item.find('div', class_='datagrid-content')
        email = content_div.text.strip()
        # 用户类别
        title_div = soup.find('div', class_='datagrid-title', string='用户类别')
        parent_item = title_div.parent
        content_div = parent_item.find('div', class_='datagrid-content')
        user_type = content_div.text.strip()
        self.account_type = user_type
        # 用户升级时间
        title_div = soup.find('div', class_='datagrid-title', string='用户升级时间')
        parent_item = title_div.parent
        content_div = parent_item.find('div', class_='datagrid-content')
        subscribe_days = content_div.span.extract().text.strip()
        subscribe_date = content_div.text.strip()
        self.subscribe_days = int(subscribe_days.removesuffix('日'))
        # 订阅结束时间
        title_div = soup.find('div', class_='datagrid-title', string='高级/专业用户截止时间')
        parent_item = title_div.parent
        content_div = parent_item.find('div', class_='datagrid-content')
        subscribe_terminate_date = content_div.text.strip()
        # api_key
        title_div = soup.find('div', class_='datagrid-title', string='API Key')
        parent_item = title_div.parent
        content_div = parent_item.find('div', class_='datagrid-content').find('input')
        api_key = content_div['value']
        self.api_key = api_key
        account_info = (f"昵称：{nick_name}\n注册邮箱：{email}\n订阅类型：{user_type}\n订阅时间：{subscribe_date}至{subscribe_terminate_date}\n订阅时长：{subscribe_days}\n"
                        f"api_key：{api_key}")
        self.account_info = account_info
        print(account_info)
        return session

    def fetch_data(self):
        self.session = self.login_account()
        if self.account_type != '专业用户':
            print('用户权限不足，无法自动从云端拉取数据，请订阅专业用户。\n在线支持：https://cornicelli.net/meteo/doc')
            return 0
        if self.history_mode == 'on':
            # 获取小时数据
            years = self.years
            for year in tqdm(years, desc=f'正在从云端拉取 {self.location} 逐小时历史气象数据'):
                file_name = f"{year}_{self.location}_history_meteo_data.parquet"
                file_abs_path = os.path.join(self.hourly_history_meteo_data_path, self.location, file_name)
                temp_csv_path = os.path.join(self.temp_data_path, file_name.replace(".parquet", ".csv"))
                if not os.path.exists(file_abs_path):
                    file_url = f"https://app.cornicelli.net/meteo/download/history/{self.location}/{year}"
                    data_file_csv = self.session.get(file_url)
                    with open(temp_csv_path, "wb") as f:
                        f.write(data_file_csv.content)
                df = pd.read_csv(temp_csv_path)
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
                df.to_parquet(file_abs_path, engine='pyarrow', compression='snappy')  # zstd
            print(f'{self.location} 逐小时历史气象数据拉取完毕。')
            # 获取逐日数据
            file_name = f"{self.location}_2000-2025_history_meteo_daily_analysis.parquet"
            file_abs_path = os.path.join(self.daily_history_meteo_data_path, file_name)
            temp_csv_path = os.path.join(self.temp_data_path, file_name.replace(".parquet", ".csv"))
            if not os.path.exists(file_abs_path):
                file_url = f"https://app.cornicelli.net/meteo/download/history_analysis/daily/{self.location}/"
                data_file_csv = self.session.get(file_url)
                with open(temp_csv_path, "wb") as f:
                    f.write(data_file_csv.content)
            df = pd.read_csv(temp_csv_path)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df.to_parquet(file_abs_path, engine='pyarrow', compression='snappy')  # zstd
            print(f'{self.location} 逐日历史气象数据拉取完毕。')
            # 拉取逐月数据
            file_name = f"{self.location}_2000-2025_history_meteo_monthly_analysis.parquet"
            file_abs_path = os.path.join(self.monthly_history_meteo_data_path, file_name)
            temp_csv_path = os.path.join(self.temp_data_path, file_name.replace(".parquet", ".csv"))
            if not os.path.exists(file_abs_path):
                file_url = f"https://app.cornicelli.net/meteo/download/history_analysis/monthly/{self.location}/"
                data_file_csv = self.session.get(file_url)
                with open(temp_csv_path, "wb") as f:
                    f.write(data_file_csv.content)
            df = pd.read_csv(temp_csv_path)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df.to_parquet(file_abs_path, engine='pyarrow', compression='snappy')  # zstd
            print(f'{self.location} 逐月历史气象数据拉取完毕。')
            # 拉取逐年数据
            file_name = f"{self.location}_2000-2025_history_meteo_yearly_analysis.parquet"
            file_abs_path = os.path.join(self.yearly_history_meteo_data_path, file_name)
            temp_csv_path = os.path.join(self.temp_data_path, file_name.replace(".parquet", ".csv"))
            if not os.path.exists(file_abs_path):
                file_url = f"https://app.cornicelli.net/meteo/download/history_analysis/yearly/{self.location}/"
                data_file_csv = self.session.get(file_url)
                with open(temp_csv_path, "wb") as f:
                    f.write(data_file_csv.content)
            df = pd.read_csv(temp_csv_path)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df.to_parquet(file_abs_path, engine='pyarrow', compression='snappy')  # zstd
            print(f'{self.location} 逐年历史气象数据拉取完毕。')
        if self.forecast_mode == 'on':
            # 预报最新数据
            date_now = datetime.datetime.now().strftime("%Y-%m-%d")
            file_name = f"{self.location}.csv"
            file_abs_path = os.path.join(self.forecast_data_path, file_name)
            temp_csv_path = os.path.join(self.temp_data_path, file_name)
            if not os.path.exists(temp_csv_path):
                print(f"正在从云端拉取 {self.location} 最新天气预报数据······")
                forecast_daily_url = f"https://app.cornicelli.net/meteo/api/forecast/daily/{self.location}/{date_now[:4]}/{date_now[5:7]}/{date_now[8:]}/{self.api_key}"
                response_bytes = requests.get(forecast_daily_url)
                json_str = response_bytes.content.decode('utf-8')
                data_dic = json.loads(json_str)
                df = pd.DataFrame.from_dict(data_dic)
                with open(temp_csv_path, "wb") as f:
                    df.to_csv(temp_csv_path, index=False)
            df = pd.read_csv(temp_csv_path)
            df.drop('Unnamed: 0', axis=1, inplace=True)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df.to_csv(file_abs_path, index=True)  # zstd
            print(f'{self.location} 今日天气预报数据拉取完毕。')
        self.data_status_check()

    def fetch_locations_data(self, locations):
        old_location = self.location
        count = 0
        for location in locations:
            progress = round(count / len(locations) * 100, 0)
            print(f'任务进度：{progress}%。已完成{count}个地点，共计{len(locations)}个。')
            self.set_location(location)
            count += 1
        self.location = old_location

    def fetch_all_latest_forecast_data(self):
        self.session = self.login_account()
        if self.account_type != '专业用户':
            print('用户权限不足，无法自动从云端拉取数据，请订阅专业用户。\n在线支持：https://cornicelli.net/meteo/doc')
            return 0
        # 预报最新数据
        date_now = datetime.datetime.now().strftime("%Y-%m-%d")
        file_name = f"ecmwf_cn_10_days_hourly_weather_forecast_csv_{date_now}.zip"
        temp_zip_path = os.path.join(self.temp_data_path, file_name)
        if not os.path.exists(temp_zip_path):
            file_url = (f"https://app.cornicelli.net/meteo/download/project/cn"
                        f"/ecmwf_cn_10_days_hourly_weather_forecast_csv_{date_now}.zip")
            print('正在下载今日天气预报数据······')
            data_file_zip = self.session.get(file_url)
            with open(temp_zip_path, "wb") as f:
                f.write(data_file_zip.content)
        print('正在解压今日天气预报数据······')
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.forecast_data_path)
        forecast_file_count = len(os.listdir(self.forecast_data_path))
        print(f'今日 {forecast_file_count} 个地点天气预报数据拉取完毕。')
        print(f'请在{self.forecast_data_path} 目录查看。')

    def set_location(self, location):
        self.location = location
        location_hourly_data_path = os.path.join(self.hourly_history_meteo_data_path, self.location)
        if self.location != '' and not os.path.exists(location_hourly_data_path):
            p = Path(location_hourly_data_path)
            p.mkdir(parents=True, exist_ok=True)
            print(f'{self.location} 工作目录已创建：{location_hourly_data_path}')
        if not self.data_status_check():
            print(f'{self.location} 数据存在缺失，现在开始从云端拉取缺失数据。')
            self.fetch_data()
        else:
            print(f'{self.location} 数据完整性校验通过。可以继续运行统计分析任务。')

    def data_status_check(self):
        data_all_ok = True
        if self.history_mode == 'on':
            # 验证逐小时历史数据、逐日历史数据、逐月历史数据、逐年历史数据
            years = self.years
            for year in years:
                file_name = f"{year}_{self.location}_history_meteo_data.parquet"
                file_abs_path = os.path.join(self.hourly_history_meteo_data_path, self.location, file_name)
                if not os.path.exists(file_abs_path):
                    print(f'{self.location} {year} 逐小时历史数据不存在。')
                    data_all_ok = False
            # 验证逐日数据完整性
            file_name = f"{self.location}_2000-2025_history_meteo_daily_analysis.parquet"
            file_abs_path = os.path.join(self.daily_history_meteo_data_path, file_name)
            if not os.path.exists(file_abs_path):
                print(f'{self.location} 逐日历史数据不存在。')
                data_all_ok = False
            # 验证逐月数据完整性
            file_name = f"{self.location}_2000-2025_history_meteo_monthly_analysis.parquet"
            file_abs_path = os.path.join(self.monthly_history_meteo_data_path, file_name)
            if not os.path.exists(file_abs_path):
                print(f'{self.location} 逐月历史数据不存在。')
                data_all_ok = False
            # 验证逐年数据完整性
            file_name = f"{self.location}_2000-2025_history_meteo_yearly_analysis.parquet"
            file_abs_path = os.path.join(self.yearly_history_meteo_data_path, file_name)
            if not os.path.exists(file_abs_path):
                print(f'{self.location} 逐年历史数据不存在。')
                data_all_ok = False
        # 验证预报数据完整性
        if self.forecast_mode == 'on':
            try:
                file_name = f"{self.location}.csv"
                latest_forecast_data_file = os.path.join(self.forecast_data_path, file_name)
                df = pd.read_csv(latest_forecast_data_file)
                first_row_date = str(df['date'].iloc[0])[:10]
                date_now = datetime.datetime.now().strftime("%Y-%m-%d")
                if first_row_date != date_now:
                    print(f"{self.location} 天气预报数据过期。")
                    data_all_ok = False
            except:
                print(f"{self.location} 天气预报数据不存在。")
                data_all_ok = False
        return data_all_ok

    def set_forecast_mode(self, code):
        if code != 'on' and code != 'off':
            print("请指定预报数据模式为‘on’或者‘off’。")
            return 0
        self.forecast_mode = code

    def set_history_mode(self, code):
        if code != 'on' and code != 'off':
            print("请指定预报数据模式为‘on’或者‘off’。")
            return 0
        self.history_mode = code

    def hourly_value(self, meteo_types, year, month, day, hour):
        meteo_types = [
            meteo_type.removesuffix("_min").removesuffix("_max").removesuffix("_mean").removesuffix("_average").removesuffix("_sum") for
            meteo_type in meteo_types]
        file_name = f"{year}_{self.location}_history_meteo_data.parquet"
        file_abs_path = os.path.join(self.hourly_history_meteo_data_path, self.location, file_name)
        with open(file_abs_path, 'rb') as f:
            df = pd.read_parquet(f)
        target_time = datetime.datetime(year=year, month=month, day=day, hour=hour)
        result = df.loc[target_time, meteo_types]
        print(result)
        return result

    def hourly_series(self, meteo_types, start_year, start_month, start_day, start_hour, end_year, end_month,
                      end_day, end_hour):
        meteo_types = [
            meteo_type.removesuffix("_min").removesuffix("_max").removesuffix("_mean").removesuffix("_average").removesuffix("_sum") for
            meteo_type in meteo_types]
        start_time = datetime.datetime(year=start_year, month=start_month, day=start_day, hour=start_hour)
        end_time = datetime.datetime(year=end_year, month=end_month, day=end_day, hour=end_hour)
        if start_year == end_year:
            file_name = f"{start_year}_{self.location}_history_meteo_data.parquet"
            file_abs_path = os.path.join(self.hourly_history_meteo_data_path, self.location, file_name)
            with open(file_abs_path, 'rb') as f:
                df = pd.read_parquet(f)
        else:
            years = range(start_year, end_year + 1)
            file_names = [f"{year}_{self.location}_history_meteo_data.parquet" for year in years]
            file_list = [os.path.join(self.hourly_history_meteo_data_path, self.location, file_name) for file_name in file_names]
            df = pd.concat([pd.read_parquet(f) for f in file_list])  # 不要使用ignore_index=True，会删除date索引导致数据无法读取
        result = df.loc[start_time:end_time, meteo_types]
        print(result)
        return result

    def daily_value(self, meteo_types, year, month, day):
        target_time = datetime.datetime(year=year, month=month, day=day)
        file_name = f"{self.location}_2000-2025_history_meteo_daily_analysis.parquet"
        file_abs_path = os.path.join(self.daily_history_meteo_data_path, file_name)
        with open(file_abs_path, 'rb') as f:
            df = pd.read_parquet(f)
        result = df.loc[target_time, meteo_types]
        print(result)
        return result

    def daily_series(self, meteo_types, start_year, start_month, start_day, end_year, end_month, end_day):
        start_time = datetime.datetime(year=start_year, month=start_month, day=start_day)
        end_time = datetime.datetime(year=end_year, month=end_month, day=end_day)
        file_name = f"{self.location}_2000-2025_history_meteo_daily_analysis.parquet"
        file_abs_path = os.path.join(self.daily_history_meteo_data_path, file_name)
        with open(file_abs_path, 'rb') as f:
            df = pd.read_parquet(f)
        result = df.loc[start_time:end_time, meteo_types]
        print(result)
        return result

    def monthly_value(self, meteo_types, year, month):
        target_time = datetime.datetime(year=year, month=month, day=1)
        file_name = f"{self.location}_2000-2025_history_meteo_monthly_analysis.parquet"
        file_abs_path = os.path.join(self.monthly_history_meteo_data_path, file_name)
        with open(file_abs_path, 'rb') as f:
            df = pd.read_parquet(f)
        result = df.loc[target_time, meteo_types]
        print(result)
        return result

    def monthly_series(self, meteo_types, start_year, start_month, end_year, end_month):
        start_time = datetime.datetime(year=start_year, month=start_month, day=1)
        end_time = datetime.datetime(year=end_year, month=end_month, day=1)
        file_name = f"{self.location}_2000-2025_history_meteo_monthly_analysis.parquet"
        file_abs_path = os.path.join(self.monthly_history_meteo_data_path, file_name)
        with open(file_abs_path, 'rb') as f:
            df = pd.read_parquet(f)
        result = df.loc[start_time:end_time, meteo_types]
        print(result)
        return result

    def yearly_value(self, meteo_types, year):
        target_time = datetime.datetime(year=year, month=1, day=1)
        file_name = f"{self.location}_2000-2025_history_meteo_yearly_analysis.parquet"
        file_abs_path = os.path.join(self.yearly_history_meteo_data_path, file_name)
        with open(file_abs_path, 'rb') as f:
            df = pd.read_parquet(f)
        result = df.loc[target_time, meteo_types]
        print(result)
        return result

    def yearly_series(self, meteo_types, start_year, end_year):
        start_time = datetime.datetime(year=start_year, month=1, day=1)
        end_time = datetime.datetime(year=end_year, month=1, day=1)
        file_name = f"{self.location}_2000-2025_history_meteo_yearly_analysis.parquet"
        file_abs_path = os.path.join(self.yearly_history_meteo_data_path, file_name)
        with open(file_abs_path, 'rb') as f:
            df = pd.read_parquet(f)
        result = df.loc[start_time:end_time, meteo_types]
        print(result)
        return result

    def forecast_hourly_series(self):
        file_name = f"{self.location}.csv"
        file_abs_path = os.path.join(self.forecast_data_path, file_name)
        df = pd.read_csv(file_abs_path)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        print(df)
        return df

    def forecast_daily_series(self):
        file_name = f"{self.location}.csv"
        file_abs_path = os.path.join(self.forecast_data_path, file_name)
        df = pd.read_csv(file_abs_path)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        daily_df = df.resample('D').agg({
            'temperature_2m': ['min', 'max', 'mean'],
            'apparent_temperature': ['min', 'max', 'mean'],
            'surface_temperature': ['min', 'max', 'mean'],
            'dew_point_2m': ['min', 'max', 'mean'],
            'pressure_msl': ['min', 'max', 'mean'],
            'surface_pressure': ['min', 'max', 'mean'],
            'runoff': ['min', 'max', 'mean'],
            'relative_humidity_2m': ['min', 'max', 'mean'],
            'wind_speed_10m': ['min', 'max', 'mean'],
            'wind_gusts_10m': ['min', 'max', 'mean'],
            'wind_direction_10m': average,
            'wind_speed_100m': ['min', 'max', 'mean'],
            'wind_direction_100m': average,
            'precipitation': 'sum',
            'weather_code': 'max',
            'cloud_cover': ['min', 'max', 'mean'],
            'cape': ['min', 'max', 'mean'],
            'shortwave_radiation_instant': ['min', 'max', 'mean'],
            'vapour_pressure_deficit': ['min', 'max', 'mean'],
            'soil_temperature_0_to_7cm': ['min', 'max', 'mean'],
            'soil_moisture_0_to_7cm': ['min', 'max', 'mean'],
            'soil_moisture_7_to_28cm': ['min', 'max', 'mean'],
            'total_column_integrated_water_vapour': ['min', 'max', 'mean'],
        })
        daily_df.columns = [f"{col[0]}_{col[1]}" if isinstance(col, tuple) else col for col in daily_df.columns]
        print(daily_df)
        return daily_df

    def find_location_by_coords(self, lon, lat):
        self.session = self.login_account()
        if self.account_type != '专业用户':
            print('用户权限不足，无法使用经纬度查询地名接口，请订阅专业用户。\n在线支持：https://cornicelli.net/meteo/doc')
            return 0
        # 预查询经纬度、海拔
        coords_info_url = f"https://app.cornicelli.net/meteo/api/gis/coords_location/{lon}/{lat}/{self.api_key}"
        coords_info_data = requests.get(coords_info_url).json()
        print(coords_info_data['description'])
        return coords_info_data['name']

    def api_forecast_hourly(self):
        self.session = self.login_account()
        if self.account_type != '专业用户':
            print('用户权限不足，无法自动从云端拉取数据，请订阅专业用户。\n在线支持：https://cornicelli.net/meteo/doc')
            return 0
        date_now = datetime.datetime.now().strftime('%Y-%m-%d')
        forecast_daily_url = f"https://app.cornicelli.net/meteo/api/forecast/daily/{self.location}/{date_now[:4]}/{date_now[5:7]}/{date_now[8:]}/{self.api_key}"
        response_bytes = requests.get(forecast_daily_url)
        json_str = response_bytes.content.decode('utf-8')
        data_dic = json.loads(json_str)
        df = pd.DataFrame.from_dict(data_dic)
        df.drop('Unnamed: 0', axis=1, inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        print(df)
        return df

    def api_forecast_hourly_by_coords(self, lon, lat):
        self.session = self.login_account()
        if self.account_type != '专业用户':
            print('用户权限不足，无法自动从云端拉取数据，请订阅专业用户。\n在线支持：https://cornicelli.net/meteo/doc')
            return 0
        forecast_coords_url = f"https://app.cornicelli.net/meteo/api/forecast/daily_coords/{lon}/{lat}/{self.api_key}"
        response_bytes = requests.get(forecast_coords_url)
        json_str = response_bytes.content.decode('utf-8')
        data_dic = json.loads(json_str)
        df = pd.DataFrame.from_dict(data_dic)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        print(df)
        return df

    def api_history_hourly_of_day(self, year, month, day):
        self.session = self.login_account()
        if self.account_type != '专业用户':
            print('用户权限不足，无法自动从云端拉取数据，请订阅专业用户。\n在线支持：https://cornicelli.net/meteo/doc')
            return 0
        history_daily_url = f"https://app.cornicelli.net/meteo/api/history/daily/{self.location}/{year}/{month}/{day}/{self.api_key}"
        response_bytes = requests.get(history_daily_url)
        json_str = response_bytes.content.decode('utf-8')
        data_dic = json.loads(json_str)
        df = pd.DataFrame.from_dict(data_dic)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        print(df)
        return df

    def api_history_hourly_of_month(self, year, month):
        self.session = self.login_account()
        if self.account_type != '专业用户':
            print('用户权限不足，无法自动从云端拉取数据，请订阅专业用户。\n在线支持：https://cornicelli.net/meteo/doc')
            return 0
        history_monthly_url = f"https://app.cornicelli.net/meteo/api/history/monthly/{self.location}/{year}/{month}/{self.api_key}"
        response_bytes = requests.get(history_monthly_url)
        json_str = response_bytes.content.decode('utf-8')
        data_dic = json.loads(json_str)
        df = pd.DataFrame.from_dict(data_dic)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        print(df)
        return df

    def api_history_hourly_of_year(self, year):
        self.session = self.login_account()
        if self.account_type != '专业用户':
            print('用户权限不足，无法自动从云端拉取数据，请订阅专业用户。\n在线支持：https://cornicelli.net/meteo/doc')
            return 0
        history_yearly_url = f"https://app.cornicelli.net/meteo/api/history/yearly/{self.location}/{year}/{self.api_key}"
        response_bytes = requests.get(history_yearly_url)
        json_str = response_bytes.content.decode('utf-8')
        data_dic = json.loads(json_str)
        df = pd.DataFrame.from_dict(data_dic)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        print(df)
        return df

    def api_history_analysis(self, time_type):
        self.session = self.login_account()
        if self.account_type != '专业用户':
            print('用户权限不足，无法自动从云端拉取数据，请订阅专业用户。\n在线支持：https://cornicelli.net/meteo/doc')
            return 0
        history_analysis_url = f"https://app.cornicelli.net/meteo/api/history_analysis/{time_type}/{self.location}/{self.api_key}/"
        response_bytes = requests.get(history_analysis_url)
        json_str = response_bytes.content.decode('utf-8')
        data_dic = json.loads(json_str)
        df = pd.DataFrame.from_dict(data_dic)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        print(df)
        return df


def average(angles_deg):
    radians = np.radians(angles_deg)
    sin_avg = np.nanmean(np.sin(radians))
    cos_avg = np.nanmean(np.cos(radians))
    avg_rad = np.arctan2(sin_avg, cos_avg)
    avg_deg = np.degrees(avg_rad)
    return (avg_deg + 360) % 360

