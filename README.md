# 使用`HtMeteo`超级气象信息体轻松玩转气象数据

## 写在前面

无论是从事气候分析领域的科研人员还是从事电力、运输、农业、生态应用领域的从业人员，无论是气象数据规模化应用的大数据分析师还是零散调取的学生用户，无论是统计分析历史气候资料还是展示城市中期天气预报信息，无论是本地气象模型运算还是网页端气象信息发布，在气象数据五花八门的应用场景中，用户通常查询下载气象数据耗费了相当多的精力和时间，现在HtMeteo超级气象信息体出现了，它会深刻改变这种局面，让所有的气象数据用户，无论是资深研究人员还是入门新手，无论是核心气象领域还是边缘应用领域，都将能够轻松触及任何地面气象观测数据。

## `HtMeteo`超级气象信息体简介

海天气象数据信息服务平台一直在探索如何优雅实现一行代码获取全国任意地点地面历史气象数据和天气预报数据。海天气象`HtMeteo`（/hæt 'miːtiə/）超级气象信息体，是海天气象数据信息服务平台开发的，基于平台数据合集和在线API的Python程序库，它能够实现账户认证、气象数据下载、气象数据 统计分析、气象数据在线API调用等功能，将海天气象平台的所有数据资源和在线接口整合在了一个Python库中，因此形象被命名为“超级信息体”。 开发它的初衷是为了变革气象领域科研人员、应用人员、学生获取地面气象数据的方式，让气象数据用户摒弃传统的数据检索整编下载思维，有了HtMeteo即可随时随地通过三两行极简的Python代码获取任何想要的地面气象数据，无论是历史天气数据还是天气预报数据，它能够最大限度减少气象数据用户在数据 查找、统计分析、整理订正、存储调取环节的时间耗费，一站式解决所有的科研任务和实践应用的数据准备问题，让用户不再受制于气象数据检索的羁绊，从而专注于对气象数据的潜能开发和价值创造。`HtMeteo`能最大限度适应追求以极简、优雅的方式调取气象数据的人。 总的来说`HtMeteo`超级气象信息体具有如下特点：

