# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from lck.django.common import remote_addr
from django.shortcuts import get_object_or_404

from ralph.discovery.models import DataCenter, Environment
from ralph.dnsedit.models import DHCPServer
from ralph.dnsedit.dhcp_conf import (
    generate_dhcp_config_entries,
    generate_dhcp_config_head,
    generate_dhcp_config_networks,
)
from ralph.ui.views.common import Base
from ralph.util import api


DHCP_DISABLE_NETWORKS_VALIDATION = getattr(
    settings, 'DHCP_DISABLE_NETWORKS_VALIDATION', False,
)


class Index(Base):
    template_name = 'dnsedit/index.html'
    section = 'dns'

    def __init__(self, *args, **kwargs):
        super(Index, self).__init__(*args, **kwargs)


def dhcp_synch(request):
    if not api.is_authenticated(request):
        return HttpResponseForbidden('API key required.')
    address = remote_addr(request)
    server = get_object_or_404(DHCPServer, ip=address)
    server.last_synchronized = datetime.datetime.now()
    server.save()
    return HttpResponse('OK', content_type='text/plain')


def dhcp_config_entries(request):
    if not api.is_authenticated(request):
        return HttpResponseForbidden('API key required.')
    dc_name = request.GET.get('dc', '')
    env_name = request.GET.get('env', '')
    if dc_name and env_name:
        return HttpResponseForbidden('Only DC or ENV mode available.')
    dc = None
    if dc_name:
        try:
            dc = DataCenter.objects.get(name__iexact=dc_name)
        except DataCenter.DoesNotExist:
            return HttpResponseNotFound(
                "Data Center `%s` does not exist." % dc_name
            )
    env = None
    if env_name:
        try:
            env = Environment.objects.get(name__iexact=env_name)
        except Environment.DoesNotExist:
            return HttpResponseNotFound(
                "Environment `%s` does not exist." % env_name
            )
    return HttpResponse(
        generate_dhcp_config_entries(
            dc=dc,
            env=env,
            disable_networks_validation=DHCP_DISABLE_NETWORKS_VALIDATION,
        ),
        content_type="text/plain",
    )


def dhcp_config_networks(request):
    if not api.is_authenticated(request):
        return HttpResponseForbidden('API key required.')
    dc_name = request.GET.get('dc', '')
    env_name = request.GET.get('env', '')
    if dc_name and env_name:
        return HttpResponseForbidden('Only DC or ENV mode available.')
    dc = None
    if dc_name:
        try:
            dc = DataCenter.objects.get(name__iexact=dc_name)
        except DataCenter.DoesNotExist:
            return HttpResponseNotFound(
                "Data Center `%s` does not exist." % dc_name
            )
    env = None
    if env_name:
        try:
            env = Environment.objects.get(name__iexact=env_name)
        except Environment.DoesNotExist:
            return HttpResponseNotFound(
                "Environment `%s` does not exist." % env_name
            )
    return HttpResponse(
        generate_dhcp_config_networks(
            dc=dc,
            env=env,
        ),
        content_type='text/plain',
    )


def dhcp_config_head(request):
    if not api.is_authenticated(request):
        return HttpResponseForbidden('API key required.')
    server_address = request.GET.get('server')
    if not server_address:
        server_address = remote_addr(request)
    dhcp_server = get_object_or_404(DHCPServer, ip=server_address)
    return HttpResponse(
        generate_dhcp_config_head(
            dhcp_server=dhcp_server,
        ),
        content_type='text/plain',
    )
