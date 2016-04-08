# FunWithPython
Some fun little python scripts We've written to do various things. Started with inspiration from https://automatetheboringstuff.com/

###*The scripts so far...*

+ ####**magicscraper.py**  
  *Author: Sean*

  Web scraper that iterates through all of the current Magic the Gathering fiction published by Wizards, sends the webpages to http://fivefilters.org/pdf-newspaper/ to be formatted into a pretty and reader friendly pdf, and then saves them onto your hard drive with appropriate titles and directory organization.

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