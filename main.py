'''
海天气象HtMeteo超级信息体使用示例代码
海天气象HtMeteo超级信息体，是海天气象数据信息服务平台开发的，基于平台数据合集和在线API的Python程序库，它能够实现账户认证、气象数据下载、气象数据
统计分析、气象数据在线API调用等功能，将海天气象平台的所有数据资源和在线接口整合在了一个Python库中，因此形象被命名为“超级信息体”。
开发它的初衷是为了变革气象领域科研人员、应用人员、学生获取地面气象数据的方式，无论是历史天气数据还是天气预报数据，它能够最大限度减少气象数据用户在数据
查找、统计分析、整理订正、存储调取环节的时间耗费，一站式解决所有的科研任务和实践应用的数据准备问题，让用户不再受制于数据准备的羁绊，从而专注于对
气象数据的潜能开发和价值创造。
在线支持：https://cornicelli.net/meteo/doc
'''
from HtMeteo import HtMeteo

# -------------------------基本参数-------------------------
location = '西安市'
# locations = ['北京市', '三原县', '喀什地区', '贡山独龙族怒族自治县', '海北藏族自治州']
meteo_types = ['temperature_2m_max',
               'surface_pressure_mean',
               'relative_humidity_2m_mean',
               'wind_speed_10m_mean',
               'precipitation_sum',
               'shortwave_radiation_min']

target_year, target_month, target_day, target_hour = 2019, 4, 20, 18

start_year, start_month, start_day, start_hour = 2019, 12, 25, 18
end_year, end_month, end_day, end_hour = 2020, 3, 26, 18

# -------------------------用户认证 示例代码-------------------------
# 初始化HtMeteo超级信息体
h = HtMeteo(username='htqx', password='C0rn!ce11!')  # 指定海天气象用户名和密码
# h = HtMeteo()  # 不指定用户名和密码，无法拉取在线数据，只能分析本地数据
# h.login_account()
print(h.account_info)  # 查看账户信息
print(h.username, h.password, h.api_key, h.account_type, h.subscribe_days)  # 分别查看用户名、密码、api_key、用户类型、订阅时间

# -------------------------历史天气数据统计分析 示例代码-------------------------
h = HtMeteo(username='htqx', password='C0rn!ce11!')  # 实例化超级信息体
h.set_location('西安市')  # 设定地点，会自动检测目录数据状态，如果数据缺失会自动从云端拉取，默认只拉区历史数据，如果需要预报数据需开启预报模式

# 1.获取单一时间历史气象数据，
# 读取西安市2019年4月20日18时历史气象数据，包含气象要素：2米气温、平均地面气压、平均2米相对湿度、10米平均风速、累积降水量和短波辐射
# 可以指定meteo_types参数改变气象要素类型，所有的历史气象要素列表在文档末尾，meteo_types是一个列表
# meteo_types = history_meteo_types_options  # 指定所有气象要素
h.hourly_value(meteo_types=meteo_types, year=target_year, month=target_month, day=target_day, hour=target_hour)
# 返回pandas series类型，可以通过气象要素名称索引
meteo_data = h.hourly_value(meteo_types=meteo_types, year=target_year, month=target_month, day=target_day,
                            hour=target_hour)
print(meteo_data['temperature_2m'])  # 输出2米气温数值
print(meteo_data.index)  # 查看所有索引

# 读取西安市2019年4月20日历史气象数据
h.daily_value(meteo_types=meteo_types, year=2019, month=4, day=20)

# 读取西安市2019年4月历史气象数据
h.monthly_value(meteo_types=meteo_types, year=2019, month=4)

# 读取西安市2019年历史气象数据
h.yearly_value(meteo_types=meteo_types, year=2019)

# 2.获取时间段内连续历史气象数据
# 读取西安市2019年12月31日0时至2020年1月1日23时历史气象数据
h.hourly_series(meteo_types=meteo_types,
                start_year=2019, start_month=12, start_day=31, start_hour=0,
                end_year=2020, end_month=1, end_day=1, end_hour=23)  # 起止时间都包含，可跨年读取
# 返回pandas dataframe，可以通过时间、气象要素名称索引
meteo_data = h.hourly_series(meteo_types=meteo_types,
                             start_year=2019, start_month=12, start_day=31, start_hour=0,
                             end_year=2020, end_month=1, end_day=1, end_hour=23)
print(meteo_data['temperature_2m'].iloc[0])  # 输出第一个2米气温数值
print(meteo_data['wind_speed_10m'].iloc[-5:].tolist())  # 输出最后5个10米平均风速数值，并转换为列表
print(meteo_data.index)  # 查看所有索引
print(meteo_data.columns)  # 查看所有列名

