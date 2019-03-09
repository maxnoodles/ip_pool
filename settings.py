# redis 数据库地址
REDIS_HOST = '127.0.0.1'

# redis 端口
REDIS_PORT = 6379

# redis KEY名
REDIS_KEY = 'proxies'

# 代理权重
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

VALID_STATUS_CODES = [200, 302]

# 代理池数量
POOL_UPPER_THRESHOLD = 2000

# 检查周期
TESTER_CYCLE = 10
# 获取周期
GETTER_CYCLE = 300

# 测试API 抓那个测试哪个
TEST_URL = 'http://www.baidu.com'
# TEST_URL = 'https://www.ipip.net/'

# API配置
API_HOST = '127.0.0.1'
API_PORT = 5000

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 20
