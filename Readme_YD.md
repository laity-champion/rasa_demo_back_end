#当进行演示的时候，我们最少需要开启服务
- 启动neo4j
- 启动前端界面（git bash- npm run start）
- rasa run --cors "*"
- rasa run actions --actions actions.actions （启动action服务，可以执行自定义action动作）
#打开这四个服务就可以成功的实现交互
nohup rasa run -m models --cors "*" --debug &


#前端
#项目根目录root下 git bash 打开
# npm i 下载项目依赖 node_modules
npm i
# npm run start 运行项目
npm run start


# 开启服务
- 启动neo4j
- python -m http.server 8888
- rasa run actions --actions actions.actions 

#打开index.html，然后启动这个服务，前端页面
- rasa run --cors "*"
- rasa run --debug --endpoints endpoints.yml
- 这个先不用开了

# 训练命令
- rasa train --domain domain.yml

# 交互命令
- rasa shell 命令行交互

#运行网页客户端
python -m http.server

#rasa交互式学习
rasa interactive

#rasa流程可视化
rasa visualize

#加入交互之后的命令
- rasa train
- rasa run --cors "*" #客户端和rasa服务器存在跨域问题，需要通过设置--cors "*" 来实现
- python -m http.server #运行网页客户端 #会在本地的8000端口启动一个基于HTTP的服务器，在浏览器中进行访问，单击右下角的蓝色对话按钮，就可以和机器人一起对话了





# 关于rasa x 遇到 sanic 的错误时
- pip install sanic-jwt==1.6.0


# 可视化stories
rasa visualize

#  端口冲突
netstat -ano|findstr 5055
taskkill /F /PID 60292

#前端冲突的话
taskkill /pid 26392 -t -f

#加了一个这样的response
  utter_question:
  - text: 您可以这样向我提问：乳腺癌的症状有哪些？/
        脑膜炎要做什么检查？/
        感冒可以怎样预防？/
        感冒需要多久才能治好/
        糖尿病是什么？/
        板蓝根能治什么病？/
        最近老流鼻涕怎么办？/
        什么病不宜吃豆腐？/
        上清丸可以治疗什么疾病？/
        肺活检可以检查什么疾病？

**文件目录**
actions
   |_____actions.py
   |_____api
          |_______answer_search.py 执行sql语句
          |_______app.py    查询天气+闲聊的API
          |_______question_parser.py 生成查询语句
          |_______Spider_open.py 疑难杂症处理
          |_______voice.py  语音识别  
          |_______asr.py 百度API语音识别
          |_______tts.py 百度API语音合成
   |_____data
          |_____lookup_tables  实体扩展
          |_____nlu.yml   定义意图
          |_____rules.yml   规则
          |_____stories.yml  故事
   |_____voice_Friday  robot语音回复文件
   |_____voice_person  用户语音输入文件
   |_____Medical_Spider_API
          |_____Spider_open.py  实时获取结果
   |_____nlu_corpus_process  语料数据格式处理
   |_____models 训练模型
   |_____config 组件等配置文件
   |_____domain.yml     
   |_____medical.json   数据库所需数据
   |_____endpoints.yml  外部消息服务对接的endpoints配置
   |_____credentials.yml  socket参数定义
   |_____nlu_corpus_process  lookups_table下增加语料文件处理code
   |_____match_entity_extractor.py      实体识别  
   |_____model   模型文件
   |_____RUN_Text_To_Voice_Friday.py    文本To语音实现
   |_____RUN_Voice_To_Voice_Friday.py   语音To语音实现
   |_____录音文件
   |_____socketio_connector.py    socket协议连接器
   |_____requirement.txt          项目运行所需安装包
   |_____build_medicalgraph.py    数据-->数据库 导入
   |_____rasa-voice-interface-master.zip     前端语音交互项目


# domain中加上intent：greet/deny/

#8.22改动
stories中query_symptom中设置了词槽，看一下可以实现不

