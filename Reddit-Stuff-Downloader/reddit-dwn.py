import praw
import json
import requests
import urllib.request	# download in 2nd method
import os
from bs4 import BeautifulSoup
from shutil import copyfile
import time
import urllib.request
import dpath.util		# comments download - dictionary search,edit

import progressbar
import re

pbar = None
def show_progress(block_num, block_size, total_size):
	global pbar
	if pbar is None:
		pbar = progressbar.ProgressBar(maxval=total_size)
		pbar.start()
	downloaded = block_num * block_size
	if downloaded < total_size:
		pbar.update(downloaded)
	else:
		pbar.finish()
		pbar = None
		
		
with open('config.json','r') as configFile:
	confData = json.load(configFile)
	_client_id = confData['client_id']
	_client_secret = confData['client_secret']
	_user_agent = confData['user_agent']
	_username = confData['username']
	_password = confData['password']


reddit = praw.Reddit(client_id=_client_id,
					 client_secret=_client_secret,
					 user_agent=_user_agent,
					 username=_username,
					 password=_password)

headers_other = [
	("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
		"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 "\
		"Safari/537.36 OPR/54.0.2952.64"),
	("Accept", "text/html,application/xhtml+xml,application/xml;" \
		"q=0.9,image/webp,image/apng,*/*;q=0.8"),
	("Accept-Charset", "ISO-8859-1,utf-8;q=0.7,*;q=0.3"),
	("Accept-Encoding", "none"),
	("Accept-Language", "en-US,en;q=0.8"),
	("Connection", "keep-alive")
]

headers = {
	'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) \
	 		AppleWebKit/537.36 (KHTML, like Gecko) \
	   		Chrome/75.0.3770.100 Safari/537.36',
	'Connection' : 'keep-alive'
}

