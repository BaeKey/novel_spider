import requests
from bs4 import BeautifulSoup

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

#获取小说内容
def getContent(start_url):
  res = requests.get(start_url,headers=header)
  res.encoding = 'gbk'
  soup = BeautifulSoup(res.text,'html.parser')

  # 获取小说名字
  novel_name = soup.select('.con_top > a')[2].text
  # 获取章节标题
  title = soup.select('.bookname h1')[0].text
  # 获取文章内容
  text = soup.select('#content')[0].prettify()
  # 优化文本显示
  content = text.replace('<div id="content">', '').replace('</div>','').replace('<p>', '').replace('\n','').replace('</p>','\n')
  #获取下一章链接
  next_url = 'http://www.ibiqu.org' + soup.select('.bottem2 a')[3]['href']

  # 保存小说
  save_novel(novel_name,title,content)
  
  # 判断是否结束
  # 最后一章结束时返回小说目录页面
  if(next_url.split('/')[5] == ''):
    return False
  return getContent(next_url)

"""
  保存小说
  :param title: 小说章节标题
  :param content: 小说内容
  :return:
"""
def save_novel(novel_name, title, content):

    filename = f'{novel_name}' + '.txt'
    print("已下载:" + title)
    with open(filename, mode='a', encoding='utf-8') as f:
        # 写入标题
        f.write(title)
        # 换行
        f.write('\n')
        # 写入小说内容
        f.write(content)


if __name__ == '__main__':
  print("爬取小说的地址：http://www.ibiqu.org/")
  print("请输入要爬取的小说的第一章节地址：（例如：http://www.ibiqu.org/book/52542/20380548.htm）")
  start_url = input()
  getContent(start_url)
  print('小说下载完成!')
