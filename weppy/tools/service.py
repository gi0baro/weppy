# -*- coding: utf-8 -*-
"""
    weppy.tools.service
    -------------------

    Provides the services handler.

    :copyright: (c) 2014 by Giovanni Barillari
    :license: BSD, see LICENSE for more details.
"""

from ..globals import response
from ..pipeline import Pipe
from ..serializers import Serializers


class ServicePipe(Pipe):
    def __init__(self, procedure):
        if not hasattr(self, procedure):
            raise RuntimeError(
                'weppy cannot handle the service you requested: %s' %
                procedure
            )
        self.procedure = getattr(self, procedure)
        self.json_encoder = Serializers.get_for('json')
        self.xml_encoder = Serializers.get_for('xml')

    async def json(self, f, **kwargs):
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        data = await f(**kwargs)
        return self.json_encoder(data)

    async def xml(self, f, **kwargs):
        response.headers['Content-Type'] = 'text/xml'
        data = await f(**kwargs)
        return self.xml_encoder(data)

    async def pipe(self, next_pipe, **kwargs):
        return await self.procedure(next_pipe, **kwargs)
