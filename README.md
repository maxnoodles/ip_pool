# ip_pool
ip代理池
python3.6 + request + Flask + redis
运行schedule.py
多进程同时调用getter.py中的Getter(), tester.py中的Tester()，api中的app.run()
Getter()获取器启动crawl.py中的抓取代理网站并存入redis的zset中
Tester()开始测试redis数据库zset中的代理，代理初始分数10分，测试通过给予100分，失败减4分，小于0分删除
app.run()使用Flask启动本地5000端口，/random随机获取测试通过的一个代理, /count获取代理总数
