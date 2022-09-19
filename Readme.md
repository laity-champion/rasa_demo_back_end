# 本地服务部署

## neo4j数据同步
```python
# 去官网下载neo4j对应系统的安装包
cmd neo4j.bat console  -- windows系统控制台显示运行
执行build_bg_utils.py   -- 向neo4j同步数据(同步的过程可能比较漫长)
```
## windows环境依赖下载 

- 本人使用的环境是

    - python3.6
    
    - pycharm2020 
  
```python
# 下载Python依赖
python install -r requirements.txt 
```

## rasa 训练并交互
- rasa train --domain domain.yml
- rasa shell 

## 运行网页客户端以及后端服务
前端
- npm install
- npm run start
  
后端
- rasa run --cors "*"
- rasa run actions --actions actions.actions 

## 需要修改的东西

- 将前端发送请求的端口 从5006改为5005

# 服务器服务部署
## 前端部署

- 配置nginx
```editorconfig
server {
        listen 9222;
        server_name  127.0.0.1;
        location /rasa {
            alias /home/doc/rasa/build;
            index index.html index.htm;
        }
}
```
## 后端部署
- python安装
```python
系统自带的python一定不要删
1）前往用户根目录
>: cd ~

2）下载 或 上传 Python3.6.7
# 服务器终端
>: wget https://www.python.org/ftp/python/3.6.7/Python-3.6.7.tar.xz

# 本地终端，给服务器上传
>: scp -r 本地Python-3.6.7.tar.xz ssh root@39.99.192.127:服务器路径
>: scp -r C:\Users\dell\Desktop\pkg\Python-3.6.7.tar.xz ssh root@39.99.192.127~

3）解压安装包
>: tar -xf Python-3.6.7.tar.xz

4）进入目标文件
>: cd Python-3.6.7

5）配置安装路径：/usr/local/python3
>: ./configure --prefix=/usr/local/python3

6）编译并安装
>: make && sudo make install

7）建立软连接：终端命令 python3，pip3
>: ln -s /usr/local/python3/bin/python3.6 /usr/bin/python3
>: ln -s /usr/local/python3/bin/pip3.6 /usr/bin/pip3

8）删除安装包与文件：
>: rm -rf Python-3.6.7
>: rm -rf Python-3.6.7.tar.xz


错误解决：zipimport.ZipImportError: can't decompress data; zlib not available
yum -y install zlib*
```

- 依赖下载
```python
pip3 install -r requirements.txt
```
- 服务运行

```python
nohup rasa run -m models --cors "*" --debug &
nohup rasa run actions --actions actions.actions
```
- 数据导入

执行build_bg_utils.py即可

