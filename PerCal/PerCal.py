# coding=utf8
'''

@author: 极端降水算法二：作物生育期内指定时间段，指定降雨阈值的累计天数及累计雨量

'''
from cma.music.DataQueryClient import DataQueryClient
import argparse

def GetText(Station, TimeRange):
    # 1. 定义client对象
    client = DataQueryClient()

    # 2. 调用方法的参数定义，并赋值
    # 2.1 用户名&密码
    userId = "BENC_QKS_NYQX"
    pwd = "Liudan@19890617"

    # 2.2  接口ID
    interfaceId = "getSurfEleByTimeRangeAndStaID"

    # 2.3  接口参数，多个参数间无顺序
    params = {'dataCode': "SURF_CHN_MUL_DAY", \
              'elements': "Year,Mon,Day,PRE_Time_2020", \
              'STAIDS': Station, \
              'TIMERANGE': TimeRange
              }

    # 2.4 返回文件的格式
    dataFormat = "text"

    # 2.5 文件的本地全路径
    savePath = "./tmp_rain.text"

    # 3. 调用接口
    result = client.callAPI_to_saveAsFile(userId, pwd, interfaceId, params, dataFormat, savePath)

    # 4. 输出接口
    print(result.request)
    print(result.fileInfos)


def TXTToRainList(FileDir, rain_threshold=10):
    """
    极端降水算法：降雨天数及累计雨量
    """
    encoding = 'utf-8'
    TmpJs = 0
    rain_days = 0
    cumulative_rainfall = 0
    
    with open(FileDir, "r", encoding=encoding) as f:
        Datas = f.readlines()
        for Line in Datas:
            TmpJs += 1
            if TmpJs > 2:  # 跳过表头
                TmpStr = Line.split()
                if len(TmpStr) >= 4:  # 确保有降水数据
                    try:
                        rain = float(TmpStr[-1])
                        if rain != 999999 and rain >= 0:  # 排除无效值
                            if rain > rain_threshold:
                                rain_days += 1
                            cumulative_rainfall += rain
                    except ValueError:
                        continue
    
    return rain_days, cumulative_rainfall


if __name__ == "__main__":
    # 创建Arg对象
    Parser = argparse.ArgumentParser(description='极端降水算法')
    
    # 添加命令行参数
    Parser.add_argument('par1', help='Station')
    Parser.add_argument('par2', help='TimeRange')
    Parser.add_argument('--threshold', type=float, default=10, help='降雨阈值(mm)')
    
    # 解析命令行参数
    Args = Parser.parse_args()
    
    # 获取参数值
    Station = Args.par1
    TimeRange = Args.par2
    rain_threshold = Args.threshold

    # 重新赋值一个方便调试
    # Station = 'J1167'
    # TimeRange = '[20230801000000,20250731000000]'
    # rain_threshold = 10

    GetText(Station, TimeRange)

    # 读取tmp.txt
    rain_days, cumulative_rainfall = TXTToRainList(FileDir='./tmp_rain.text', rain_threshold=rain_threshold)
    
print("降雨阈值: {}mm".format(rain_threshold))
print("强降雨天数: {} 天".format(rain_days))
print("累计雨量: {:.2f} mm".format(cumulative_rainfall))