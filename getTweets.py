import tweepy
from random import randint
import time

auth = tweepy.OAuthHandler('1Y4Dv07ZtkvrGt9isPtoCKrrS', '4YjFTuY280BKoFmq6wDX0WoO0eCSEuDilRzZfXx8tWRLysZbjM')
auth.set_access_token('391259637-lUfQ9joo8tG3LGwfQqdJuCO4M6YwZ6RxhllAnrKZ', 'wr025ejM5EUVrOhmwB2zVOPpoU8Yl5npUtQIEUn8iN3Hx')

api = tweepy.API(auth)

# 3, ignore word list
ignore_list = ['','uh','oh','and','or', 'for', 'a', 'I', 'u','you','them','we','they','their', 'is', 'lt','go', 'are', 'of', 'at', 'with', 'in', 'out', 'to', 'RT', 'this', 'that', 'there', 'the', 'it', 'into', 'these','those','then', 'than', 'am','pm','et', 'ct','pt','as', 'hey','w/','w/o']
# 4, also check and ignore string.startswith('http://')
# 1, check and remove @ or # before or after string
punc=['@', '"', "'",'#', '.', ',', ':', '!','?',';','=','+','<','>','&', ' ', '(',')', '/', '~', '|']
# 2. tokens in middle of string to split one word in half
split=['&','-','_']
# 5 and ignore numbers that are not year

# For political orientation
# 30 Libertarian Users
libertarian=['stephengordon', 'TopLibertarian', 'LPNational', 'libertyideals', 'SlavLibertarian', 'RobertDButler2', 'robertmeyer9', 'LibertyIsNow', 'freedompolitics', 'LibertarianView', 'A_Liberty_Rebel', 'libstandard', 'jfktruther', 'LibertariansFor', 'libertarianJ', 'TheLibRepublic', 'NM_libertarian', 'LPIN', 'Libertarian_New', 'LPTexas', 'JulieBorowski', 'thornecassidy', 'RobMcNealy', 'HellFogg', 'LibertarianCiti', 'solmc', 'RonPaul_2012', 'normanhorn', 'karldickey', 'dmataconis']
# Liberal Users
liberal=['LiberalsAreCool', 'LiberalAus', 'LibDems', 'liberal_party', 'BeingLiberal','LiberalPhenom','LiberalCap', 'LiberalTucker','michlib','tomwatson', 'thinkprogress','theprospect', 'SuzyKhimm','JeffreyFeldman', 'Wolfrum','benjaminspector','proudlib', 'mercerstine','LibManifest','realLibs','marpiwill','Politics_PR','XtinaDavidson','GodlessLiberals','MuggleBornNY','SoapboxLiberal','WiseLiberal','mattdawidowicz','keystonepol','politicususa']
# Conservative
conservative=['paulbenedict7', 'gopleader','rightwingnews','anna12061', 'Conservatives', 'YoungCons', 'CPC_HQ', 'GOHConservative', 'TeaPartyCat', 'CR', 'ConNewsNow', 'NYConsMom', 'SCF', 'GOPLADYAMY', 'jdigg78', 'ConservativeQuo', 'MrConservative_','CICMedia', 'teaparty321', 'PatriotTweetz', 'rightcuban', 'ConservativeMag', 'ConservLatina', 'BlacksFund', 'conserv_tribune', 'liberaltreason', 'Steelpolynbrass', 'Eggoverlight', 'MadCityCon', 'conking', 'cnsnews']
# Revolutionary
revolutionary=['therrevolution','BootsRiley', 'MarxProject', 'soulrebelJ', 'tweetmarx', 'QuoteRevolution','chiume', 'USRevolutionWar', 'RYA_Punjab', 'aroydee', 'RevolutnryMedia', 'SpringfieldFree', 'radicaldaily', 'Rosa__Luxemburg', 'RevolutionChan', 'NjabuloCB', 'Richard_P_Smith', 'RadicalProverbs', 'ykhong', 'HoCHlminh', 'RevolutionaryPo', 'EricSaenz4', 'RevolutionsLaws','RadicalBooks', 'blankstudent', 'MrLewis915']
# Progressive, 
progressive=['thinkprogress', 'thenation', 'chrislhayes', 'dailykos', 'alternet', 'AFLCIO', 'BoldProgressive', 'DrDigiPol', 'GottaLaff', 'TPElections', 'theprogressive', 'keithellison', 'allisonkilkenny', 'BobFertik', 'ProgressivePam', 'maddow', 'ProgressMich', 'ProgressOnline', 'NYWFP', 'WhiteHouse', 'ProgressNowCO', 'greenparty_ie', 'jricole', 'gaycivilrights', 'kwcollins','NewRoosevelt', 'JoeWalshDC', 'carlsciortino', 'rosswallen', 'ManhattanGreens']
#Tea party, 
tea_party = ['TPPatriots','michaeljohns', 'TeaPartyExpress', 'TeaPartyOrg', 'TheTeaParty_net', 'TeaPartyNevada', 'teapartynation', 'TeaParty365', 'teapartynews', 'jennybethm', 'TeaPartyPatriot', 'RenoTeaParty', 'TeaParty_Leader', 'nogirlemen', 'teapartytown', 'TeaPartyReport', 'HoustonTeaParty', 'TeaPartyDeanie', 'TeaPartyArmy', 'EValleyTeaParty', 'TeaPartyRepubs', 'TeaPartyPolice', 'Tea_Party_Now', 'TeaPartyAllies1', 'tylerteaparty', 'BCSTeaParty', 'TeaPartyJane', 'dsmteaparty', 'TeaPartyUSA41', 'TeaParty4Perry']
#Independent&moderate, 
moderate=['CortneyTippery', 'BruceThompson51', 'Emperor_Bob', 'CassoforCO', 'DavisPaine', 'JerryLeeGP', '_politics_', 'reasonablymod', 'mjwstickings', 'bspence5', 'CLTmathMOM', 'iamrc10', 'Salon_Politics', 'Newsmax_Media', 'ShiftingGrounds', 'thenewpolitical','14democracy', 'bamagirl0117', 'Politicolnews', 'TheIndyExpress', 'GIS_Info', 'NoLabelCentrist', 'FedUpPolitics', 'FactChek', 'Indie_Voters', 'MStrawPSU']
#anarchist
anarchist=['anarchists', 'anarchistwriter', 'OccupyWallSt', 'AfedEdinburgh', 'SwindonAnarchos', 'ODANARCHISTS', 'AnarchistLens', 'AnarchistBH', 'Anarchists4Life', 'OpWallStreet', 'AnarchistFed', 'AnarchistNews', 'PriyaWarcry', 'OccupyWallStNYC']

