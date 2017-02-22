__author__ = 'user'
import requests
from bs4 import BeautifulSoup
import re
import os.path

def main():
    web_sites = []
    get_web_sites(web_sites)
    if not os.path.isfile('sports.txt'):
        sports_names = get_sports_names()
    else:
        sports_names = get_sports_names_file()
    for i in range(0,len(web_sites)):
        print web_sites[i]," -  ",
        file_output.write(web_sites[i] + " - ")
        f=0
        html_source = requests.get(web_sites[i])
        soup = BeautifulSoup(html_source.content,"html.parser")
        if len(soup.title.text)>0:
            f = check_sport(sports_names,soup.title.text)

        if f==0:
            meta_content = re.findall('<meta name="description" content="(.+?)".+?',html_source.content)
            if not meta_content:
                f = check_sport(sports_names,html_source.content)
            else:
                f = check_sport(sports_names,meta_content[0])

        if f==0:
            print "NA"
            file_output.write("NA\n")


def check_sport(sports_names,regex):
    for j in range(0,len(sports_names)):
        name = sports_names[j]
        if re.search(r"\b{}\b".format(name),regex,flags=re.IGNORECASE):
            print sports_names[j]
            file_output.write(sports_names[j] + "\n")
            return 1

    return 0

def get_sports_names_file():
    file = open('sports.txt','r')
    sports_names = []
    sports_names = file.read().splitlines()
    return sports_names


def get_sports_names():
    html = requests.get('http://www.askaboutsports.com/about/by-name.htm')
    soup = BeautifulSoup(html.content,"html.parser")
    file = open('sports.txt','w')
    list = []
    sports_names = []
    for l in soup.find_all('a'):
        list.append(l)

    for i in range(0,len(list)):
        if re.match('<a href="/.+?/">',str(list[i])):
            if '(duplicate?)' in str(list[i]):
                name_1 = re.findall('<a href="/(.+?)/">',str(list[i]))
                sports_names.append(str(name_1[0]))
            else:
                name_1= re.findall('<a href="/(.+?)/">',str(list[i]))
                name_2= re.findall('<a href="/.+?/">\n(.+?)</a>',str(list[i]))
                if len(name_1[0])==len(name_2[0]):
                    sports_names.append(str(name_2[0]))

    sports_names = remove_useless_sports(sports_names)
    sports_names = add_some_sports(sports_names)
    for i in range(0,len(sports_names)):
        file.write(sports_names[i]+"\n")
    return sports_names


def get_web_sites(web_sites):
    file_name = raw_input("Enter File Name -\n")
    f = open(file_name,'r')
    for site_name in f:
        if 'http' not in site_name:
            site_name = 'http://' + site_name
        web_sites.append(site_name.strip())


def remove_useless_sports(sports_names):
    sports_names.remove('Yoga')
    sports_names.remove('Running')
    sports_names.remove('Bridge')
    sports_names.remove('Gambling')
    sports_names.remove('Athletics')
    sports_names.remove('Backpacking')
    sports_names.remove('Board Games')
    sports_names.remove('Bird Watching')
    return sports_names

def add_some_sports(sports_names):
    sports_names.append('Skating')
    sports_names.append('Hockey')
    sports_names.append('American Football')
    sports_names.append('Taekwondo')
    sports_names.append('Polo')
    sports_names.append('Martial art')
    return sports_names

file_output = open('output.txt','w')
main()
file_output.close()







