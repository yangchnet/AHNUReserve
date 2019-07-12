import requests
import json
import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formataddr
import logging
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s- %(message)s')


def reserve(account, password, sid, rtime):
    atDate = rtime
    st = rtime + ' 08:10'
    et = rtime + ' 22:00'
    with requests.Session() as s:
        try:
            logging.info('''
            start  with account:{0}, password:{1}, seatid:{2}. From {3} to {4}.'''
                         .format(account, password, sid, st, et))

            # 开始登陆
            postUrl = 'http://libzwxt.ahnu.edu.cn/SeatWx/login.aspx'
            postData = {
                '__VIEWSTATE': '/wEPDwULLTE0MTcxNzMyMjZkZJoL/NVYL0T+r5y3cXpfEFEzXz+dxNVtb7TlDKf8jIxz',
                '__VIEWSTATEGENERATOR': 'F2D227C8',
                '__EVENTVALIDATION': '/wEWBQKV1czoDALyj/OQAgKXtYSMCgKM54rGBgKj48j5D1AZa5C6Zak6btNjhoHWy1AzD9qoyayyu5qGeLnFyXKG',
                'tbUserName': account,
                'tbPassWord': password,
                'Button1': '登 录',
                'hfurl': ''
            }

            login = s.post(postUrl, data=postData)

            if '个人中心' in login.content.decode():
                logging.info('login successfully!')

            # 开始预约
            logging.info('begin to reserve...')
            header = {
                'Host': 'libzwxt.ahnu.edu.cn',
                'Origin': 'http://libzwxt.ahnu.edu.cn',
                'Referer': 'http://libzwxt.ahnu.edu.cn/SeatWx/Seat.aspx?fid=3&sid=1438',
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                'X-AjaxPro-Method': 'AddOrder',
            }
            reserveUrl = 'http://libzwxt.ahnu.edu.cn/SeatWx/ajaxpro/SeatManage.Seat,SeatManage.ashx'
            reserverData = {
                'atDate': atDate,
                'sid': sid,
                'st': st,
                'et': et,
            }
            reserve = s.post(reserveUrl, data=json.dumps(reserverData), headers=header)
            logging.info(reserve.text)
            return reserve.text
        except BaseException as e:
            logging.error(e)


def send_mail(my_sender, my_pass, to_user, my_nick, to_nick, mail_msg):
    msg = MIMEText(mail_msg, 'html', 'utf-8')
    msg['Form'] = formataddr([my_nick, my_sender])
    msg['To'] = formataddr([to_nick, to_user])
    msg['Subject'] = '图书馆座位预约'
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(my_sender, my_pass)
    server.sendmail(my_sender, [to_user, ], msg.as_string())
    server.quit()


if __name__ == "__main__":
    # 账号
    account = '16111206015'
    # 密码
    password = '16111206015'
    # 座位编号（要从网页端报文查看）
    sid = '258'
    # 邮件接收者
    to_user = '**********'
    # 邮件发送者
    my_sender = '*******'
    # 邮箱密码
    my_pass = '*********'
    # 配置发件人昵称
    my_nick = '*********'
    # 配置收件人昵称
    to_nick = '**********'

    today = time.strftime("%Y-%m-%d", time.localtime())
    tomorrow = today[:-2] + (str(int(today[-2:]) + 1)).zfill(2)

    try:
        # 尝试预约
        rtext = reserve(account, password, sid, tomorrow)
        while '预约成功' not in rtext:
            # 若位置已被占据或其他原因未完成预约，则尝试重新预约下一个座位
            logging.info('Appointment failed, trying to reserve another seat...')
            sid = str(int(sid)+1)
            rtext = reserve(account, password, sid, tomorrow)
        logging.info('reserve successfully! Your seat id is {0}'.format(sid))

        # 开始发送电子邮件
        mail_msg = '''
        <p>尊敬的主人：<p>
        <p>您明天的座位已经预约完成，请您及时登录自己的账户查看哦！<p>
        <p>为您约到的座位id为{0}<p>
        '''.format(sid)
        send_mail(my_sender, my_pass, to_user, my_nick, to_nick, mail_msg)
        logging.info('The email has been sent to {0}'.format(to_user))
    except BaseException as e:
        logging.error(e)