def checkDownloadFormat(url):
	
	if('comments' in url and 'reddit.com' in url):
		return 'POST',url
	elif('comments' in url and '/r/' in url[:3]):
		return 'POST','https://www.reddit.com' + url

	if('youtu.be' in url or 'youtube.com' in url):
		return 'youtube',url
	
	if('reddit.com' in url and 'gallery' in url):
		print('reddit gallery')
		rcon = requests.get(url,headers = headers)
		re_url = []
		soup = BeautifulSoup(rcon.content,"html.parser")
		try:
			for ii in  soup.find_all('img'):
				srcUrl = ii.get('src')
				if('preview.redd.it' in srcUrl):
					re_url.append(srcUrl.replace('&amp;','&'))
			ext = re.findall("\.\w+\?",re_url[0])[0][:-1]
			return ext, re_url
		except Exception as e:
			print(e)
			return '.txt',url
		
	if(url.find('v.redd.it') != -1):
		print('v.reddit.it .mp4 video and audio')
		bitrates = ["DASH_1080","DASH_720","DASH_600","DASH_480","DASH_360","DASH_240","DASH_96","DASH_1_2_M","DASH_2_4_M","DASH_600_K",
			  "DASH_1080.mp4","DASH_720.mp4","DASH_600.mp4","DASH_480.mp4","DASH_360.mp4","DASH_240.mp4","DASH_96.mp4","DASH_1_2_M.mp4","DASH_2_4_M.mp4","DASH_600_K.mp4"]
					
		for bitrate in bitrates:
			videoURL = url+"/"+bitrate

			try:
				responseCode = urllib.request.urlopen(videoURL).getcode()
			except urllib.error.HTTPError:
				responseCode = 0

			if responseCode == 200:
				return '.mp4',videoURL 
	
	if(url.find('redgifs.com') != -1 and ('.webm' in url or '.mp4' in url or '.gif' in url)):
		mod_url = url[:url.rfind('.')]+'.mp4'
		try:
			responseCode = urllib.request.urlopen(mod_url).getcode()
		except urllib.error.HTTPError:
			responseCode = 0

		if(responseCode == 200):
			return '.mp4',mod_url
		else:
			return str(url[url.rfind('.'):]),url

	if(url.find('redgifs.com') != -1):
		print('redgifs .mp4')
		try:
			rcon = requests.get(url,headers = headers)
		except:
			print('connection reset ?!?!')
			return '.txt',url
		soup = BeautifulSoup(rcon.content,"html.parser")
		url_mod = str([link.get('src') for link in soup.find_all('source')][1])
		return str(url_mod[url_mod.rfind('.'):]),url_mod

	if(url.find('streamable.com') != -1):
		print('streamable .mp4')
		rcon = requests.get(url,headers = headers)
		soup = BeautifulSoup(rcon.content,"html.parser")
		url_mod = 'http://' + str([link.get('src') for link in soup.find_all('video')][0])[2:]
		return '.mp4',url_mod

	if(url.find('gfycat.com') != -1):
		
		rcon = requests.get(url,,headers = headers)			
		lengthEstimated = len(url.split('/')[-1]) + 30 + 15		# estimation
		srcon = str(rcon.content)
		posEnd_ = srcon.find('.mp4" type="video/mp4"')
		posStart = srcon.find('https://thumbs.gfycat.com/',posEnd_ - lengthEstimated)
		posEnd = posEnd_ + 4						# .mp4
		url_mod = srcon[posStart:posEnd]
		#print("URL Modified : "+url_mod)
  
		if(url_mod == ""):
			print('gfycat - redgifs redirect .mp4')
			soup = BeautifulSoup(rcon.content,"html.parser")
			url_mod = str([link.get('src') for link in soup.find_all('source')][1])
			return str(url_mod[url_mod.rfind('.'):]),url_mod
   
		print('gfycat .mp4')
		return '.mp4',url_mod

	if(url.find('imgur.com') != -1 and url.find('.gif') != -1):		# .gifv or gif
		print('imgur .mp4')
		posEnd = url.find('.gif')
		url_mod = url[:posEnd] + '.mp4'
		return '.mp4',url_mod

	if(url.find('imgur.com') != -1 and url.find('.mp4') != -1):
		print('imgur .mp4 dir')
		return '.mp4',url

	if(url.find('imgur.com') != -1 and url.find('.jpg') != -1):
		print('imgur .jpg dir')
		return '.jpg',url

	if(url.find('imgur.com') != -1 and url.find('.png') != -1):
		print('imgur .png dir')
		return '.png',url

	if(url.find('imgur.com') != -1):
		print('imgur .jpg')
		rcon = requests.get(url,headers = headers)			
		lengthEstimated = 35
		srcon = str(rcon.content)
		posEnd_ = srcon.find('.jpg')
		posStart = srcon.find('https://i.imgur.com',posEnd_ - lengthEstimated)
		posEnd = posEnd_ + 4															
		url_mod = srcon[posStart:posEnd]
		#print("URL Modified : "+url_mod)
		return '.jpg',url_mod

	if(url.find('.jpg') != -1):			#url[-3:] -> .jpg   check ? 
		print('.jpg')
		return '.jpg',url

	if(url.find('.png') != -1):			
			print('.png')
			return '.png',url
	if(url.find('.gif') != -1):			
			print('.gif')
			return '.gif',url

	#rcon = requests.get(url)

	print('not the above format ! DEBUGGING Req- ')
	return '.txt',url

	#print(url.split("/"))		# debug purpose


