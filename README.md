### 自动提取算法部署

#### 支持两种部署方式

1. 使用gunicorn部署：

   使用gunicorn部署支持多用户并发请求，可以修改gun.py并发数，修改workers这个参数就可以，此外需要注意的是，根据你自己的需要修改端口号，参数为bind，将其中的20002修改为你自己的端口号。存放gunicorn运行日志需要新建gunicorn_log文件夹，也可以使用你自定义文件夹，修改pidfile和logfile这两个参数。

   python依赖查看requirements.txt这个文件

2. 使用gunicorn+zmq部署

   这种部署方式将算法作为单独的服务，使用pyzmq进行算法服务部署。gunicorn是接收来自外面的REST请求，此时gunicorn服务作为服务器，然后gunicorn服务作为客户端想算法服务进行请求。这种分层不熟的优点如下：

   独立REST服务和算法服务，解耦合（支持只部署一次算法服务，但是可以部署多次REST服务，这样就可以，将算法服务部署在公司内部，REST服务部署在公司外，保护算法不被外部知道。同时可以节约资源，一般情况下，算法比较消耗资源)

   zmq部署服务可以支持负载均衡，一次POST请求，gunicorn服务接收到这次请求，根据数据量，对数据进行切分，分成多个对zmq服务进行请求，支持高并发，可以充分使用cpu。

#### 执行流程
1. 使用gunicorn部署
执行gunicorn -c gun.py annotation_server:app
2. 使用gunicorn+zmq部署
先执行zmq_server_new下的zmq_start.py，启动zmq服务，然后执行gunicorn -c gun.py annotation_zmq_server:app
#### 支持Docker部署
1. 使用gunicorn部署 使用Dockerfile文件
2. 使用gunicorn+zmq部署 使用Dockerfile_zmq文件
#### 需要注意的
需要下载pyltp的模型文件夹放在与data文件夹同目录，具体可以修改查看config.py


   

   

   

