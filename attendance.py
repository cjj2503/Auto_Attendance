from dgut.dgut_xgxtt import dgut_xgxtt
import time
import sys
import datetime
import json

def get_schedule(filename='./schedule.json'):
    '''
    获取今天的考勤时间表
    返回一个考勤时间列表[[start1, end1], [start2, end2]]
    '''
    try:
        fp = open(filename, 'r')
        schedule = json.loads(fp.read())
        
        # 获取今天的时间表
        now = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
        week = now.strftime("%w")
        
        schedule_today = schedule[week]
        schedule_today.sort(key=lambda elem: int(elem[0].split(':')[0]))
        return schedule_today

    except FileNotFoundError:
        print(f'没找到文件{filename}')


def sign(username, password, flag):
    '''
    考勤签到/签退
    '''
    mydgut = dgut_xgxtt(username, password)

    # 签到/签退
    response = mydgut.attendance(flag=flag)

    # 如果错误码3开头，进行重新请求三次
    if str(response['code'])[0] == '3':
        for i in range(3):
            time.sleep(5)
            response = mydgut.attendance(flag=flag)
            if response['code'] == 1:
                break
    return response


if __name__ == '__main__':

    # 验证账号密码和登录时间
    try:
        username = sys.argv[1]
        password = sys.argv[2]

        schedule = get_schedule(filename='./schedule.json')
        print(schedule)
        for atten in schedule:
            start = atten[0].split(":")
            end = atten[1].split(":")
            print("-"*20)
            print(f"{start[0]}:{start[1]}-{end[0]}:{end[1]}……")
            now = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
            if now.hour > int(start[0]) or (now.hour == int(start[0]) and now.minute > int(start[1])):
                continue
            
            while True:
                if now.hour == int(start[0]) and now.minute == int(start[1]):
                    break
                now = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
            # 签到
            response1 = sign(username, password, 1)
            print(response1)
            if response1['code'] != 1:
                print("启动自动考勤失败！")
                exit()
            now = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
            while True:
                if now.hour == int(end[0]) and now.minute == int(end[1]):
                    break
                now = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
            # 签退
            response2 = sign(username, password, 2)
            print(response2)
            if response2['code'] != 1:
                print("签到成功了但签退失败！")
                exit()

    except IndexError:
        print("请完整输入账号和密码")
    
    except:
        print("未知的错误")

    
    
