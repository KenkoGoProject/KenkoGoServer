DEFAULT_MIDDLEWARE = {  # 默认中间件
    'access-token': '',  # 访问密钥 api token
    'filter': '',  # 事件过滤器文件目录，留空接收所有消息
    'rate-limit': {  # API限速设置，参考https://baike.baidu.com/item/%E4%BB%A4%E7%89%8C%E6%A1%B6%E7%AE%97%E6%B3%95/6597000?fr=aladdin
        'enabled': False,  # 是否启用限速
        'frequency': 1,  # 令牌回复频率, 单位秒
        'bucket': 1,  # 令牌桶大小
    },
}


DEFAULT_GOCQ_CONFIG = {
    'account': {
        'uin': 0,  # QQ号，保留 0，使用二维码登录
        'password': '',  # 密码，保留空，使用二维码登录
        'encrypt': False,  # 加密密码，保留 False
        'status': 0,  # 在线状态
        'relogin': {  # 重连设置
            'delay': 3,  # 首次重连延迟, 单位秒
            'interval': 3,  # 重连间隔
            'max-times': 0,  # 最大重连次数, 0为无限制
        },
        'use-sso-address': True,  # 是否使用服务器下发的新地址进行重连。注意, 此设置可能导致在海外服务器上连接情况更差
        'allow-temp-session': True,  # 是否允许临时会话
    },  # 账号配置
    'heartbeat': {
        'interval': 5,  # -1 为关闭心跳
    },    # 心跳频率, 单位秒
    'message': {
        'post-format': 'string',  # 上报数据类型，可选: string,array
        'ignore-invalid-cqcode': False,  # 是否忽略无效的CQ码, 如果为假将原样发送
        'force-fragment': False,  # 是否强制分片发送消息，分片发送将会带来更快的速度，但是兼容性会有些问题
        'fix-url': False,  # 是否将url分片发送
        'proxy-rewrite': '',  # 下载图片等请求网络代理
        'report-self-message': True,  # 是否上报自身消息
        'remove-reply-at': False,  # 移除服务端的Reply附带的At
        'extra-reply-data': False,  # 为Reply附加更多信息
        'skip-mime-scan': False,  # 跳过 Mime 扫描, 忽略错误数据
    },
    'output': {
        'log-level': 'error',  # 默认为warn, 支持 trace,debug,info,warn,error
        'log-aging': 30,  # 日志时效 单位天. 超过这个时间之前的日志将会被自动删除. 设置为 0 表示永久保留.
        'log-force-new': False,  # 是否在每次启动时强制创建全新的文件储存日志. 为 false 的情况下将会在上次启动时创建的日志文件续写
        'log-colorful': True,  # 是否使用彩色日志输出
        'debug': False,  # 开启调试模式
    },
    'default-middlewares': DEFAULT_MIDDLEWARE,  # 默认中间件锚点
    'database': {  # 数据库相关设置
        'leveldb': {  # 是否启用内置leveldb数据库
            'enable': True,  # 启用将会增加10-20MB的内存占用和一定的磁盘空间，关闭将无法使用 撤回 回复 get_msg 等上下文相关功能
        },
        'cache': {  # 媒体文件缓存， 删除此项则使用缓存文件(旧版行为)
            'image': 'data/image.db',
            'video': 'data/video.db',
        }
    },
    'servers': [  # 前两个为 KenkoGo 必须项，若需要其他配置，请在尾部添加
        {
            'http': {
                'address': '127.0.0.1:35700',  # 必须打开，KenkoGo暂时使用此方案
                'timeout': 5,  # 反向 HTTP 超时时间, 单位秒，<5 时将被忽略
                'long-polling': {  # 长轮询拓展
                    'enabled': False,  # 是否开启
                    'max-queue-size': 2000,  # 消息队列大小，0 表示不限制队列大小，谨慎使用
                },
                'middlewares': DEFAULT_MIDDLEWARE,
            }
        },
        {
            'ws-reverse': {  # 反向 WebSocket（作为客户端）
                'universal': 'ws://127.0.0.1:18082/instance',  # 必须打开，KenkoGo暂时使用此方案
                'reconnect-interval': 3000,  # 重连间隔, 单位毫秒
                'middlewares': DEFAULT_MIDDLEWARE,
            }
        },
        {
            'ws': {  # 正向 WebSocket（作为WebSocket服务器）
                'disabled': True,  # 暂时关闭
                'host': '0.0.0.0',
                'port': 6700,
                'middlewares': DEFAULT_MIDDLEWARE,
            }
        },
    ],
}

ONLINE_STATUS = {  # 在线状态
    0: '在线',
    1: '离开',
    2: '隐身',
    3: '忙碌',
    4: '听歌中',
    5: '星座运势',
    6: '今日天气',
    7: '遇见春天',
    8: 'Timi中',
    9: '吃鸡中',
    10: '恋爱中',
    11: '汪汪汪',
    12: '干饭中',
    13: '学习中',
    14: '熬夜中',
    15: '打球中',
    16: '信号弱',
    17: '在线学习',
    18: '游戏中',
    19: '度假中',
    20: '追剧中',
    21: '健身中',
}
