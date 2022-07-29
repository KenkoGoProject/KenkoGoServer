DEFAULT_MIDDLEWARE = {
    'access-token': '1231',
    'filter': '',
    'rate-limit': {
        'enabled': False,
        'frequency': 1,
        'bucket': 1,
    },
}


DEFAULT_GOCQ_CONFIG = {
    'account': {
        'uin': 0,
        'password': '',
        'encrypt': False,
        'status': 0,
        'relogin': {
            'delay': 3,
            'interval': 3,
            'max-times': 0,
        },
        'use-sso-address': True,
    },
    'heartbeat': {
        'interval': 5,
    },
    'message': {
        'post-format': 'string',
        'ignore-invalid-cqcode': False,
        'force-fragment': False,
        'fix-url': False,
        'proxy-rewrite': '',
        'report-self-message': True,
        'remove-reply-at': False,
        'extra-reply-data': False,
        'skip-mime-scan': False,
    },
    'output': {
        'log-level': 'error',  # 默认为warn, 支持 trace,debug,info,warn,error
        'log-aging': 30,
        'log-force-new': False,
        'debug': False,
    },
    'default-middlewares': DEFAULT_MIDDLEWARE,
    'database': {
        'leveldb': {
            'enable': True,
        },
    },
    'servers': [
        {
            'http': {
                'address': '127.0.0.1:35700',
                'timeout': 5,
                'long-polling': {
                    'enabled': False,
                    'max-queue-size': 2000,
                },
                'middlewares': DEFAULT_MIDDLEWARE,
                # 'post': [
                #     {
                #         'url': 'http://127.0.0.1:18082/gocq',
                #         'secret': '',
                #     }
                # ],
            }
        },
        # {
        #     'ws': {
        #         'host': '0.0.0.0',
        #         'port': 6700,
        #         'middlewares': default_middleware,
        #     }
        # },
        {
            'ws-reverse': {
                'universal': 'ws://127.0.0.1:18082/instance',
                'reconnect-interval': 3000,
                'middlewares': DEFAULT_MIDDLEWARE,
            }
        },
    ],
}