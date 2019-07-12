# AHNUReserve
> 使用Python爬虫完成图书馆自动预约座位（安徽师范大学敬文图书馆）

### 代码中需要自定义的地方
```Python
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

将以上内容根据自己的需要更改后，即可进行服务器部署。

### 服务器部署
服务器环境
* Ubuntu16.04
* Python3.5
需要的Python包（一般应该都有安装）
* requests
* json
* smtplib
* time
* email
* logging
部署步骤
