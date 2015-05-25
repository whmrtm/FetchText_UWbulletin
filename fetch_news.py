import urllib.request
import urllib.response
import urllib.parse
import smtplib
from email.mime.text import MIMEText
import re
import time

class fetch_from_bulletin:
	def __init__(self, url, to, sender, passwd, interval):
		self._myUrl = url
		self.User_agent = "Mozilla/4.0(compatible;MSIR 5.5;Windows NT)"
		self._headers = {"User-Agent:":self.User_agent}
		self._sender = sender
		self._passwd = passwd
		self._to = to
		self._interval = interval
		self._css = '<link type="text/css" rel="stylesheet" href="https://uwaterloo.ca/daily-bulletin/sites/ca.daily-bulletin/files/css/css_E9Jx7KnM-yqRxjhPa8EV5J8WR_ykPxCCDdg2xV3lpFg.css" media="screen" /><link type="text/css" rel="stylesheet" href="https://uwaterloo.ca/daily-bulletin/sites/ca.daily-bulletin/files/css/css_sRoiJhQvJQq6QeaA_k2TBTUGBBlzX2SqcMVA03KcM3A.css" media="all" /><link type="text/css" rel="stylesheet" href="https://uwaterloo.ca/daily-bulletin/sites/ca.daily-bulletin/files/css/css_gNWCS6wE181QWaYxguqP8_wmzWEeh5_XoIKywvEAozw.css" media="all" /><link type="text/css" rel="stylesheet" href="https://uwaterloo.ca/daily-bulletin/sites/ca.daily-bulletin/files/css/css_JsjqRffb60798aNiwPIdcykQm2v0frI1XERvIaW_E2E.css" media="all" /><link type="text/css" rel="stylesheet" href="https://uwaterloo.ca/daily-bulletin/sites/ca.daily-bulletin/files/css/css_batA2UMU7p9a6KjhhxVxaktSXYsGgGaa2cXmNi_oyMM.css" media="print" />'
# get the unicode of the UWbulletin
# then use regular expression to abstract brief information from the unicodepage
	def get_article(self):
		try:
			req=urllib.request.Request(self._myUrl,headers=self._headers)
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
# send the email with the given subject and message
	def mail(self,subject,msg):
			body=MIMEText(msg,'html')
			body['From']=self._sender
			body['To']=self._to
			body['Subject']=subject
			server=smtplib.SMTP("smtp.gmail.com",587)
			server.ehlo()
			server.starttls()
			server.ehlo()
			try:
				server.login(self._sender,self._passwd)
				print("Successfully login........")
			except:
				print("Login Failure...........")
			try:
				server.sendmail(self._sender,self._to,body.as_string())
				print("Mail successfully sent!")
				server.close()
			except:
				print('Error! Mail sent failure!')
				server.close()
# execute the update for every _interval seconds
	def start(self):
		while(1):
			article=self.get_article()
			print('Article fetched..........')
			self.mail("Today's bulletin",article)			
			time.sleep(self._interval)
	
<<<<<<< HEAD
# input all the information we need
=======


>>>>>>> f2a197a6af6f05f5455c037b0ea238fdaf54b999
url = "http://bulletin.uwaterloo.ca/"
to = input("The email address you want to receive updates: ")
sender = input("The email you are sending updates with: ")
passwd = input("The password of you email: ")
interval = float(input("Time interval between each updates (seconds): "))
<<<<<<< HEAD
# then run the program
fecth = fetch_from_bulletin(url, to, sender, passwd, interval)
fecth.start()
=======
myclass=fetch_from_bulletin(url, to, sender, passwd, interval)
myclass.start()
>>>>>>> f2a197a6af6f05f5455c037b0ea238fdaf54b999
