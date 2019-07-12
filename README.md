# AHNUReserve
> 使用Python爬虫完成图书馆自动预约座位（安徽师范大学敬文图书馆）

[![Build status](https://ci.appveyor.com/api/projects/status/69iwhe2g11t30sj8/branch/master?svg=true)](https://ci.appveyor.com/project/HTBox/allready/branch/master)

### 服务器部署
服务器环境
* Ubuntu16.04
* Python3.5
需要的Python包（一般应该都有安装, 可用```pip list```进行查看）  
* requests
* json
* smtplib
* time
* email
* logging

部署步骤  
1. 首先使用```git clone https://github.com/yangchnet/AHNUReserve.git```把代码clone到你的服务器上
    ![clone](https://github.com/yangchnet/AHNUReserve/blob/master/img/clone.png?raw=true)

2. 修改参数（账号密码等, 邮箱授权码的获取请看[这里](#邮箱授权码的获取)）  
    ```Python
    # 73行附近
    # 账号
    account = '*******'
    # 密码
    password = '******'
    # 座位编号（要从网页端报文查看）
    sid = '******'
    # 邮件接收者
    to_user = '**********'
    # 邮件发送者
    my_sender = '*******'
    # 邮箱密码(这里是设置授权码，并不是真正的密码)
    my_pass = '*********'
    # 配置发件人昵称
    my_nick = '*********'
    # 配置收件人昵称
    to_nick = '**********'
    ```
3. 修改日志位置  
    ```Python
    logging.basicConfig(filename='***.log', level=logging.INFO, format=' %(asctime)s - %(levelname)s- %(message)s')
    ```
    将这里filename后的值改成你想要日志保存的位置，**注意需要使用绝对路径**。  
3. 使用crontab进行定时运行  
    使用```crontab -l```命令查看当前用户的定时任务  
    使用```crontab -e```命令编辑文件来新建任务  
    其格式为```minute (m), hour (h), day of month (dom), month (mon),and day of week (dow)， commond```, 使用```*```表示任意值
    例如，如果你想在每周的第一天的早上5点完成某个任务，你可以使用    
    ```bash
    0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
    ```
    这里我们设置为每天的凌晨00：01来进行预约座位，则设置为  
    ```
    1 0 * * * python3 /home/***/Reserve.py
    ```
    设置完成后，再次用```crontab -l```命令查看是否设置成功  
    
### 邮箱授权码的获取    
1. 登录自己的QQ邮箱  

2. 点击邮箱中的【设置】，进入【帐户】栏，下拉你会看见如下的截图  
    ![smtp](https://github.com/yangchnet/AHNUReserve/blob/master/img/smtp.png?raw=true)
    
3. 点击POP3/SMTP服务后的开启（我这里已经是开启了），根据下图的提示，发送短信，获取授权码（设置为my_pass参数的值）  
    ![send message](https://github.com/yangchnet/AHNUReserve/blob/master/img/message.png?raw=true)
    
**有用请点星，欢迎fork**
