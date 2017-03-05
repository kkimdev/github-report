#!/usr/bin/env python3

import collections
import datetime
import types
import json
import getopt
import sys

# https://github.com/PyGithub/PyGithub
from github import Github

try:
    opts, args = getopt.getopt(sys.argv[1:], '', ["github-token="])
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

github_token = None
for opt, arg in opts:
    if opt == '--github-token':
        github_token = arg

g = None
if github_token is None:
    g = Github()
else:
    g = Github(github_token)

# TODO: Get repos from commandline?
repo = g.get_repo('m19g/www.m19g.com')

# Event type reference:
# https://developer.github.com/v3/activity/events/types/

def format_event(event):
    e = {}
    e['created_at'] = event.created_at.isoformat()
    e['type'] = event.type
    e['actor'] = event.actor.login

    if event.type == 'IssuesEvent':
        e['action'] = event.payload['action']
        e['title'] = event.payload['issue']['title']
        e['url'] = event.payload['issue']['html_url']
    elif event.type == 'IssueCommentEvent':
        e['action'] = event.payload['action']
        e['title'] = event.payload['issue']['title']
        e['url'] = event.payload['issue']['html_url']
    elif event.type == 'PullRequestEvent':
        e['action'] = event.payload['action']
        e['title'] = event.payload['pull_request']['title']
        e['url'] = event.payload['pull_request']['html_url']
    elif event.type == 'PullRequestReviewEvent':
        assert event.payload['action'] == 'submitted'
        e['action'] = event.payload['action']
        e['title'] = event.payload['pull_request']['title']
        e['url'] = event.payload['pull_request']['html_url']
    elif event.type == 'PullRequestReviewCommentEvent':
        e['action'] = event.payload['action']
        e['title'] = event.payload['pull_request']['title']
        e['url'] = event.payload['pull_request']['html_url']
    elif event.type == 'PushEvent':
        # TODO: pushing new commit to a pull request???
        pass
    else:
        # TODO:
        pass

    return e


data = [format_event(event) for event in repo.get_events()]

print(json.dumps(data, indent=2))
