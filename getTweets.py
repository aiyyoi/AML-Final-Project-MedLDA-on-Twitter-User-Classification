import tweepy
from random import randint
import time

auth = tweepy.OAuthHandler('1Y4Dv07ZtkvrGt9isPtoCKrrS', '4YjFTuY280BKoFmq6wDX0WoO0eCSEuDilRzZfXx8tWRLysZbjM')
auth.set_access_token('391259637-lUfQ9joo8tG3LGwfQqdJuCO4M6YwZ6RxhllAnrKZ', 'wr025ejM5EUVrOhmwB2zVOPpoU8Yl5npUtQIEUn8iN3Hx')

api = tweepy.API(auth)

# 3, ignore word list
ignore_list = open('ignore.list', 'r')
# 4, also check and ignore string.startswith('http://')
# 1, check and remove @ or # before or after string
punc=['@', '"', "'",'#', '.', ',', ':', '!','?',';','=','+','<','>','&', ' ', '(',')', '/', '~', '|']
# 2. tokens in middle of string to split one word in half
split=['&','-','_']
# 5 and ignore numbers that are not year

# For political orientation
# 30 Libertarian Users
libertarian= open('libertarian','r')
# Liberal Users
liberal= open('liberal','r')
# Conservative
conservative=open('conservative','r')
# Revolutionary
revolutionary=open('revolutionary', 'r')
# Progressive, 
progressive=open('progressive', 'r')
#Tea party, 
tea_party = open('teaparty', 'r')
#Independent&moderate, 
moderate=open('moderate', 'r')
#anarchist
anarchist= open('anarchist','r')
political = [libertarian, liberal, progressive, moderate, tea party, conservative, anarchist, revolutionary]
# Personal Interest
tech=open('tech','r')
sport=open('sport','r')
music=open('music','r')
gamer=open('gamer','r')
interest=[tech, sport, music, gamer]

def preProcessWords(description):
	pre_list=[]
	for word in description:
		# check front and back of each word
		if any(word[0] in s for s in punc):
			word = word[1:]
		if len(word)>1:
			if any(word[len(word)-1] in s for s in punc):
				word = word[:(len(word)-1)]
		if len(word)>2:
			if word.endswith("'s"):
				word = word[:(len(word)-2)]
			if word.endswith("'m"):
				word = word[:(len(word)-2)]
		# and separate words accordingly
		i=0
		for c in split:
			if c in word:
				sub_words = word.split(c)
				for each in sub_words:
					pre_list.append(each)
				i+=1
		if i==0:
			pre_list.append(word)
	return pre_list

def FormatData(words, train_dict, test_dict, s=0):
	#build dictionary
	for w in words:
		w=w.lower()
		if not (('http' in w) or (w in ignore_list) or w<str(1000)):
			if s==0:
				# write to both train & test
				if not train_dict.has_key(w):
					train_dict[w]= 1
				else:
					train_dict[w]+=1

				if not test_dict.has_key(w):
					test_dict[w]=1
				else:
					test_dict[w]+=1
			else:
				if s<6:
				# separate data 6/4 in train/test
					if not train_dict.has_key(w):
						train_dict[w]= 1
					else:
						train_dict[w]+=1
				else:
					if not test_dict.has_key(w):
						test_dict[w]=1
					else:
						test_dict[w]+=1

	return train_dict, test_dict

def UserGroupDict(train_dict, test_dict, overall_dict):
	for word in train_dict:
		if overall_dict.has_key(word):
			overall_dict[word]+=train_dict[word]
		else:
			overall_dict[word]=train_dict[word]

	for word in test_dict:
		if overall_dict.has_key(word):
			overall_dict[word]+=test_dict[word]
		else:
			overall_dict[word]=test_dict[word]
	return overall_dict

#overall word list of dictionaries
political_list=[]
interest_list=[]

f_train = open('interest.train','a')
f_test = open('interest.test', 'a')
#4/6 train/test
for label_id in range(len(interest)):
	overall_dict={}
	for user_id in range(len(interest[label_id])):
		time.sleep(15)
		print time.clock(), label_id, user_id
		train_dict={}
		test_dict={}
		profile = api.get_user(interest[label_id][user_id])
		# add to both test and train data
		description = profile.description.encode('utf-8').split()
		pre_list = preProcessWords(description)
		train_dict, test_dict = FormatData(pre_list, train_dict, test_dict, 0)
		# for each tweet
		public_tweets = api.user_timeline(screen_name=interest[label_id][user_id],count = 400)
		# print(description+" "+ user_id.location.encode('utf-8'))
		# randomly generate 1~10 to decide the train or test data the tweet go to
		# for each tweet, separate and analyze each word against 5 criterion
		for tweet in public_tweets:
			rand = randint(1,10)
			words = tweet.text.encode('utf-8').split()
			pre_list = preProcessWords(words)
			train_dict, test_dict = FormatData(pre_list, train_dict, test_dict, rand)

		f_train.write(str(label_id))
		f_test.write(str(label_id))
		for key in train_dict:
			nkey = key.replace(' ', '')
			nkey = nkey.replace(':', '')
			nkey = nkey.replace('.', '')
			nkey = nkey.replace(';', '')
			nkey = nkey.replace('?', '')
			nkey = nkey.replace('[', '')
			nkey = nkey.replace(']', '')
			if (train_dict[key]>1 and (len(nkey)>2 or nkey=='pc')):
				f_train.write(' '+nkey+':'+str(train_dict[key]))
		f_train.write('\n')

		for key in test_dict:
			nkey = key.replace(' ', '')
			nkey = nkey.replace(':', '')
			nkey = nkey.replace('.', '')
			nkey = nkey.replace(';', '')
			nkey = nkey.replace('?', '')
			nkey = nkey.replace('[', '')
			nkey = nkey.replace(']', '')
			if (test_dict[key]>1 and (len(nkey)>2 or nkey=='pc')):
				f_test.write(' '+nkey+':'+str(test_dict[key]))
		f_test.write('\n')
		overall_dict = UserGroupDict(train_dict, test_dict, overall_dict)

	interest_list.append(overall_dict)

f_train.close()
f_test.close()


f_list=open('interestlist.topic', 'a')
for each in interest_list:
	for item in sorted(each.items(), key=lambda x: (-x[1], x[0])):
		if item[1]>3:
			f_list.write(item[0]+':'+str(item[1])+' ')

	f_list.write('\n\n')		

f_list.close()



