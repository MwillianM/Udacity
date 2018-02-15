import quiz_3 as q3

answers=[]

#How many bands named "first aid kit"?
query=q3.query_by_name(q3.ARTIST_URL, q3.query_type["simple"], "first aid kit")
artists=[a["name"] for a in query["artists"]]
a1=0
for a in artists:
	if a.lower() == "first aid kit":
		a1+=1

print("There are", a1, "artists named first aid kit")
answers.append(a1)

#Begin_area name for Queen?
query=q3.query_by_name(q3.ARTIST_URL, q3.query_type["simple"], "Queen")
artists=[a for a in query["artists"] if a["name"] == "Queen"]
for a in artists:
	try:
		a["begin-area"]["name"]
		a2=a["begin-area"]["name"]
	except:
		print("")

answers.append(a2)

#Spanish alias for Beatles?
query=q3.query_by_name(q3.ARTIST_URL, q3.query_type["simple"], "Beatles")
for a in query["artists"]:
	if a["name"] == "The Beatles":
		for al in a["aliases"]:
			if al["locale"] == "es":
				al["name"]
				a3=al["name"]

answers.append(a3)

#Nirvana disambiguation?
query=q3.query_by_name(q3.ARTIST_URL, q3.query_type["simple"], "Nirvana")
artists=[json.dumps(a) for a in query["artists"] if a["name"] == "Nirvana"]
for a in artists:
	if 'kurt cobain' in a:
		json.loads(a)["disambiguation"]
		a4=json.loads(a)["disambiguation"]

answers.append(a4)

#When was One Direction formed?
query=q3.query_by_name(q3.ARTIST_URL, q3.query_type["simple"], "One Direction")
for a in query["artists"]:
	if a["name"] == "One Direction":
		a["life-span"]["begin"][:4]
		a5=a["life-span"]["begin"][:4]

answers.append(a5)

#Answers
print(answers)
