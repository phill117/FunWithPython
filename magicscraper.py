#!/usr/bin/python3

import requests, bs4, urllib.parse, os, re

# TODO make target directory an optional argument
# TODO only get latest articles (dont redownload on rerun)

# create a folder in working directory
path = './MTGArticles'
if not os.path.exists(path):
    os.makedirs(path)

# Request the MTG article archive page
res = requests.get('http://magic.wizards.com/en/articles/columns/magic-story-archive')

res.raise_for_status()

storyPageSoup = bs4.BeautifulSoup(res.text, "html.parser")

# Gather the newer stories (Battle for Zendikar forward)

specialSections = storyPageSoup.select('#content > div > div > .slides > div > .container > .content')

for specialSection in specialSections:
	
	# extract the title and link for the folder and card-set page
	specialTitle = specialSection.select('.header > h3')
	specialLink = specialSection.select('p > a')

	# make a directory for each story arc
	path = './MTGArticles/'+specialTitle[0].text
	if not os.path.exists(path): os.makedirs(path)

	# request the corresponding card-set page
	spec = requests.get(specialLink[0].get('href'))
	spec.raise_for_status()

	specPageSoup = bs4.BeautifulSoup(spec.text, "html.parser")
	specArticles = specPageSoup.select('#magic-story > ul > li')

	for specArticle in specArticles:

		# extract the title and link for each article
		specTitle = specArticle.select('.item > .item-content > h3 > span')
		specLink = specArticle.select('.item > .item-content > .details > .description > p > a')
		
		# stop if you hit an article that hasnt been written yet.
		if len(specLink) == 0: continue

		# encode the url
		encodedSpecUrl = urllib.parse.quote_plus(specLink[0].get('href'))
		print(encodedSpecUrl)

		# get the newspaper from fivefilters.org
		pdfdata = requests.get('http://pdf.fivefilters.org/makepdf.php?mode=single-story&images=1&url=' + encodedSpecUrl)

		# strip out none alphanumeric characters
		filename = re.sub(r'\W+', '', specTitle[0].text)+'.pdf'

		# write the file to the hard drive
		pdf = open(os.path.join(path, filename), 'wb')
		for chunk in pdfdata.iter_content(100000):
			pdf.write(chunk)
		pdf.close()

# Gather the articles from all of the older sections (the ones that are just presented in a grid form)

sections = storyPageSoup.select('#content > .header_curated_articles')

boxArticles = storyPageSoup.select('.section_articles > .articles-bloc > .article > .wrap > .details > .cat')
boxTitles = storyPageSoup.select('.section_articles > .articles-bloc > .article > .wrap > .details > .title')

for section in sections:
	sectionTitle = section.select('h2 > span')[0].text
	articles = section.select('.section_articles > .articles-bloc > .article > .wrap > .details > .cat')
	titles = section.select('.section_articles > .articles-bloc > .article > .wrap > .details > .title')
	for i in range(0, len(articles)):

		place = len(articles) - i

		article = articles[i]
		title = titles[i]

		# strip out none alphanumeric characters
		newTitle = re.sub(r'\W+', '', title.text)

		# encode the url
		link = article.get('href')
		encodedUrl = urllib.parse.quote_plus('http://magic.wizards.com'+link)
		print(encodedUrl)

		# get the newspaper from fivefilters.org
		pdfdata = requests.get('http://pdf.fivefilters.org/makepdf.php?mode=single-story&images=1&url=' + encodedUrl)
		
		filename = sectionTitle+'_'+str(place)+'_'+newTitle+'.pdf'

		# write the file to the hard drive
		pdf = open(os.path.join(path, filename), 'wb')
		for chunk in pdfdata.iter_content(100000):
			pdf.write(chunk)
		pdf.close()
