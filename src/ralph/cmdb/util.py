#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from bob.data_table import DataTableColumn

from ralph.cmdb.models import CI


def report_filters(cls, order, filters=None):
    if filters is False:
        return cls.objects.none()
    if filters:
        filters_list = filters.pop()
        return cls.objects.filter(**dict(filters_list)).order_by(order)
    return cls.objects.order_by(order).all()


def add_filter(request, ci=None):
    """Creates filters that can be used by report_filters method based on
    GET params from request.

    :param request: django request object
    :param ci: the CI to search for (None for all CIs)
    :return: the filters in a form of a [(field, value)] list or False if
        nothing should be found
    """
    filters = []
    if ci:
        filters.append({'ci': ci})
    if request.get('ci'):
        ci_id = CI.objects.select_related('id').filter(
            name=request.get('ci')
        )
        if ci_id:
            filters.append({'ci_id': ci_id[0]})
        else:   # CI not found
            return False

    if request.get('assignee'):
        filters.append({'assignee': request.get('assignee')})
    if request.get('jira_id'):
        filters.append({'jira_id': request.get('jira_id')})
    if request.get('issue_type'):
        filters.append({'issue_type': request.get('issue_type')})
    if request.get('status'):
        filters.append({'status': request.get('status')})
    if request.get('start_update') and request.get('end_update'):
        filters.append(
            {'update_date__lte': request.get('start_update')}
        )
        filters.append(
            {'update_date__gte': request.get('end_update')}
        )
    if request.get('start_resolved') and request.get('end_resolved'):
        filters.append(
            {'resolvet_date__lte': request.get('start_resolved')}
        )
        filters.append(
            {'resolvet_date__gte': request.get('end_resolved')}
        )
    if request.get('start_planned_start') and request.get('end_planned_start'):
        filters.append(
            {'planned_start_date__lte': request.get('start_planned_start')}
        )
        filters.append(
            {'planned_start_date__gte': request.get('end_planned_start')}
        )
    if request.get('start_planned_end') and request.get('end_planned_end'):
        filters.append(
            {'planned_end_date__lte': request.get('start_planned_end')}
        )
        filters.append(
            {'planned_end_date__gte': request.get('start_planned_end')}
        )
    return filters


def table_colums():
    _ = DataTableColumn
    columns = [
        _(
            'Issue updated',
            field='update_date',
            sort_expression='update_date',
            bob_tag=True,
        ),
        _(
            'Type',
            field='issue_type',
            sort_expression='issue_type',
            bob_tag=True,

        ),
        _(
            'Status',
            field='resolvet_date',
            sort_expression='resolvet_date',
            bob_tag=True,
        ),
        _(
            'Ci',
            field='ci',
            sort_expression='ci',
            bob_tag=True,
        ),
        _(
            'Summary',
            field='summary',
            bob_tag=True,
        ),
        _(
            'Assignee',
            field='assignee',
            bob_tag=True,
        ),
        _(
            'Description',
            field='description',
            bob_tag=True,
        ),
        _(
            'Analysis',
            field='analysis',
            bob_tag=True,
        ),
        _(
            'Problems',
            field='problems',
            bob_tag=True,
        ),
        _(
            'Planed start',
            field='planned_start_date',
            sort_expression='planned_start_date',
            bob_tag=True,
        ),
        _(
            'Planed end',
            field='planned_end_date',
            sort_expression='planned_end_date',
            bob_tag=True,
        ),
    ]
    return columns
