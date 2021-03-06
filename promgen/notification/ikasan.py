# Copyright (c) 2017 LINE Corporation
# These sources are released under the terms of the MIT license: see LICENSE

import logging

from django import forms
from django.template.loader import render_to_string

from promgen import util
from promgen.notification import NotificationBase

logger = logging.getLogger(__name__)


class FormIkasan(forms.Form):
    value = forms.CharField(
        required=True,
        label='Channel'
    )
    alias = forms.CharField(
        required=False,
        help_text='Used to hide chanel from being shown'
    )


class NotificationIkasan(NotificationBase):
    '''
    Send messages to Hipchat using Ikasan Hipchat bridge

    https://github.com/studio3104/ikasan
    '''

    form = FormIkasan

    def _send(self, channel, data):
        url = self.config('server')

        params = {
            'channel': channel,
            'message_format': 'text',
        }

        if data['status'] == 'resolved':
            params['color'] = 'green'
            params['message'] = render_to_string('promgen/sender/ikasan.resolved.txt', data).strip()
        else:
            params['color'] = 'red'
            params['message'] = render_to_string('promgen/sender/ikasan.body.txt', data).strip()

        util.post(url, params)
        return True
