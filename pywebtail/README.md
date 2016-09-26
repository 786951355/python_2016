#### 集中查看客户端上被监控的文件， 左边显示运行客户端的列表及日志文件日志数据先从客户端发送到服务端，默认保存在/log/下面


环境
python `3.5.2`  tornado `4.4.1`

依赖`requests`模块,安装`requests`

`pip install requests`


```
修改agent.py、templates目录下面的tail.html, index.html中的对应的IP地址
端口可以根据需要自己指定
```


客户端上运行
`python agent.py &`

服务器端
```
python server.py &
python webapp.py &
```


停止客户端
```
kill agent-pid
```

停止服务端
```
kill server-pid
kill webapp-pid
```






