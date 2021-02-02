from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from . import forms

#pip install praw
#pip install tabulate
import praw
from tabulate import tabulate

#env
import os
from dotenv import load_dotenv
project_folder = os.path.abspath('.')
load_dotenv(os.path.join(project_folder, '.env'))

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT)


def sub_exists(sub):
    exist = True
    try:
        reddit.subreddit(sub).subreddit_type
    except:
        exist = False
    return exist


def redditSort(inpurStr):
    subreddit_list = set()
    for word in inpurStr.split():
        #print(word)
        if not (sub_exists(word)):
            continue
        subreddit_list.add(word)
    #print("sub list: ", subreddit_list)
    subreddit_subs = []
    for x in subreddit_list:
        subr = reddit.subreddit(x)
        subs = subr.subscribers
        subreddit_subs.append((x, format(subs, ',')))
    subreddit_subs.sort(key=lambda x: int(x[1].replace(',', '')), reverse=True)
    #print(subreddit_subs)

    multi = ""
    for a in subreddit_subs:
        multi += a[0] + '+'
    #print(multi)

    output = tabulate(subreddit_subs, headers=[
        'SubReddit', 'Subscribers'
    ]) + "\n\n----Multi----\n" + multi

    return output


def index(request):
    form = forms.FormInput()
    if (request.method == 'POST'):
        form = forms.FormInput(request.POST)
        if (form.is_valid()):
            inp = form.cleaned_data['Input']
            #print('Input: ' + inp)
            out = redditSort(inp)
            return render(request, 'index.html', {"form": form, 'OUT': out})
    return render(request, 'index.html', {"form": form})