# 读取西安市2019年12月31日至2020年1月1日历史气象数据
h.daily_series(meteo_types=meteo_types,
               start_year=2019, start_month=12, start_day=31,
               end_year=2020, end_month=1, end_day=1)  # 起止时间都包含，可跨年读取

# 读取西安市2019年12月31日至2020年1月1日历史气象数据
h.monthly_series(meteo_types=meteo_types,
                 start_year=2019, start_month=12,
                 end_year=2020, end_month=1)  # 起止时间都包含，可跨年读取

# 读取西安市2019年至2025年历史气象数据
h.yearly_series(meteo_types=meteo_types,
                start_year=2019,
                end_year=2025)  # 起止时间都包含，可跨年读取

# -------------------------天气预报数据统计分析 示例代码-------------------------
# 3.读取预报数据
h.set_forecast_mode('on')  # 开启预报模式，预报模式默认为关闭，开启后方能使用预报数据读取功能，如果关闭不会下载天气预报数据
h.set_history_mode('off')  # 如果不使用历史数据，可以先关闭它，否则设定地点后，历史数据也会被自动下载，耗费时间
h.set_location('三原县')
# 读取三原县未来240小时逐小时天气预报原始数据
h.forecast_hourly_series()
meteo_data = h.forecast_daily_series()
print(meteo_data.columns)  # 查看所有气象要素名称

# 读取三原县未来10日逐日天气预报统计分析数据
h.forecast_daily_series()
meteo_data = h.forecast_daily_series()
print(meteo_data.columns)  # 查看所有气象要素名称

# 4.只想下载数据，或者关注的地点较多，想先下载完数据再读取处理以节省时间
locations = ['南京市', '疏勒县', '顺德区', '大理白族自治州']
h.set_forecast_mode('on')  # 开启预报数据模式，若关闭则不会下载预报数据
h.set_history_mode('on')  # 开启历史数据模式，否则不会下载历史数据
# 如果不设定历史数据模式或者预报数据模式，则只下载历史数据，因为预报数据模式默认为关闭状态
h.fetch_locations_data(locations)

# 5.批量下载全国3191个市区县预报数据3191
h.fetch_all_latest_forecast_data()

# 6.需要查询经纬度所在地名和海拔
lon, lat = 116, 40
h.find_location_by_coords(lon, lat)
location_name = h.find_location_by_coords(lon, lat)  # 将查询到的坐标地点名称赋值给location_name
# time.sleep(1000)

# -------------------------在线API 示例代码-------------------------
# 7.直接从API调取数据，不再下载数据到本地
h.set_forecast_mode('off')  # 关闭预报数据模式，不再从云端下载数据到本地，直接API调取
h.set_history_mode('off')  # 关闭历史数据模式，不再从云端下载数据到本地，直接API调取
# 通过地名调取未来10日逐小时天气预报数据
meteo_data = h.api_forecast_hourly()  # 从API直接调取西安市未来10日逐小时天气预报数据
print(meteo_data.index)  # 输出时间索引
print(meteo_data.columns)  # 输出气象要素列表

# 通过经纬度坐标调取未来10日逐小时天气预报数据
lon, lat = 116, 40
meteo_data = h.api_forecast_hourly_by_coords(lon, lat)  # 从API直接调取西安市未来10日逐小时天气预报数据
print(meteo_data.index)  # 输出时间索引
print(meteo_data.columns)  # 输出气象要素列表

# 调取某一天的逐小时历史天气数据
year, month, day = 2019, 4, 20
meteo_data = h.api_history_hourly_of_day(year, month, day)  # 从API直接调取西安市2019年4月20日的逐小时历史天气数据
print(meteo_data.index)  # 输出时间索引
print(meteo_data.columns)  # 输出气象要素列表

# 调取某一月的逐小时历史天气数据
year, month = 2019, 4
meteo_data = h.api_history_hourly_of_month(year, month)  # 从API直接调取西安市2019年4月的逐小时历史天气数据
print(meteo_data.index)  # 输出时间索引
print(meteo_data.columns)  # 输出气象要素列表

# 调取某一年的逐小时历史天气数据
year = 2019
meteo_data = h.api_history_hourly_of_year(year)  # 从API直接调取西安市2019年的逐小时历史天气数据
print(meteo_data.index)  # 输出时间索引
print(meteo_data.columns)  # 输出气象要素列表

