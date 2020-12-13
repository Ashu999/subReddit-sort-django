from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from . import forms

#pip install praw
#pip install tabulate
import praw
from tabulate import tabulate

reddit = praw.Reddit(client_id="oybZZHDdE1EnYQ",
                     client_secret="eboZUU1BVG5Tpy1WAKiXDp7ECEVqjA",
                     user_agent="my user agent")


def sub_exists(sub):
    exist = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except:
        exist = False
    return exist


def redditSort(inpurStr):
    subreddit_list = set()
    for word in inpurStr.split():
        print(word)
        if not (sub_exists(word)):
            continue
        subreddit_list.add(word)
    print("sub list: ", subreddit_list)
    subreddit_subs = []
    for x in subreddit_list:
        subr = reddit.subreddit(x)
        subs = subr.subscribers
        subreddit_subs.append((x, format(subs, ',')))
    subreddit_subs.sort(key=lambda x: int(x[1].replace(',', '')), reverse=True)
    #print(subreddit_subs)

    output = tabulate(subreddit_subs, headers=['SubReddit', 'Subscribers'])
    return output


def index(request):
    form = forms.FormInput()
    if (request.method == 'POST'):
        form = forms.FormInput(request.POST)
        if (form.is_valid()):
            inp = form.cleaned_data['Input']
            print('Input: ' + inp)
            out = redditSort(inp)
            return render(request, 'index.html', {"form": form, 'OUT': out})
    return render(request, 'index.html', {"form": form})
