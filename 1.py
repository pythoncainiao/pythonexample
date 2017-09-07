 # -*- coding:utf-8 -*-
  2 '''
  3 抓取豆瓣电影某部电影的评论
  4 这里以《我不是潘金莲为例》
  5 网址链接:https://movie.douban.com/subject/26630781/comments
  6 为了抓取全部评论需要先进行登录
  7 '''
  8 from selenium import webdriver
  9 import time
 10 import codecs
 11 import jieba
 12 import jieba.analyse as analyse
 13 from wordcloud import WordCloud
 14 from scipy.misc import imread
 15 from os import path
 16 
 17 def get_douban_comments(url):
 18     comments_list = [] # 评论列表
 19     login_url = 'https://accounts.douban.com/login?source=movie'
 20     user_name = '1111111'  # 这里替换成你的豆瓣用户名
 21     password = '11111111'  # 这里替换成你的密码
 22     driver = webdriver.Firefox() # 启动Firefox()
 23     driver.get(login_url)
 24     driver.find_element_by_id('email').clear() # 清除输入框
 25     driver.find_element_by_id('email').send_keys(user_name) # 输入用户名
 26     driver.find_element_by_id('password').clear()
 27     driver.find_element_by_id('password').send_keys(password) # 输入密码
 28     captcha_field = raw_input('请打开浏览器输入验证码:') # 手动填入验证码
 29     driver.find_element_by_id('captcha_field').send_keys(captcha_field)
 30     driver.find_element_by_class_name('btn-submit').click() # 点击登录按钮
 31     time.sleep(5) # 等待跳转到登录之后的页面
 32     driver.get(url) # 定位到目标页面
 33     driver.implicitly_wait(3) # 智能等待3秒
 34     n = 501 # 页数
 35     count = 10000 # 评论数目
 36     while True:
 37         try:
 38             results = driver.find_elements_by_class_name('comment')
 39             for result in results:
 40                 # author = result.find_elements_by_tag_name('a')[1].text # 作者
 41                 # vote = result.find_element_by_class_name('comment-vote').find_element_by_tag_name('span').text # 赞同数目
 42                 # time0 = result.find_element_by_class_name('comment-info').find_elements_by_tag_name('span')[1].text # 时间
 43                 comment = result.find_element_by_tag_name('p').text # 评论内容
 44                 comments_list.append(comment+u'\n')
 45                 print u"查找到第%d个评论" % count
 46                 count += 1
 47             driver.find_element_by_class_name('next').click() # 点击下一页
 48             print u'第%d页查找完毕!' % n
 49             n += 1
 50             time.sleep(4)
 51         except Exception,e:
 52             print e
 53             break
 54     with codecs.open('pjl_comment.txt','a',encoding='utf-8') as f:
 55         f.writelines(comments_list)
 56     print u"查找到第%d页,第%d个评论!" %(n,count)
 57 
 58 # 得到所有关键词
 59 def get_all_keywords(file_name):
 60     word_lists = [] # 关键词列表
 61     with codecs.open(file_name,'r',encoding='utf-8') as f:
 62         Lists = f.readlines() # 文本列表
 63         for List in Lists:
 64             cut_list = list(jieba.cut(List))
 65             for word in cut_list:
 66                 word_lists.append(word)
 67     word_lists_set = set(word_lists) # 去除重复元素
 68     sort_count = []
 69     word_lists_set = list(word_lists_set)
 70     length = len(word_lists_set)
 71     print u"共有%d个关键词" % length
 72     k = 1
 73     for w in word_lists_set:
 74         sort_count.append(w+u':'+unicode(word_lists.count(w))+u"次\n")
 75         print u"%d---" % k + w+u":"+unicode(word_lists.count(w))+ u"次"
 76         k += 1
 77     with codecs.open('count_word.txt','w',encoding='utf-8') as f:
 78         f.writelines(sort_count)
 79 
 80 def get_top_keywords(file_name):
 81     top_word_lists = [] # 关键词列表
 82     with codecs.open(file_name,'r',encoding='utf-8') as f:
 83         texts = f.read() # 读取整个文件作为一个字符串
 84         Result = analyse.textrank(texts,topK=20,withWeight=True,withFlag=True)
 85         n = 1
 86         for result in Result:
 87             print u"%d:" % n ,
 88             for C in result[0]: # result[0] 包含关键词和词性
 89                 print C,u"  ",
 90             print u"权重:"+ unicode(result[1]) # 关键词权重
 91             n += 1
 92 
 93 # 绘制词云
 94 def draw_wordcloud():
 95    with codecs.open('pjl_comment.txt',encoding='utf-8') as f:
 96        comment_text = f.read()
 97    cut_text = " ".join(jieba.cut(comment_text)) # 将jieba分词得到的关键词用空格连接成为字符串
 98    d = path.dirname(__file__) # 当前文件文件夹所在目录
 99    color_mask = imread("F:/python2.7work/wordcloud/alice_color.png") # 读取背景图片
100    cloud = WordCloud(font_path=path.join(d,'simsun.ttc'),background_color='white',mask=color_mask,max_words=2000,max_font_size=40)
101    word_cloud = cloud.generate(cut_text) # 产生词云
102    word_cloud.to_file("pjl_cloud.jpg")
103 
104 
105 
106 if __name__ == '__main__':
107     '''
108     url = 'https://movie.douban.com/subject/26630781/comments?start=10581&limit=20&sort=new_score'
109     get_douban_comments(url)
110     file_name = 'pjl_comment.txt'
111     get_top_keywords(file_name)
112     '''
113     draw_wordcloud()
