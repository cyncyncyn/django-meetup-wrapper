# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
#from django.conf import settings
import json

MEETUP_KEY = None

class MeetupClient:
    def __init__(self):
        if not MEETUP_KEY:
            raise ValueError('MEETUP_KEY in meetup.py module is not set')
        self.key = MEETUP_KEY

    def get_response(self, group_urlname):
        from urllib.request import urlopen
        response = urlopen("https://api.meetup.com/2/events?key={}&group_urlname={}".format(self.key, group_urlname))
        return response

    def get_events(self, group_urlname):
        response = self.get_response(group_urlname)
        return json.loads(response.read().decode())