# 调取2000~2025年全时段统计分析历史天气数据
time_type = 'monthly'  # 'daily''monthly''yearly' 三选一，分别代表日、月、年尺度的统计分析数据
meteo_data = h.api_history_analysis(time_type)  # 从API直接调取西安市2000~2025年的月统计分析历史天气数据
print(meteo_data.index)  # 输出时间索引
print(meteo_data.columns)  # 输出气象要素列表


# 8.其他功能
# h.clear_work_dirs()  # 清空./data目录内的所有数据，重置工作目录，谨慎操作

# 9.注意事项
# 全国有大约30个区名重复，冠以所在市名称加以区分，全国市区县地名清单下载地址：https://cornicelli.net/meteo/doc

# 附录：历史气象数据中的气象要素列表
history_meteo_types_options = [
    'temperature_2m_min',
    'temperature_2m_max',
    'temperature_2m_mean',
    'dew_point_2m_min',
    'dew_point_2m_max',
    'dew_point_2m_mean',
    'pressure_msl_min',
    'pressure_msl_max',
    'pressure_msl_mean',
    'surface_pressure_min',
    'surface_pressure_max',
    'surface_pressure_mean',
    'relative_humidity_2m_min',
    'relative_humidity_2m_max',
    'relative_humidity_2m_mean',
    'wind_speed_10m_min',
    'wind_speed_10m_max',
    'wind_speed_10m_mean',
    'wind_gusts_10m_min',
    'wind_gusts_10m_max',
    'wind_gusts_10m_mean',
    'wind_direction_10m_average',
    'wind_speed_100m_min',
    'wind_speed_100m_max',
    'wind_speed_100m_mean',
    'wind_direction_100m_average',
    'precipitation_sum',
    'weather_code_max',
    'cloud_cover_min',
    'cloud_cover_max',
    'cloud_cover_mean',
    'shortwave_radiation_min',
    'shortwave_radiation_max',
    'shortwave_radiation_mean',
    'boundary_layer_height_min',
    'boundary_layer_height_max',
    'boundary_layer_height_mean',
    'et0_fao_evapotranspiration_min',
    'et0_fao_evapotranspiration_max',
    'et0_fao_evapotranspiration_mean',
    'vapour_pressure_deficit_min',
    'vapour_pressure_deficit_max',
    'vapour_pressure_deficit_mean',
    'soil_temperature_7_to_28cm_min',
    'soil_temperature_7_to_28cm_max',
    'soil_temperature_7_to_28cm_mean',
    'soil_temperature_28_to_100cm_min',
    'soil_temperature_28_to_100cm_max',
    'soil_temperature_28_to_100cm_mean',
    'soil_temperature_100_to_255cm_min',
    'soil_temperature_100_to_255cm_max',
    'soil_temperature_100_to_255cm_mean',
    'soil_moisture_7_to_28cm_min',
    'soil_moisture_7_to_28cm_max',
    'soil_moisture_7_to_28cm_mean',
    'soil_moisture_28_to_100cm_min',
    'soil_moisture_28_to_100cm_max',
    'soil_moisture_28_to_100cm_mean',
    'soil_moisture_100_to_255cm_min',
    'soil_moisture_100_to_255cm_max',
    'soil_moisture_100_to_255cm_mean',
    'total_column_integrated_water_vapour_min',
    'total_column_integrated_water_vapour_max',
    'total_column_integrated_water_vapour_mean',
]
# 天气预报数据中的气象要素列表，日统计分析天气预报数据舍弃了一些用不着的气象要素
forecast_meteo_types_options = [
    'date',
    'temperature_2m',
    'relative_humidity_2m',
    'dew_point_2m',
    'apparent_temperature',
    'precipitation',
    'rain',
    'snowfall',
    'weather_code',
    'pressure_msl',
    'surface_pressure',
    'cloud_cover',
    'cloud_cover_low',
    'cloud_cover_mid',
    'cloud_cover_high',
    'vapour_pressure_deficit',
    'wind_speed_10m',
    'wind_speed_100m',
    'wind_direction_10m',
    'wind_direction_100m',
    'wind_gusts_10m',
    'surface_temperature',
    'soil_temperature_0_to_7cm',
    'soil_moisture_0_to_7cm',
    'soil_moisture_7_to_28cm',
    'runoff',
    'cape',
    'total_column_integrated_water_vapour',
    'shortwave_radiation_instant',
    'direct_radiation_instant',
    'diffuse_radiation_instant',
    'direct_normal_irradiance_instant',
    'global_tilted_irradiance_instant'
]
