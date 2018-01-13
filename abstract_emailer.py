#!/usr/bin/env python3

##
#
# An abstract a day keeps the ignorance at bay!
# Scrape random arXiv abstracts and send them over email.
#
# Author: Vince Kurtz
#
##

import requests
from bs4 import BeautifulSoup
import random
import smtplib
from email.mime.text import MIMEText

# Different pages we're interested in
fields = {
        "Robotics":"https://arxiv.org/list/cs.RO/pastweek?show=1000",  # set max per page to 1000
        "Artificial Intelligence":"https://arxiv.org/list/cs.AI/pastweek?show=1000",
        "Systems and Control" : "https://arxiv.org/list/cs.SY/pastweek?show=1000",
        "Multiagent Systems" : "https://arxiv.org/list/cs.MA/pastweek?show=1000",
        "Learning" : "https://arxiv.org/list/cs.LG/pastweek?show=1000",
        "Machine Learning" : "https://arxiv.org/list/stat.ML/pastweek?show=1000",
        "Computer Vision" : "https://arxiv.org/list/cs.CV/pastweek?show=1000",
        "Human Robot Interaction" : "https://arxiv.org/list/cs.HC/pastweek?show=1000",
        "Formal Languages and Automata Theory" : "https://arxiv.org/list/cs.FL/pastweek?show=1000",
}

def grab_a_paper(base_url):
    """
    Given an arXiv base url, grab a random paper from that URL
    """
    links = []
    titles = []
    papers = {}  # a dictionary of links and titles

    # Get webpage and initialize bs object
    r = requests.get(base_url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    # Get all the links
    for link in soup.find_all("a", title="Abstract"):
        links.append(link.get("href"))

    # Get all the titles
    for title in soup.find_all("div", class_="list-title mathjax"):
        titles.append(title.text.strip()[7:])  # take off "Title: " from beginning

    # Check that the lengths match
    if len(titles) != len(links):
        print("Uh oh, different number of titles than links. Parser must be broken")
        return 1

    # Compile the papers dictionary
    for i in range(len(links)):
        papers[links[i]] = titles[i]

    # now select one at random and return it!
    my_link, my_title = random.choice(list(papers.items()))

    return (my_link, my_title)

def get_all_articles():
    """
    Return a dictionary of a random article for each of the
    set fields.
    """
    my_articles = {}
    for name in fields:
        url = fields[name]
        link, title = grab_a_paper(url)
        full_link = "https://arxiv.org" + link

        my_articles[name] = [title, full_link]

    return my_articles

def get_abstract(url):
    """
    For the given url, grab the abstract and return it as
    a string. And also get the authors while you're at it.
    """

    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    abstract = soup.find("blockquote", class_="abstract mathjax").text[10:]
    authors = soup.find("div", class_="authors").text[9:]
    return (abstract, authors)

def format_message(article_dict):
    """
    From a dictionary of randomly selected articles, create and
    format a message string.
    """
    msg = ""
    for subject in article_dict:
        url = article_dict[subject][1]
        abstract, authors = get_abstract(url)

        msg = msg + "<h2>" + subject + "</h2>" 
        msg = msg + "\n<p>\n"
        msg = msg + "<b>" + article_dict[subject][0] + "</b>\n"     # title
        msg = msg + "\n<br></br>\n"
        msg = msg + "<i>" + authors + "</i>\n"
        msg = msg + "<blockquote>" + abstract
        msg = msg + "\n<br></br>\n"
        msg = msg + "\n<br></br>\n"
        msg = msg + url + "\n"   # link
        msg = msg + "</blockquote></p>\n\n"
    return msg


def send_email(message_text):
    from_line = "Your Daily Abstract Bot"
    to_line = "sendtoemail@domain.com"  ### EDIT THIS LINE ###
    subject_line = "Your Daily Abstract"

    msg = MIMEText(message_text, "html")
    msg["Subject"] = subject_line
    msg["To"] = to_line
    msg["From"] = from_line

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("sendfromemail@gmail.com", "myplaintextpassword")   ### EDIT THIS LINE ###
    server.sendmail(from_line, [to_line], msg.as_string())
    server.quit()


if __name__=="__main__":
    print("Scraping articles...")
    articles = get_all_articles()
    print("Formatting message...")
    message = format_message(articles)
    print("Sending email...")
    send_email(message)
    print("Done!")
