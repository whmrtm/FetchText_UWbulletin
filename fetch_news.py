import urllib.request
import urllib.response
import urllib.parse
import smtplib
from email.mime.text import MIMEText
import re
import time

class fetch_from_bulletin:
	def __init__(self,url,to):
		self.myUrl = url
		self.User_agent = "Mozilla/4.0(compatible;MSIR 5.5;Windows NT)"
		self.headers = {"User-Agent:":self.User_agent}
		self.sender = 'whmrtm@gmail.com'
		self.passwd = 'whm9316rtm'
		self.to = to
		self._css = '<link type="text/css" rel="stylesheet" href="https://uwaterloo.ca/daily-bulletin/sites/ca.daily-bulletin/files/css/css_E9Jx7KnM-yqRxjhPa8EV5J8WR_ykPxCCDdg2xV3lpFg.css" media="screen" /><link type="text/css" rel="stylesheet" href="https://uwaterloo.ca/daily-bulletin/sites/ca.daily-bulletin/files/css/css_sRoiJhQvJQq6QeaA_k2TBTUGBBlzX2SqcMVA03KcM3A.css" media="all" /><link type="text/css" rel="stylesheet" href="https://uwaterloo.ca/daily-bulletin/sites/ca.daily-bulletin/files/css/css_gNWCS6wE181QWaYxguqP8_wmzWEeh5_XoIKywvEAozw.css" media="all" /><link type="text/css" rel="stylesheet" href="https://uwaterloo.ca/daily-bulletin/sites/ca.daily-bulletin/files/css/css_JsjqRffb60798aNiwPIdcykQm2v0frI1XERvIaW_E2E.css" media="all" /><link type="text/css" rel="stylesheet" href="https://uwaterloo.ca/daily-bulletin/sites/ca.daily-bulletin/files/css/css_batA2UMU7p9a6KjhhxVxaktSXYsGgGaa2cXmNi_oyMM.css" media="print" />'
# get the unicode of the UWbulletin
	def get_article(self):
		try:
			req=urllib.request.Request(self.myUrl,headers=self.headers)
			print('Obtain response from the server.......')
		except:
			print('Fail to get response.........')
		response=urllib.request.urlopen(req)
		result=response.read()
		unicodepage=result.decode('gb2312', 'ignore')
		the_time = re.search(r'<title>(.*)</title>',unicodepage,re.DOTALL).group(1)
		s_split = re.split('<div class="field-items">', unicodepage)
		thearticle = s_split[1]
		thearticle = re.sub('<img .*?/>',"",thearticle)
		thearticle = re.split('<div id="footer">',thearticle)[0]
		thearticle = "<html><head>"+self._css +"</head><body><h1>"+the_time+"</h1>"+thearticle+"</body></html>"
		return thearticle
	def mail(self,subject,msg):
			body=MIMEText(msg,'html')
			body['From']=self.sender
			body['To']=self.to
			body['Subject']=subject
			server=smtplib.SMTP("smtp.gmail.com",587)
			server.ehlo()
			server.starttls()
			server.ehlo()
			try:
				server.login(self.sender,self.passwd)
				print("Successfully login........")
			except:
				print("Login Failure...........")
			try:
				server.sendmail(self.sender,self.to,body.as_string())
				print("Mail successfully sent!")
				server.close()
			except:
				print('Error! Mail sent failure!')
				server.close()
	# execute
	def start(self):
		while(1):
			article=self.get_article()
			print('Article fetched..........')
			self.mail("Today's bulletin",article)			
			time.sleep(86400)
	



myclass=fetch_from_bulletin("http://bulletin.uwaterloo.ca/","whmowen@gmail.com")
myclass.start()
#print(article)
# What needs to be improved:
#             execute regularly
#             use class to conseal the whole module