# neo4j构建过程中
载脂蛋白A1\\载脂蛋白B比值  改成与
写入科室实体
写入not_eat关系 
写入do_eat关系
写入recommand_recipes关系
写入 recommand_drug 关系
写入 need_check 关系
写入 acompany_with 关系
写入 疾病 实体的属性


#rasa x安装
https://blog.csdn.net/LeungSr/article/details/122682785


# NLU inbox中进行批注
处理此收件箱是改进助手 NLU 模型的最快方法。
如果消息预测正确，则可以通过选择”标记正确“直接将其保存到训练数据中
如果预测意向不正确，从下拉菜单选择其他一项

#rasax对话中进行批注
对话中存在不正确的 NLU 预测，可以直接从对话页面对其进行注释

#修改问候语
嗨！我是您的 IT 帮助台助理！我可以帮助您打开 IT 帮助台票证，并检查未结票证的状态

#rasax版本-我的Rasa版本为2.6.2，以此为例对应Rasa-X版本为0.40.1

#未加入到domain中的intent
- greet
- goodbye
- affirm
- deny
- mood_great
- mood_unhappy
- bot_challenge
- query_premise
#报错1
rasa.core.processor  - Encountered an exception while running action 'FindTheCorrespondingSymptom'.Bot will continue, but the actions events are
lost. Please check the logs of your action server for more information.

解决方案：尝试在debug mode中使用调试标志-vv运行操作服务器，如rasa run actions -vv，查看代码中的问题所在。（问题可能是因为您可能没有导入Action或sqlite3或其他任何东西）

jieba.setLogLevel(jieba.logging.INFO)
#数据库中可以查到的例子
#一、根据关系查询——疾病-并发症、疾病-科室、疾病-宜吃食物、疾病-药品（疾病-通用药品、疾病-推荐药品）、疾病-症状、疾病-不宜吃食物、疾病-检查、疾病-推荐菜谱
1.腱鞘炎的并发症有哪些/嗜睡的并发症有哪些 
2.汗疱症推荐去哪个科室/韧带炎应该去哪个科室
3.胆囊炎适合吃什么食物/汞中毒适合吃什么食物
4.哮喘应该吃什么药品/甲亢应该吃什么药
5.肠梗阻有什么症状/肠套叠有什么症状
6.白血病不能吃的饮食有什么/溶血性贫血不能吃的饮食有什么
7.痛风应该做什么检查/外痔应该做什么检查
8.高血压推荐菜谱/冠心病推荐菜谱
#二、查询节点本身的属性——疾病节点的属性-病因、治疗科室、治疗周期、治疗方式、治愈概率、简介、易感人群、感染概率、预防措施、症状
1.[黑头粉刺痣](disease)的原因是什么
2.糖尿病应该去哪个科室就诊
3.糖尿病的治疗周期有多长
4.肺纤维化的治疗方式有哪些
5.
#三、反向检查——检查-疾病、症状-疾病、不宜吃食物-疾病、药品-疾病
1.颈静脉回流试验可以检查什么疾病/血常规可以检查什么疾病
2.出现衰弱是什么疾病的表现/出现腹围增大可能是什么疾病
3.什么疾病不适合吃苏打粉/什么疾病不适合喝啤酒
4.藿香正气水可以治疗什么疾病/诺氟沙星胶囊可以治疗什么疾病

1.crf实体抽取配置
2.match_entity_extractor.py有啥用
3.entities怎么传值
4.DIETClassifier


#填槽问答
1.请问你需要查询哪些疾病呢
2.要查询疾病的什么信息呢？比如病因、预防措施、易感人群等等

#1.根据关系查询（正向）-疾病-并发症、疾病-科室、疾病-宜吃食物、疾病-药品（疾病-通用药品、疾病-推荐药品）、疾病-症状、疾病-不宜吃食物、疾病-检查、疾病-推荐菜谱
感冒不能吃什么
感冒的检查项目有哪些
萎缩性咽炎应该吃什么药
#2.根据关系查询（逆向）-检查-疾病、症状-疾病、不宜吃食物-疾病、药品-疾病
腹水检查可以检查什么疾病
胆心综合征是什么疾病的表现
上清丸可以治疗什么疾病
#3.查询节点属性-疾病节点的属性-病因、治疗科室、治疗周期、治疗方式、治愈概率、简介、易感人群、感染概率、预防措施、症状
感冒的症状有哪些？
感冒的治疗周期有多长