- 数据驱动强力。底层数据由[海天气象](https://cornicelli.net/)数据信息服务平台驱动
- 一站式集成。同时具备气象数据查询、下载、统计分析功能
- 极致精简。一行代码获取全国任意地点任意气象要素任意时间或时段的气象数据
- 数据组织高效。所有数据按地名索引，通过任意市、区、县地名查找气象数据
- 工作流程清晰。工作流程符合人类思维，即使是非气象专业人员也能轻松上手
- 高度自动化。用户仅通过接口查询数据无需配置环境、处理数据、编写统计分析算法
- 文档齐全。丰富的数据说明文档和全套示例代码，满足“复制粘贴”式编程需求
- 开箱即用。仅需一个py文件实现全部数据调取和统计分析功能
- 自由灵活。可选择是否缓存数据到本地，也可仅下载数据用户自行统计分析
- 长期演进。会有更丰富的气象数据接入和更强大的数据可视化方法加入

## 一、如何使用

安装软件？不需要。配置环境和策略？不需要。甚至联网有时也不需要。要说它什么也不需要？那当然也不是。理论上用户只需要一个HtMeteo.py文件和一个[海天气象](https://cornicelli.net/)账户即可。当然你还得有一台安装了Python环境的计算机。或者手机？
如果要使用`HtMeteo`超级气象信息体，**无需将本仓库全部拉取到本地计算机**，只下载一个`HtMeteo.py`文件即可，如果想省事再下载一个`requirement.txt`使用`pip install -r requirement.txt`命令安装全部依赖。现在再在同一目录下创建一个`main.py`文件即可开始。

### 1.通过几个简单示例快速入门

我们对`HtMeteo`超级气象信息体的设计和Python语言一样遵循极简哲学，任何多余的代码和字符我们都不想要。试想你是一位气象领域的研究人员，现在你的课题想让你立马知道2019年4月20日18时西安市的气温是多少，你就可以这么干（编辑你的`main.py`文件）：

```python
from HtMeteo import HtMeteo

h = HtMeteo(username='username', password='password')  #使用海天气象用户名和密码实例化HtMeteo超级信息体
h.set_location('西安市')  # 设定地点
h.hourly_value(meteo_types=['temperature_2m'], year=2019, month=4, day=20, hour=18)
```

现在你将看到屏幕上输出了以下内容：

```python
temperature_2m           16.5
```

没错，西安市2019年4月20日18时西安市的气温就是16.5℃。以上代码发生了什么？简要地讲，你刚干了这些事：
导入`HtMeteo`超级气象信息体并将其实例化为`h`，然后你告诉`h`你现在关注的地点叫“西安市”，并让它帮你调取了西安市2019年4月20日18时西安市的气温数据。

再比如你是一位农业专家，想知道农作物能不能熬过8月的高温天气，现在要查一下去年西安市8月每天的最高温度是多少，就可以像这样：

```python
h.daily_series(meteo_types=['temperature_2m_max'],
               start_year=2025, start_month=8, start_day=1,
               end_year=2025, end_month=8, end_day=31)  # 起止时间都包含，可跨年读取
```

现在HtMeteo已经为你返回了2025年8月西安市每一天的最高气温：

```python
date			temperature_2m_max
2025-08-01                40.0
2025-08-02                41.3
2025-08-03                41.8
···
2025-08-29                24.2
2025-08-30                22.0
2025-08-31                28.8
```

再比如你既不是什么研究人员也不是什么专家，只想知道未来几天顺德区有没有雨，现在就可以这样查看它未来10天的降水预报：

```python
h.set_forecast_mode('on')  # 打开预报模式，它默认是关闭的
h.set_location('顺德区')
h.forecast_daily_series()['precipitation_sum']  # 读取顺德区未来10日逐日累积降水量天气预报数据
```

现在你的屏幕上将出现下列内容：

```python
date
2026-03-07 00:00:00+00:00    0.0
2026-03-08 00:00:00+00:00    0.0
2026-03-09 00:00:00+00:00    0.0
2026-03-10 00:00:00+00:00    0.0
2026-03-11 00:00:00+00:00    0.0
2026-03-12 00:00:00+00:00    0.0
2026-03-13 00:00:00+00:00    0.0
2026-03-14 00:00:00+00:00    0.0
2026-03-15 00:00:00+00:00    0.0
2026-03-16 00:00:00+00:00    0.0
Freq: D, Name: precipitation_sum, dtype: float64
```

看来顺德区未来10天都不下雨，如上所示，它3月7日到10日每天的累积降水量都是0.0 mm。
或许你对`meteo_types=['temperature_2m_max']`参数感到好奇，它是一个气象要素名称字符串列表，前面的例子列表中只有1个元素，如果需要多种气象要素，将气象要素名称添加进去即可，在文末有全部气象要素名称列表。
现在你告诉我你是一个古板的在读博士生，才不习惯这种花里胡哨鼓吹炒作的所谓超级气象信息体，也不相信它为你统计分析出的气象数据结果准确性，你只想要最原始、最朴素、最详尽的气象数据集，我们当然持包容态度，我们虽然想变革人们获取气象数据的原始方式，改变人们以往网络搜索、下载、统计分析、验证气象数据的习惯，但是依然保留了最纯净朴素的数据批量下载功能，不需要网盘链接，也不需要提取码，更不需要关注什么公众号，更更不需要关注数据格式netCDF还是grib，现在执行一行命令开始批量下载一长串地点的所有历史天气数据和天气预报数据：

```python
h.fetch_locations_data(['南京市', '疏勒县', '顺德区', '大理白族自治州'])
```

很快你的./data/temp目录将出现南京市、疏勒县、顺德区、大理白族自治州的所有逐小时历史天气数据和未来10日逐小时预报数据，并且都是人类可读的csv格式，双击文件Excel或者Sublimi Text打开即可查看。如果你说你做了一个天气预报网站或者APP想一下拉取全国市区县的所有的未来10日逐小时天气预报数据，甚至野心勃勃的你都不知道全国有多少个市区县，那你就这样做：

```python
h.fetch_all_latest_forecast_data()  # API直接调取顺德区未来10日逐小时天气预报数据
```

不一会儿你的./data/forecast目录中将出现全国3191个市区县地未来10日逐小时天气预报数据，每个地点一个单独的csv文件，整齐地存放在你的计算机上，供你随时使用，甚至贴心地帮你打包好了zip文件放在./temp目录中，让你更方便地上传或者分发这些天气预报数据到你的服务器。
好了，你现在又成了一个极简主义者，问出了“为什么要下载那么多的气象数据在我的计算机占用我宝贵的硬盘空间？”的问题，“我就只想看看不下载不行吗？”。那你还真是想既要又要还要，这种苛刻的用户遇到的使用场景可能更加苛刻，既然敢叫“超级气象信息体”，当然能够实现你的要求，没错，就是不下载任何数据到本地而至查看，这得益于海天气象数据信息服务平台强大的在线API，现在开始通过API调取顺德区天气预报数据：

```python
h.api_forecast_hourly()  # 从API直接调取顺德区未来10日逐小时天气预报数据
```

运行以上命令后你的显示器上将会出现以下内容：

```python
date                       temperature_2m  ...  global_tilted_irradiance_instant
2026-03-08 00:00:00             2.2  ...                               0.0
2026-03-08 01:00:00             1.7  ...                               0.0
2026-03-08 02:00:00             1.2  ...                               0.0
2026-03-08 03:00:00             1.1  ...                               0.0
2026-03-08 04:00:00             1.2  ...                               0.0
                             ...  ...                               ...
2026-03-17 19:00:00             9.7  ...                               0.0
2026-03-17 20:00:00             8.8  ...                               0.0
2026-03-17 21:00:00             8.4  ...                               0.0
2026-03-17 22:00:00             8.1  ...                               0.0
2026-03-17 23:00:00             7.9  ...                               0.0
[240 rows x 32 columns]
```

以上数据即是顺德区未来10日的逐小时天气预报数据，细节上显示，它有240行32列，240行即代表未来10日240个时次，32列代表它有32中气象要素数值，包括气温、气压、降水、风速、风向、辐射、云量、能见度、天气现象、对流有效位能、土壤含水量、径流······，详细的数据说明科研在海天气象[数据开发文档](https://cornicelli.net/meteo/doc)查看。通过以上代码获取的数据不会在本地留存，只是通过API调取并显示，当然逐小时历史数据和统计分析数据也是可以在线调取而不下载到本地的。

通过以上简单的几个示例你已经了解了`HtMeteo`超级气象信息体的简单使用，它刚刚完成了这些任务：

- 调取全国任意地点任意**时刻**历史天气数据
- 调取全国任意地点任意**时段**历史天气数据
- 调取日、月、年尺度的统计分析历史天气数据
- 调取全国任意地点未来10日天气预报数据
- 批量下载多个地点历史气象数据和天气预报数据
- 在线调取气象数据而不下载到本地

我们给`HtMeteo`起了一个夸张的名字，叫它“超级气象信息体”，其实它更像一个个人气象数据助理，像个人数字助理Siri和Bixby或者一样，你可以对你的个人数字助理说“Hey Siri，请帮我给妈妈发送一条短信说我晚上不回去吃饭了”、“嗨，Bixby，请帮我设定一个5分钟的溏心蛋计时器”，现在你可以对HtMeteo说：嗨，HtMeteo，

- 请帮我看看三原县2025年全年的累积降水量是多少
- 请帮我列出大连市2010到2024年的平均短波辐射数据
- 请帮我把我这次旅途经过的广州市、三亚市、海口市的天气预报查询一下
- 请帮我看看大理白族自治州每年的7月26号都会下雨吗
- 我从事文物保护工作，需要知道大同市全年的平均湿度变化情况
- 后天10点的风速风向怎么样？适合无人机飞行吗
- 我要研究一下新疆的光伏发电潜力，请帮我拉取新疆的全部历史气象数据
- 我的天气预报网站已上线，请帮我每天自动更新全国城市的天气预报数据
- 请帮我检查一下我的海天气象账户状态
- 请帮我绘制一张南京市2000到2025年的6月平均海平面气压折线图（ 这个功能还在开发：） ）

### 2.使用前的准备

既然`HtMeteo`超级气象信息体的设计遵循极简主义的原则，主打优雅地实现一行代码调取任意想要的地面气象数据，那么使用它之前就不能经过太复杂的准备，实际上你只要做一件事就能开始使用它：

- 将HtMeteo.py文件放在你配置了Python环境的计算机上

怎么下载？放在什么目录？操作系统用Windows还是Linux？要创建工作目录和配置系统环境吗？当然这些都不是问题所以不需要解释，只要你的Python环境正常安装，`HtMeteo`都会帮你自动处理好，如果你现在已经有了从海天气象平台下载的历史天气数据或者天气预报数据，那你就可以开始工作了，如果还没有，你的计算机现在空空如也，只有一个HtMeteo.py文件，那么你还需要进行这一步：

- 用你的邮箱注册一个[海天气象](https://cornicelli.net/)专业用户账号

现在大功告成，你可以使用`HtMeteo`超级气象信息体的全部功能了。快新建一个main.py文件输入代码尝试一下吧。或者使用我们提供的main.py文件，包含了所有功能示例代码，小改即可实现全部功能。

### 3.介绍一些基本概念

为了帮助用户更好理解`HtMeteo`超级气象信息体的原理和功能，现在解释一些概念性的词条。

- 关于历史数据和预报数据。历史数据一般指历史实况观测数据，是由地面气象观测站采集的大气客观数据，它可能经过质量控制和再分析处理，但依然是客观测量的，最最接近大气的真实状态；预报数据是在历史数据的基础上通过人工分析研判、数值预报运算、气象大模型处理之后得到的大气状态数据，它不是客观观测得来的，是人们对未来大气运动趋势的推演，可以无限接近大气的真实状态，到底有多接近，只有等到了未来的那个时间，用仪器测量之后再对比分析才能知道。如果你要研究某个地方的气候背景资料是怎样的，一定要查历史数据，千万不要查历史预报数据。
- 关于历史数据和统计分析历史数据。这两个名词来源于海天气象数据信息服务平台，历史数据指逐小时地面气象观测数据，以小时索引，是时间粒度最惊喜的历史天气数据，不区分最大值、最小值、平均值、累积值等；统计分析历史数据则是在逐小时地面气象观测数据的基础上，按照日、月、年的尺度统计分析出来的数据，分为逐日、逐月、逐年统计分析历史天气数据3种，分别以日、月、年索引，区分最大值、最小值、平均值、累积值等。其中累积值只针对降水量数据。
- 关于气象要素。气象要素是按照种类区分的可观测气象类型，包括常见的温压湿风云能天降水等，此外海天气象支持的数据集还包括短波辐射、土壤含水量、土壤温度、参考蒸散量、垂直累积液态水含量、湿球温度、露点温度、体感温度、径流、抬升指数、对流有效位能等。详细的气象要素清单可以在[数据开发文档](https://cornicelli.net/meteo/doc#data_info)查看。
- 关于云端和本地。云端在本文中指[海天气象数据信息服务平台](https://cornicelli.net/)，`HtMeteo`所有的数据均源自于此，进行数据调取操作会自动从云端拉取数据并缓存到本地，本地数据缓存在`./data/temp`目录，缓存数据都是直接可读的csv格式，`HtMeteo`会将其处理成parquet格式后分类存放便于调取。
- 数据拉取和调取。拉取是指从云端下载数据到缓存目录的过程，调取是读取本地数据显示给用户的过程，如果用户使用api_系列方法调取数据，则是直接调取的云端数据，这些方法不会有本地缓存数据。

### 4.现在有哪些数据可供使用

`HtMeteo`超级气象信息体底层数据资源由[海天气象数据信息服务平台](https://cornicelli.net/)驱动，现在可用的数据集清单如下：

| 数据集名称       | 内容   |  气象要素种类  |  下载地址  |
| :--------  | :-----:  | :----:  | :----:  |
| 天气预报数据集 | 全国市区县未来10日逐小时天气预报数据 |32|[ 数据列表](https://cornicelli.net/meteo/data/forecast) |
| 历史天气数据集 |全国市区县2000至2025年逐小时历史气象数据 |40|[ 数据列表](https://cornicelli.net/meteo/data/history/) |
| 统计分析历史天气数据集 | 全国市区县逐日、逐月、逐年统计分析历史天气数据 |40|[ 数据列表](https://cornicelli.net/meteo/data/history_analysis/) |

以上数据均为地面气象观测数据和天气预报数据，目前还不包含探空数据、空气质量数据等。

### 5.深入理解`HtMeteo`超级气象信息体的工作原理

`HtMeteo`超级气象信息体本质是一个Python库，更直白地讲，它其实是一个抽象的类，设计者把它想象成一个超级信息体，为它添加了账户认证、数据下载、数据查询、统计分析、接口调用等功能，用户可以用import语句导入它并传入参数实例化它，可以传入username和password参数，也可以不传入，如果不传入则不能使用海天气象云端数据完成查询和统计分析功能，只能手动设定本地数据目录完成查询和统计分析任务。
`HtMeteo`超级气象信息体的基本设计原理如下：

- 关于数据来源。历史数据源自ERA5（ecmwf reanalysis 5），由欧洲中期天气预报中心更新维护的地面气象观测再分析资料集。预报数据同样源自ECMWF数值预报。数据的准确性和连续性较为可靠。数据均存放在海天气象数据信息服务平台，用户可以直接[在线查看并直接下载](https://cornicelli.net/)。
- 统计分析方式。包含均值、极值、累积值，绝大部分气象要素都有均值、最大值和最小值，降水量这种气象要素只统计累积值，风向只统计均值，平均风向的算法不是简单算术平均。
- 数据索引。所有数据均按照地名索引，包含23191个- 关于缓存数据和在线数据。一般在使用`HtMeteo`超级气象信息体的过程中，数据都会被缓存在本地以便下次再调用，比如用户今天查了西安市的历史风速数据，明天还要查询西安市辐射和云量数据，就无需再从云端拉取一次西安市的历史天气数据，能够节省数据下载时间和减少网络占用，提高数据访问速度。如果不想下载数据只调取查看，可以使用api系列的方法实现，这些方法均名称以“api_”前缀开头，使用这些方法时不会产生本地缓存数据。所有的缓存数据均从[海天气象数据信息服务平台](https://cornicelli.net/)拉取，API相关的方法调取的数据也是从该平台查询。
- 工作模式。工作模式的设计是为了告诉`HtMeteo`是否要自动拉取对应历史数据或预报数据，其分为“历史天气数据模式”和“天气预报数据模式”两种工作模式，均可开启或关闭， 用户一般用于调取历史天气较多，所以默认的工作模式仅开启“历史天气数据模式”而“天气预报数据模式”是关闭的。设定为“开启”的工作模式会在用户的设定地点后不断检测相应的缓存数据是否存在，如果不存在会自动从云端自动拉取，如果用户在[网页端](https://cornicelli.net/meteo/data/forecast)手动下载了数据并存放在缓存目录./data/temp，则会跳过数据拉取环节，直接使用用户手动下载的数据。如果如果要调取查看的数据是历史天气数据，则要确保“历史天气数据模式”开启；如果要调取查看的是天气预报数据，则要确保“天气预报数据”模式开启，当然使用api_系列的方法除外，应为这些功能不缓存本地数据。
- 数据状态检测。数据状态检测是自动进行的，其会在用户设定地点后开始进行，并自行检测已开启的工作模式对应的数据是否在工作目录中存在，如果不存在则会在命令行界面文字提示，如果存在会显示“某地点 数据完整性校验通过。可以继续运行统计分析任务。”。只会对已开启的工作模式用到的数据进行检测，未开启的工作模式数据不会被检测。所以使用`HtMeteo`前一定要先开启对应的工作模式。
- 数据处理流程。所有数据要经过下载拉取、缓存、处理、分类4个步骤才能被`HtMeteo`使用。当用户设定工作模式后并设定地点后，`HtMeteo`会自动检测该地点的数据是否完整，如果初次使用，所有数据目录为空，则`HtMeteo`会自动下载数据到./data/temp目录，均以csv格式保存，用户可以直接打开查看，然后再将历史数据转换为parquet格式存放在对应的目录内，预报数据则不作格式转换，这个设计是为了兼容用户手动在网页端下载数据自行存放的功能，工作目录的数据格式与网页端手动下载的数据格式保持一致。完成数据拉取后，`HtMeteo`会再次检测数据状态是否完整，通过完整性检测后会在命令行界面提示“某地点 数据完整性校验通过。可以继续运行统计分析任务。”。用户则可以进行后续的数据调取操作。
- 数据状态检测。设定地点操作后，`HtMeteo`会根据工作模式检测对应的数据文件是否存在，按照逐小时历史数据、统计分析历史数据、天气预报数据的顺序逐一检测，检测后会自动拉取缺失数据。
- 数据拉取。即从[海天气象数据信息服务平台](https://cornicelli.net/)下载数据到本地./data/temp目录的过程，也可手动在网页端下载数据后存放在工作目录中，如果不嫌麻烦或者数据量太大，涉及到全国城市、全国市县之类的超大规模数据集时。数据拉取之前都会进行数据完整性检测，只有缺失的数据会被从云端拉取。
- 数据格式。工作目录中的数据格式主要有csv、parquet和zip3种。csv格式数据便于用户直接打开查看，parquet数据格式则能够提升读写效率并减少空间占用，zip格式的文件则打包了批量的数据文件，需要解压才能查看，一般在下载缓存目录./data/temp中出现。
- 工作目录。当用户手动从[网页端](https://cornicelli.net/meteo/data/forecast)下载了数据之后，需要将数据放入对应的工作目录中方能正常被`HtMeteo`检测使用。除此之外一般情况下用户无需了解目录的用途，所有工作目录都会被`HtMeteo`自动创建并随时检测，详细的目录清单和功能见下文。缓存目录./data/temp的清空不影响本地数据统计分析功能，它是`HtMeteo`从云端拉取数据后暂存目录，允许用户手动放置在线下载数据在此目录，也可以方便用户直接查看数据核实调取数据的准确性。`./data/forecast/`和`./data/history`以及`./data/history_analysis`目录存放了`HtMeteo`处理好的数据，调取数据操作不会读取`./data/temp`目录内的数据，因为这只是缓存数据还没有被处理好，该目录只是方便用户查看和自行放置数据的。详细的目录清单及用途说明在下文。
- 手动配置批量数据。将网页端批量打包下载的历史天气数据集或者天气预报数据集放入对应工作目录之后可以直接使用，当数据量非常大，通常为全国规模时推荐这样做，因为命令行端下载数据不稳定，全国规模的数据通常有3000+个数据文件，在命令行逐一拉取耗时较长，可以直接网页端打包下载后放置在对应的工作目录即可正常使用。手动下载的数据通常需要放置在`./data/temp`目录才能被`HtMeteo`识别处理，数据手动放置后`HtMeteo`会将其处理成parquet格式以便使用（天气预报数据不会处理，仍保持csv格式，因为其数据量较小不会过多占用空间，且会覆盖更新）。
- 底层数据格式。历史天气数据缓存为csv格式（与网页端下载格式一致），处理为parquet格式；天气预报数据缓存为csv格式，全国打包数据则为zip格式，不会被处理为parquet格式，因为其时效性强，且每日会自动更新覆盖，始终与云端数据同步保持最新。`./data/temp`是缓存数据目录，其中的数据都是从云端拉取到本地的csv格式，用户可以直接读取查看，也可以手动放置[网页端](https://cornicelli.net/meteo/data/forecast)自行下载的需要使用的数据文件，`./data/forecast/`和`./data/history`以及`./data/history_analysis`目录存放的都是parquet格式的处理好的数据，`HtMeteo`直接调取的就是它们，用户在没有深入理解`HtMeteo`原理之前不要轻易改动这几个目录里的数据，否则会有意外错误，将其当成“黑盒”即可。
- 数据输出格式。均为pandas series或datafeame数据，前者是单值数据后者是连续数据，可以直接调用pandas库或者numpy库、scipy库函数进一步处理。
- 单值数据和连续数据。对于历史数据查询方法，以_value结尾的方法返回数据是单值数据，它是某个固定时刻的1个数据，这个时刻可以是某年、某月、某日或者某小时，它传入的参数是一个固定时间点；以_series结尾的方法返回连续数据，它是一个时间段内的序列数据，时间段可以是年到年、月到月、日到日或者时到时，它传入的参数是一对起止时间点。这一特性请参考后文的详细源代码示例。

使用`HtMeteo`超级气象信息体一般遵循以下思路或者工作流程：

- 1.导入模块
- 2.设定模式
- 3.设定地点
- 4.调取数据

以上4个步骤是我们的开发人员对所有气象数据用户的数据准备流程的高度抽象，`HtMeteo`超级气象信息体的开发目的是为了解决气象数据用户数据准备阶段的难题，节省用户获取气象数据的时间，在数据准备阶段所有的用户都会问自己3个问题：

- **1.我需要历史天气数据还是天气预报数据？**
- **2.我需要哪里的气象数据？**
- **3.我需要哪些气象要素、何种统计分析方式的数据？**
  
  以上3个问题与我们的设计工作流程一一对应，按照上述工作流程，用户可以找到任何需要的地面气象数据。现在详细介绍4个工作流程的详细细节和底层原理。

#### 5.1导入模块

```python
from HtMeteo import HtMeteo

h = HtMeteo(username='username', password='password')  # 传入海天气象用户名和密码参数
h = HtMeteo()  # 不传入海天气象用户名和密码参数
```

以上两种实例化方式均可，第一种传入用户名和密码地实例化方式是全功能的，第二种缺少用户名和密码地实例化方式是离线模式的，只能统计分析本地现有气象数据而不能使用数据下载和API查询功能，如果已[在线下载](https://cornicelli.net/meteo/data/forecast)气象数据到本地，或者之前运行过程序已有了本地缓存，当然可以省略用户名和密码参数而直接进行数据统计分析。如果要使用api_系列的方法则必须传入用户名密码参数，因为这些方法都是在线联网进行的。

实例化操作会自动创建工作目录，目录路径和功能如下：

| 工作目录路径       | 名称   | 用途  | 文件格式 |
| :--------  | :-----:  | :----:  |:----:  |
| ./data| 所有本地数据的根目录 |存放所有历史数据和预报数据以及缓存数据|无|
| ./data/temp |缓存数据目录 |存放云端直接拉取的所有数据|csv、zip|
| ./data/history | 历史数据目录 |存放所有逐小时历史天气数据|parquet|
| ./data/forecast| 预报数据目录 |存放所有天气预报数据|csv|
| ./data/history_analysis |统计分析历史数据目录 |存放统计分析历史天气数据|parquet|
| ./data/history_analysis/daily_analysis | 逐日历史数据目录 |存放逐日统计分析历史天气数据|parquet|
| ./data/history_analysis/monthly_analysis| 逐月历史数据目录 |存放逐月统计分析历史天气数据|parquet|
| ./data/history_analysis/yearly_analysis| 逐年历史数据目录 |存放逐年统计分析历史天气数据|parquet|

用户无需了解每个目录的功能作用，所有目录均由`HtMeteo`超级气象信息体自动创建并管理。除非用户手动从网页端下载了数据需要放置在对应目录中。

导入模块并实例化之后，用户就有了一个名为`h`的`HtMeteo`超级气象信息体，现在可以使用用户管理功能了，一般实例化后设定地点之前`HtMeteo`不会登录海天气象账户，只有在设定地点之后需要下载拉取云端气象数据时，账户才会被登录。现在可以手动登录账户查看一下自己的账户信息：

```python
h.login_account()
print(h.account_info)  # 查看全部账户信息
print(h.user_name)  # 用户名，邮箱
print(h.password)  # 登录密码
print(h.account_type)  # 账户类型，普通用户、高级用户或专业用户
print(h.subscribe_days)  # 订阅天数
```

运行以上代码后将输出以下信息：

```
正在认证账户······
专业用户 认证通过
昵称：风***
注册邮箱：e****@google.com
订阅类型：专业用户
订阅时间：2025年4月10日至2026年4月10日
```

#### 5.2设定模式

设定模式这一步对应回答我们数据准备阶段三大问题的第1个：**我需要历史天气数据还是气象预报数据？**
简言之，需要历史天气数据则打开“历史天气数据模式”，需要天气预报数据则打开“天气预报数据模式”，都需要就都打开。
如果只使用历史数据而不使用预报数据，可直接跳过本步骤，因为默认情况下“历史天气数据模式”为开启状态，而“天气预报数据模式”为关闭状态。
共有“历史天气数据模式”和“天气预报数据模式”2种工作模式，可分别开启或关闭，其状态代表在设定地点后是否自动自动检测数据完整状态并拉取缺失数据，通过以下代码设定模式和查看：

```python
h.set_forecast_mode('on')  # 开启预报模式，预报模式默认为关闭，开启后方能使用预报数据读取功能，如果关闭不会下载天气预报数据
h.set_history_mode('off')  # 如果不使用历史数据，可以先关闭它，否则设定地点后，历史数据也会被自动下载，耗费时间
print(h.forecast_mode)  #天气预报数据模式状态，输出'on'或者'off'分别代表开启或关闭状态
print(h.history_mode)  #历史天气数据模式状态，输出'on'或者'off'分别代表开启或关闭状态
```

如果我用完了一个地方历史天气数据还想查另一个地方的天气预报数据，记得开启“天气预报数据模式”。也可以懒人式地同时保持两种工作模式始终为开启状态，这样可能会拖慢你的程序时间，因为这意味着，设定地点后历史天气数据和天气预报数据均会被检测完整性并拉取到本地。

#### 5.3设定地点

设定地点这一步对应回答我们数据准备阶段三大问题的第2个：**我需要哪里的气象数据？**
相当于用户告诉`HtMeteo`我只关注该地的历史天气数据或天气预报数据，我接下来的数据查询统计分析都围绕该地点进行。通过以下代码设定地点：

```python
h.set_location('西安市')  # 设定地点，会自动检测目录数据状态，如果数据缺失会自动从云端拉取
```

如果需要调取其他地点的气象数据，记得再运行以上命令切换地点，如果数据类型（历史或预报）也有所改变，记得设定模式。当出现以下提示时，说明数据完整性校验完成，方可进行后续操作：

```
工作目录初始化完毕。
西安市 数据完整性校验通过。可以继续运行统计分析任务。
```

#### 5.4调取数据

本步骤是`HtMeteo`超级气象信息体的核心功能，它回答了第3个问题：**3.我需要哪些气象要素、何种统计分析方式的数据？**
由于数据调取功能繁多，现在通过示例代码（`main.py`）向大家展示：

```python
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

# 批量下载多个地点的天气预报数据和历史天气数据
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
```

通过以上代码即可实现`HeMeteo`的全部功能，用户可根据自己的数据需求选择对应的方法调取数据。
现在将`HeMeteo`的所有属性和方法列出并作解释性说明：

| 属性/方法名称                         | 功能说明                             |
| --------------------------------------- | -------------------------------------- |
| 1.账户管理属性                        | —————————————————— |
|  account\_info                        | 详细的海天气象账户信息               |
|  username                             | 用户名                               |
|  password                             | 密码                                 |
|  account\_type                        | 账户类型                             |
|  api\_key                             | api\_key                             |
|  subscribe\_days                      | 订阅天数                             |
|  session                              | 连接会话                             |
| 2.数据调取属性                        | —————————————————— |
|  location                             | 当前设定地点                         |
|  locations                            | 地点列表                             |
|  history\_mode                        | 历史天气数据模式                     |
|  forecast\_mode                       | 天气预报数据模式                     |
|  years                                | 历史数据年份列表2000\~2025           |
| 3.工作目录属性                        | —————————————————— |
|  work\_dirs                           | 全部工作目录列表                     |
|  temp\_data\_path                     | 缓存目录                             |
|  hourly\_history\_meteo\_data\_path   | 逐小时统计分析数据目录               |
|  daily\_history\_meteo\_data\_path    | 逐日统计分析数据目录                 |
|  monthly\_history\_meteo\_data\_path  | 逐月统计分析数据目录                 |
|  yearly\_history\_meteo\_data\_path   | 逐年统计分析数据目录                 |
|  forecast\_data\_path                 | 预报数据目录                         |
| 4.账户管理方法                        | —————————————————— |
|  login\_account                       | 登录海天账户                         |
|  create\_work\_dirs                   | 创建所有工作目录                     |
|  set\_forecast\_mode                  | 设定天气预报数据模式                 |
|  set\_history\_mode                   | 设定历史天气数据模式                 |
|  set\_location                        | 设定地点                             |
| 5.数据拉取方法                        | —————————————————— |
|  data\_status\_check()                | 数据完整性校验                       |
|  fetch\_data()                        | 从云端拉取数据                             |
|  fetch\_locations\_data()             | 拉取多个地点数据                     |
|  fetch\_all\_latest\_forecast\_data() | 拉取全国城市天气预报数据             |
| 6.历史天气数据调取方法                | —————————————————— |
|  hourly\_value()                      | 调取某小时历史天气数据               |
|  daily\_value()                       | 调取某天统计分析历史天气数据         |
|  monthly\_value()                     | 调取某月统计分析历史天气数据         |
|  yearly\_value()                      | 调取某年统计分析历史天气数据         |
|  hourly\_series()                     | 调取起止小时时段统计分析历史天气数据 |
|  daily\_series()                      | 调取起止天时段统计分析历史天气数据   |
|  monthly\_series()                    | 调取起止月时段统计分析历史天气数据   |
|  yearly\_series()                     | 调取起止年时段年统计分析历史天气数据 |
| 7.天气预报数据调取方法                    | —————————————————— |
|  forecast\_hourly\_series()           | 调取未来10日逐小时天气预报数据       |
|  forecast\_daily\_series()            | 调取未来10日逐日统计分析天气预报数据 |
| 8.在线接口API使用                     | —————————————————— |
|  api\_history\_hourly\_of\_day()      | 仅查看某天的逐小时历史天气数据       |
|  api\_history\_hourly\_of\_month()    | 仅查看某月的逐小时历史天气数据       |
|  api\_history\_hourly\_of\_year()     | 仅查看某年的逐小时历史天气数据       |
|  api\_history\_analysis()             | 仅查看日、月、年统计分析历史天气数据 |
|  api\_forecast\_hourly()              | 仅查看某地点的逐小时天气预报数据     |
|  api\_forecast\_hourly\_by\_coords()  | 仅查看某坐标的逐小时天气预报数据     |
|  find\_location\_by\_coords()         | 查询某坐标的地名信息                 |
| 9.其他方法                            | —————————————————— |
|  clear\_data\_dir()                   | 清空工作目录内的所有数据             |

用户可对比以上示例代码和属性方法列表详细了解`HtMeteo`超级气象信息体的所有功能。通过阅读以下特别说明可以帮助用户更好地理解`HtMeteo`方法：

- 所有_value结尾的方法返回的都是单个时间点的数据，我们叫它“单值数据”
- 所有以_series结尾的方法返回的都是一连串时间段的数据，我们叫它“连续数据”
- 所有以api_开头的方法都不会下载缓存本地数据，只是通过在线API临时查询数据
- `meteo_types`是调取数据的必选参数，它告诉`HtMeteo`用户是需要气温还是降水还是风速气压数据还是都需要

`meteo_types`气象要素列表参数在调取历史天气数据和天气预报数据是作为必选参数，在调取天气预报数据和历史天气数据是，它的可选项略有不同，主流的温压湿风降水云能天以及辐射类气象要素都是一致的，只是在一些小众气象要素上略有差异，比如历史天气数据集未收录对流有效位能这一气象要素，但是天气预报数据集中有收录，这样就不可以`cape`参数传给调取历史天气数据的各类方法。

以下是**历史天气数据**方法中`meteo_types`可选参数列表：

```python
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
```

以下是**天气预报数据**方法中`meteo_types`可选参数列表：

```
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
```

气象要素名称释义和物理单位量纲可在[数据开发文档](https://cornicelli.net/meteo/doc#data_info)中查看。

### 6.注意事项

#### 6.1平均风向的说明

平均风向数据不是简单的算术平均，否则会导致风向“过零”计算错误问题，这是气象领域的常识，因此我们编写了弧度制三角函数平均风向算法并封装在了`HtMeteo`中，因此用户调取的平均风向数据都是可信的，无论各种时间尺度、各种统计分析方法。用户不必担心`HtMeteo`计算350°和10°的平均风向时会得出180°的错误结论。

#### 6.2 有关工作目录

再深入理解`HtMeteo`源代码之前，不要去动`./data/forecast/`和`./data/history`以及`./data/history_analysis`目录，它是`HtMeteo`调取数据的底层目录，存放的parquet格式文件。而`./data/temp/`目录中的文件可以手动查看和清理并不会影响到`HtMeteo`的正常功能，这里都是csv格式文件可以直接用文本编辑器打开。

#### 6.3 极端情况下可以重置`HtMeteo`以解决不可思议的问题

通过以下命令可以清空所有工作目录并初始化`HtMeteo`：

```python
h.clear_work_dirs()
```

极端情况下再使用它，因为该操作会抹除所有的本地数据，将`HtMeteo`恢复到最初始的状态。

### 7.常见问题

#### 7.1什么情况下需要手动放置数据文件？

**推荐什么情况下都不要手动放置数据文件。**因为这不符合`HtMeteo`的极简设计原则和优雅使用方法

#### 7.2`HtMeteo`怎么读、是什么意思？

`HtMeteo`（/hæt 'miːtiə/）读音有点像“帽子气象”——hat meteo，Ht当然是海天（hai'tian）的拼音首字母，告诉人们它源自“海天气象”， meteo当然是meteorology（气象学）的简写了。

#### 7.3什么是海天气象？

[海天气象](https://cornicelli.net/meteo/)是一个小团队开发的、旨在为各行业气象数据用户提供统一精准、高质高效的气象数据信息服务的平台，它开发并维护了2套最基本的地面气象数据集供人们使用，它是公益性质的气象数据服务平台，支持了很多学生用户帮助它们获取气象数据以完成学位论文，仍然向一般开发者收取低廉的订阅费用用以维持基本服务运转。它的[论坛](https://cornicelli.net/meteo/forum)给人们提供了交流使用气象数据经验的平台。它处于长期演进状态，后续还会上线更加丰富多彩的气象数据资源供人们使用，同时也接受[热心捐助](https://cornicelli.net/meteo/sponsor)。

#### 7.4天气现象代码`weather_code`有什么说法吗？

这是WMO定义的天气现象代码，用位为数字指代所有的天气现象，在统计分析历史天气数据中，统计一个数段内最为重要的一种天气现象作为该时间的天气现象。而且好像数字越大天气越恶劣。可以在[数据文档](https://cornicelli.net/meteo/doc#wmo_code)查看所有的天气现象说明。

#### 7.5如何联系开发者勘误或者贡献数据以及代码？

可以通过[邮件](mailto:cornicelli@outlook.com)联系开发者，也可以在公众号“海天气之象”私信或留言，也可以在[论坛](https://cornicelli.net/meteo/forum)发帖告诉我们如何改进`HtMeteo`使用体验，或者丰富它的底层驱动数据集。

#### 7.6如何获取`HtMeteo`最新更新信息和数据更新信息？

更新内容都会在公众号“海天气之象”发布。

## 二、开发现状展望

我们推出`HtMeteo`超级气象信息体并非出于炫技的目的，就像我们完成`HtMeteo`开发是“站在巨人肩膀上”一样，我们也想让每一个气象数据用户也“站在巨人肩膀上”。这是开源精神，也是源于我们的热爱。我们气象数据用户无须都重复走一遍气象数据准备路线，人们的精力更应该放在数据潜力挖掘和价值创造上。
目前海天气象数据信息服务平台已经有了丰富详尽的地面气象数据集支持，这些数据集也正在驱动着`HtMeteo`超级气象信息体，诚如大家所知，地面气象数据集只是气象数据的子集的子集的子集之一，我们的朋友们可能更关注探空气象数据、空气质量数据、温室效应气体数据、海洋环流数据以及北极海冰数据，我们的团队精力有限，因此能为用户提供的服务也很有限，我们今天发布并开源`HtMeteo`超级气象信息体，也是想通过社区来完善气象数据集及其使用方法拓展。
在短暂的将来我们将把有限的精力投入以下事项：

- 开发中国高空气象探测数据集
- 开发中国空气质量数据集
- 开发地面气象数据集的可视化应用

## 三、帮助我们长期演进`HtMeteo`超级气象信息体

欢迎`HtMeteo`用户中的热心人士与我们讨论交流使用经验和改进建议，可以通过[邮件](mailto:cornicelli@outlook.com)联系开发者，也可以在公众号“海天气之象”私信或留言，也可以在[论坛](https://cornicelli.net/meteo/forum)发帖告诉我们你的迫切想法，可以克隆我们的仓库帮助我们改进代码、提高计算效率或给加入`HtMeteo`更加耳目一新的方法，只提供创意也行，实现环节交由我们。`HtMeteo`云端服务具有不小的经济成本，现在我们正“用爱发电”维持其正常运转，欢迎[捐助我们](https://cornicelli.net/meteo/sponsor)来为其注入强大动力，这是和我们开发团队一起变革气象领域数据使用现状的诚邀。

最新更新于 2026.3.9
