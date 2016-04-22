# FunWithPython
Some fun little python scripts we've written to do various things. Started with inspiration from https://automatetheboringstuff.com/

###*The scripts so far...*

+ ####**magicscraper.py**  
  *Author: Sean*

  Web scraper that iterates through all of the current Magic the Gathering fiction published by Wizards, sends the webpages to http://fivefilters.org/pdf-newspaper/ to be formatted into a pretty and reader friendly pdf, and then saves them onto your hard drive with appropriate titles and directory organization.

+ ####**yobomb.py**
  *Author: Sean*

  Ever want to piss off your friends, family, co-workers, 
strangers whose Yo username you just so happen to have?
  yobomb.py is the answer. Yo bomb sends a designated amount of 
Yos to some poor schmuck periodically after a designated interval of 
  time has passed. 
  An API key is required and must be inserted into the code (I think it should be obvious where)
  One can get said API key at https://dev.justyo.co/
  ```
  Usage:
    yobomb.py target [iterations] [interval]

  Arguments:
    target:	your "friend's" Yo username (no caps required)
    iterations (optional):		the total number of Yos to send (default: 100)
    interval (optional):		interval in seconds between the sending of each Yo (default: 1)
  
  ```
  
+ ####**push20.py**
  *Author: Chris*

  CLI-based script that uses Pushbullet's API https://docs.pushbullet.com/ to create and send
  pushes of dice rolls in a simplified dice notation to either yourself, or a specified email.
  All you need is a Pushbullet API Token, which can be acquired from https://www.pushbullet.com/#settings/account
  ```
  Usage:
    push20.py [email] [dice]

  Arguments:
    email:	standard email@something.com format
    dice:		standard [N]dX+K, where N is number of dice, X is number of faces of the dice
  		+ is the operator (+, -, *|x, /) accepted, K is the factor to operate on 
  
  ```
  
+ ####**hackerscraper.py**
  *Author: Chris*
  
  Basic script that prints the title of the top article and a specified number of top-level comments
  from HackerNews to the screen. Uses HackerNews' firebase API. Not very impressive; a full-fledged
  CLI browser was found a couple of days after I started this.
  ```
  Usage:
  hackerscraper.py [numcomments]

  Argument(s):

    numcomments: number of top comments to load.

  ```
  
+ ####**wikiGraph.py**
  *Author: Chris*
  
  Visualizer for Wikipedia article connections. Uses MediaWiki's api to retrieve the markdown for a
  specified article, then parses all the links in the first section of that article, and those articles'
  first section links. Then, uses networkx to draw the graph. Used as a jumping-off point for a future
  offline mobile Wikipedia browser.
  ```
  Usage:
  wikiGraph.py articleName
  
  Argument:
	
	articleName: name of article to query. use quotation marks for articles with spaces.

  ```