感冒不能吃什么？/感冒的检查项目有哪些？/萎缩性咽炎应该吃什么药/腹水检查可以检查什么疾病 /胆心综合征是什么疾病的表现 /上清丸可以治疗什么疾病 /感冒的症状有哪些？
/感冒的治疗周期有多长

#关于RegexEntityExtractor不能正确识别LookupTables中的实体的问题
#后来发现没啥用，但是加入RegexEntityExtractor之后，可以识别出来查找表中的专业名词
问题分析：继续追踪，在_convert_lookup_tables_to_regex方法中可以看到，正则表达式又是调用_generate_lookup_regex方法生成的。
最终，我们来到了_generate_lookup_regex方法，发现了事情的真相。直接看return的部分，
我们发现，返回的正则表达式并不是简单地将查找表中的例子用|连接起来，而是在每个例子前后都加上了一个\b，而这个\b就是问题的关键。
经过搜索（博主并不擅长正则表达式，见谅），原来\b是为了在匹配时只匹配边界的例子，如er\b可以匹配never中的er，但不能匹配verb中的er，
而中文的单词间并没有空格，导致句子中的例子无法被识别。

解决方案：只需将rasa/nlu/utils/pattern_utils.py中_generate_lookup_regex方法中的返回值中的\\b删去，
即可得到适合中文的RegexEntityExtractor

随之而来的问题描述：如果DIETClassifier已经识别出某一城市，而RegexEntityExtractor根据lookup table又识别了一次该城市，
就会出现实体被识别两次的情况

解决方案：所以在修改完pattern_utils.py之后，还需要对rasa/nlu/extractors/regex_entity_extractor.py的_extract_entities方法进行如下修改，
使同一个城市不会被多次识别
————————————————
原文链接：https://blog.csdn.net/Humanlike_/article/details/109731727

#bug
Transport closed @ ('127.0.0.1', 52171) and exception experienced during error handling
解决办法：重启一下电脑或者重启一下服务


# c:\users\yd\appdata\local\programs\python\python36\lib\site-packages\aiohttp\helpers.py"
源码：raise asyncio.TimeoutError from None


1.在credentials中设置那三行 有一个链接，websocket-channels
2.用下面的命令来开启机器人
- rasa run -m models --enable-api --cores "*" --debug
- rasa run actions
3.现在可以看到为我们的机器人服务看到不同的api细节
  可以使用webchat脚本将机器人链接到网页上
  http://github.com/mrbot-ai/rasa-webchat
  创建一个网页并将下面的代码加上
  
4.改变socket url变为rasa服务地址
5.然后开始测试
打开项目文件夹，之后打开index页面

- rasa run -vv --cors "*"
  Terminal终端命令执行:pip install -r requirements.txt 即可安装
  

- /opt/neo4j/neo4j-community-4.1.1/bin/neo4j console

https://blog.csdn.net/sinat_39595180/article/details/108292874?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166320652516800182159791%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=166320652516800182159791&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-108292874-null-null.142^v47^pc_rank_34_default_3,201^v3^control_2&utm_term=centos7%20neo4j%E5%AE%89%E8%A3%85%E6%95%99%E7%A8%8B&spm=1018.2226.3001.4187
https://blog.csdn.net/qq_33951308/article/details/84027922?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166320652516800182159791%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=166320652516800182159791&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-3-84027922-null-null.142^v47^pc_rank_34_default_3,201^v3^control_2&utm_term=centos7%20neo4j%E5%AE%89%E8%A3%85%E6%95%99%E7%A8%8B&spm=1018.2226.3001.4187

rasa run -m models --cors "*" -p 5006