political = [libertarian, liberal, conservative, revolutionary, progressive, tea_party, moderate, anarchist]
# Personal Interest
tech=['techcrunch', 'google', 'timoreilly', 'leolaporte', 'Scobleizer', 'jeffpulver', 'PCMag', 'digiphile', 'mikebutcher', 'technology', 'nytimestech', 'CAinc', 'fttechnews', 'TEDchris', 'BBCTech', 'TelegraphTech', 'GlobeTechnology', 'AccentureTech', 'MedNetTech', 'SteveLohr', 'TechnologyGeek', 'AFRtechnology', 'PostTechNews', 'griffintech', 'ZebraTechnology', 'technologybuzz', 'SalonTechnology', 'WSJdigits', 'WIRED', 'us_technology', 'physorg_tech']
sport=['espn', 'NYTSports', 'SHAQ', 'AdamSchefter', 'darrenrovell', 'SportsCenter', 'SInow', 'CBSSportsGang', 'nfl', 'BuzzFeedSports', 'WSJSports', 'CNBCSportsBiz', 'MSGSportsNYC', 'NBCSports', 'SkySportsNewsHQ', 'FOXSports', 'guardian_sport', '5liveSport', 'YahooSports', 'EliasSports', 'BBCSport', 'ChrisWragge', 'IndoSport', 'FirstpostSports', 'TelegraphSport', 'CBSSportsNet', 'SkySportsNFL', 'SkySportsFL', 'FSSouthwest', 'NFLonFOX', 'NewsdaySports']
music=['musicindustry54', 'musicindustrypr', 'SimplySFans', 'ReverbNation', 'hypebot', 'ArtistReach', 'MusicDreamer', 'womeninmusicorg', 'metalinsider', 'EINMusicNews', 'MusicWeek', 'MusicInd_News', 'LA_Music_Pros', 'agentofchangeNY', 'MusicInd2day', 'THR_EarShot', 'MusicIndConnect', 'music_industry2', 'MusicLinkUp', 'MusicForRelief', 'UK_Music', 'themusicnetwork', 'billboard', 'CLGMusicMedia', 'SPINmagazine', 'BleepBot']
gamer=['PlayStation', 'IGN', 'AskPlayStation', 'OPM_UK', 'VideoGamerCom', 'VideoGameWeekly', 'gamespot', 'VideoGamerRob', 'Kotaku', 'RockstarGames', 'L337Lauren', 'GP_Video_Games', 'Xbox', 'MVGworld', 'joystiq', 'gamespot', 'TheAvgGamer', 'VidGame_Blog', 'gamesandtrailer', 'VideoGaming_Hub', 'GamingDecoded', 'GamingRats', 'jwhdavison', 'justvideogames', 'GamerSpy1', 'gameinformer']

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
#4/6 test/train
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



