### django的logging模块

```python
LOGGING = {
    'version': 1,#指明dictConnfig的版本，目前就只有一个版本，哈哈
    'disable_existing_loggers': True,#禁用所有的已经存在的日志配置
    'formatters': {#格式器
        'verbose': {#详细
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {#简单
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {#过滤器  过滤器可以放在logger, handlers 里  一般不会使用过滤器
        'special': {#使用project.logging.SpecialFilter，别名special，可以接受其他的参数
            '()': 'project.logging.SpecialFilter',
            'foo': 'bar',#参数，名为foo，值为bar
        }
    },
    'handlers': {#处理器，在这里定义了三个处理器
        'null': {#Null处理器，所有高于（包括）debug的消息会被传到/dev/null
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{#流处理器，所有的高于（包括）debug的消息会被传到stderr，使用的是simple格式器
            'level':'DEBUG',
            'class':'logging.StreamHandler',  # 会在控制台输出  
            
            #'class': logging.handlers.TimedRotatingFileHandler'  #在文件中输出
            #'filename': 'log/webservice.log',  #文件路径
            #'when': 'D', # 每天一个新文件
            
            'formatter': 'simple'
        },
        'mail_admins': {#AdminEmail处理器，所有高于（包括）而error的消息会被发送给站点管理员，使用的是special格式器
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['special']
        }
    },
    'loggers': {#定义了三个记录器
        'django': {#使用null处理器，所有高于（包括）info的消息会被发往null处理器，向父层次传递信息
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {#所有高于（包括）error的消息会被发往mail_admins处理器，消息不向父层次发送
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'myproject.custom': {#所有高于（包括）info的消息同时会被发往console和mail_admins处理器，使用special过滤器
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'filters': ['special']
        }
    }
}
```

第一步 机器把信息发送给loggers    

第二步  loggers把自己过滤后的信息发给handles, 

第三步  handles对得到的信息进行处理,  流输出, 或者写入文件,或者发送邮件等等

在logger中会选择配置多个handles

在handles中会选择formatters (输出格式)

filter(过滤器)可以放在logger中 也可以放在handles中  一般不会使用过滤器

formatters(输出格式) 可以自己控制输出的信息  下图是一些格式

![](/home/mrg/图片/2018-05-15 20-46-16屏幕截图.png)

### django信号

- 自定义信号

  1定义信号

```python
from django.dispatch import Signal
action=Signal(providing_args=["aaaa","bbbb"])
```

​	2注册信号

```python
# 自定义处理函数
def signal_call_back(sender,**kwargs):
	print(sender,kwargs)
# 注册信号处理函数
action.connect(signal_call_back)
```

​	3发送信号

```python
action.send('province_page',para1='para11',para2='para22')
```