def downloadCoreFunc(re_url, file_name, exten):
	if(exten == '.txt'):
		raise ValueError('cannot DOWNLOAD -rising manual error !')
	if(exten == 'POST' or exten == 'youtube'):
		return exten
	#if(sss.find(post_ID) == -1):
	t=3
	flag = 1
	while(t):
		try:
			print("...")
			r = requests.get(re_url,timeout=65,headers=headers)
			flag = 0
			break
		except:
			t=t-1
			continue
	if(flag == 0):		
		print("saving!")
		try:
			if('<?xml' in str(r.content)):
				return 'NO_AUDIO'
			with open(file_name,"wb") as f:
				f.write(r.content)
		except:
			print("ERROR WHILE SAVING!!")
			raise ValueError('cannot DOWNLOAD -rising manual error !')
	else:
		try:
			print("TRYING Again and Saving!?")
			t=5
			flag = 1
			while(t):
				try:
					print("...>")
					# request = requests.get(re_url, timeout=10, stream=True)
					# with open(file_name, 'wb') as fh:
					# 	for chunk in request.iter_content(100): 	# 1024 * 1024
					# 		fh.write(chunk)
					opener = urllib.request.build_opener()
					urllib.request.install_opener(opener)
					opener.addheaders = headers_other
					urllib.request.install_opener(opener)
					urllib.request.urlretrieve(re_url,file_name,show_progress)
	
					flag = 0
					break
				except:
					t=t-1
					continue
			if(flag == 1):
				raise ValueError('cannot DOWNLOAD -rising manual error !')
		except:
			raise ValueError('cannot DOWNLOAD -rising manual error !')
	return exten

def download(post_ID, url, re_url, file_name, title, exten):
	try:
		
		if(type(re_url) == list):
			loopCnt = 1
			for linkUrl in re_url:
				#print(linkUrl)
				exten = downloadCoreFunc(linkUrl, post_ID+'_'+str(loopCnt)+exten, exten)
				loopCnt += 1
		else:
			exten = downloadCoreFunc(re_url, file_name, exten)
	except Exception as e:
		#print(e)		# for debugging
		print("cannot able to download")
		newD = '{"title" : "'+ str(title) +'", "url" :"' + str(url) + '", "re_url" :"' + str(re_url) + '"}'
		txt_file = open(post_ID+'.txt','a')
		txt_file.write(newD)
		txt_file.close()
		exten = '.txt'
	return exten


def getCommentsDownload(post,post_ID):
		
	post.comments.replace_more(limit=3)
	count = 0
	comm = {}
	parL = []
	level = 0
	for comment in post.comments.list():
		#print(20*'-')
		
		pID = str(comment.parent())
		cID = str(comment.id)
		#print('Parent ID: ', pID)
		#print('Comment ID: ', cID)
		# print(comment.author.name)
		# print(comment.body)
		# print('\n')
		try:
			_author = str(comment.author.name)
		except:
			_author = '[DELETED]'
		try:
			_commentBody = str(comment.body)
		except:
			_commentBody = '[DELETED]'
		
		comm_data = {
			"_author": _author,
			"_comment": _commentBody,
			"_reply": {}
		}
		if(post_ID == pID):
			comm[cID] = comm_data
			parL.append(cID)
		else:
			if(pID in parL):
				level += 1
				parL = []
			extraPath = (level-1) * '*/*/'
			#path = [path 
			#print(json.dumps(comm,indent = 4, sort_keys=True))
			for path,extra in dpath.util.search(comm, extraPath +pID, yielded=True):
				path = path
			dpath.util.new(comm, path + '/_reply/' + cID, comm_data)
			parL.append(cID)


		count +=1
	print("\nCount : ",count)
	json_file = open(post_ID+'_comm_.json','w')
	json.dump(comm,json_file,indent = 4, sort_keys=True)




def getSubredditPosts(subredditName,limitPosts,filter_type):

	print('\n----------------------'+subredditName+'------------>'+filter_type+'----------\n')
	subreddit = reddit.subreddit(subredditName)	#subreddit name

	try:
		os.mkdir(subredditName)
	except:
		pass
	os.chdir(subredditName)


	try:
		json_file = open(subredditName+'.json')
		json_file.close()
	except:
		json_fileI = open(subredditName+'.json','a')
		dataInit = '''{ "POST-ID": { 
								"title" : "POST-TITLE",
								"url" :"POST-URL"
							}
						}'''
		dataInitJSON = json.loads(dataInit)
		json.dump(dataInitJSON,json_fileI,indent = 4, sort_keys=True)
		json_fileI.close()

	time_ = str(time.time()).split('.')[0]
	copyfile(subredditName+'.json', subredditName+'_BACKUP_'+time_+'.json')

	json_file = open(subredditName+'.json','r')
	data = json.load(json_file)
	json_file.close()
	#	=====================================================================================
	if(filter_type == 'hot'):
		posts = subreddit.hot(limit=limitPosts)
	elif(filter_type == 'top'):
		posts = subreddit.top('all',limit=limitPosts)
	for post in posts:
		print(str(post))		# put dir(post) for all attributes
		post_ID = str(post)
  
		if(_comments):			# irrespective of available, downloading comments
			try:
				cf = open(post_ID+'_comm_.json','r')
				cf.close()
			except:
				try:
					getCommentsDownload(post,post_ID)
					print('comments downloaded')
				except Exception as e:
					print(e)
					print('error downloading comments!')
		exist_IDs = [ID for ID in data]
		if(post_ID in exist_IDs):
			continue
		
		url = (post.url)
		title = (post.title)
		print(url)
		title = title.replace("\"","*")
		title = title.replace("\'","_")
		print(title)
	
		# file_name = url.split("/")
		# #print(file_name)
		# if len(file_name) == 0:
		# 	file_name = re.findall("/(.*?)", url)
		# #print(file_name)
		# file_name = file_name[-1]
		# #print(file_name)
		# if "." not in file_name:
		# 	file_name += ".jpg"

		if(post.selftext != ''):
			print('POST saved!')
			txt_file = open(post_ID+'_text_.txt','a')
			txt_file.write(post.selftext)
			txt_file.close()
		exten,re_url = checkDownloadFormat(url)
		file_name = post_ID + exten		# might change for other format media
		print(file_name)
		
		
		
		#url = re_url
		
		if(url.find('v.redd.it') != -1 and exten != '.txt'):
			file_name_v = 'v_'+ file_name
			exten = download(post_ID, url, re_url, file_name_v, title, exten)
			file_name_a = 'a_'+ file_name
			re_url_au = re_url[:re_url.rfind('/')] + '/audio'
			exten = download(post_ID, url, re_url_au, file_name_a, title, exten)
			if(exten != 'NO_AUDIO'):
				os.system('ffmpeg -i '+ file_name_v+' -i '+file_name_a+' -c:v copy -c:a aac -strict experimental '+file_name)
				os.remove(file_name_v)
				os.remove(file_name_a)
			else:
				os.rename(file_name_v,file_name)

		elif(exten == 'youtube'):
			print('Youtube Video txt file saved!')
			txt_file = open(post_ID+'_ytb_.txt','a')
			txt_file.write(title + '\n\n' + url)
			txt_file.close()
		elif(exten != 'POST' and exten != 'youtube'):
			exten = download(post_ID, url, re_url, file_name, title, exten)
	
	
		if(exten != '.txt'):
			#newD = '{"title" : "'+ str(title) +'", "url" :"' + str(url) + '"}'
			newD = {
				'title' : str(title),
				'url' :  str(url)
			}
			#newDL = json.loads(newD)
			data[post_ID] = newD#L
			#print(data)
			json_file = open(subredditName+'.json','w')
			json.dump(data,json_file,indent = 4, sort_keys=True)
		print("============\n")
	if(parentFolder in os.getcwd() and parentFolder != os.getcwd().split('/')[-1]):
		os.chdir('..')
	elif(parentFolder not in os.getcwd()):
		print('ERROR WRONG FOLDER PATH DEBUG !!!')



parentFolder = 'Reddit-Stuff-Downloader'

_comments = False	# True to download comments


limitPostCount = 50
listSubreddits = 	[			# fill this list with subreddit names
			'Python',
			'learnpython',
			'ProgrammerHumor'

				]

def main():
	for subreddit_N in listSubreddits:
		getSubredditPosts(subreddit_N,limitPostCount,'hot')
		
main()




