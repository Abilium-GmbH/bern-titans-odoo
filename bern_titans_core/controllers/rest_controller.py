import odoo.http as http
from odoo.http import request
from datetime import date, timedelta
import logging

_logger = logging.getLogger(__name__)


class RestController(http.Controller):

    @http.route('/reset_password', type='json', auth="public")
    def reset_password(self, **kwargs):
        request.env['res.users'].sudo().reset_password(kwargs.get('login'))

    @http.route('/calendar/events/list/my', type='json', auth="user")
    def calendar_events_fetch_list_for_user(self, offset=0, limit=50, **kwargs):
        group_ids = request.env.user.partner_id.partner_group_ids.ids
        domain = [
            ('group_ids', 'in', group_ids),
            ('start', '>', date.today() - timedelta(days=2))
        ]
        calendar_events = request.env['calendar.event'].sudo()\
            .search_read(domain=domain,
                         fields=['id', 'name', 'allday', 'start', 'stop', 'partner_answers', 'attendees_count', 'group_ids'],
                         limit=limit,
                         offset=offset,
                         order='start asc')

        return self._populate_calendar_event_dict(calendar_events)

    def _populate_calendar_event_dict(self, calendar_events, with_details = False):
        partner_answers = request.env['partner.answer'].sudo()
        group_ids = request.env['partner.group'].sudo()
        for ce in calendar_events:
            ce['start'] = ce['start'].isoformat()
            ce['stop'] = ce['stop'].isoformat()
            if 'group_ids' in ce:
                groups = []
                for g in group_ids.browse(ce['group_ids']):
                    groups.append({'id': g.id, 'name': g.name, 'color': g.color_name})
                ce['groups'] = groups
            my_answer = None
            if with_details:
                attendees = partner_answers.browse(ce['partner_answers'])
                attendees_set = []
                undecided = request.env['res.partner'].sudo() \
                        .search(['&', ('partner_group_ids', 'in', ce['group_ids']),
                                 ('id', 'not in', attendees.partner_id.ids)])
                for un in undecided:
                    attendees_set.append({'name': un.name,
                                          'answer': None,
                                          'trikot_num': un.trikot_num,
                                          'position': un.position})
                for at in attendees:
                    if at.partner_id == request.env.user.partner_id:
                        my_answer = at.answer
                    attendees_set.append({'name': at.partner_id.name,
                                          'answer': at.answer,
                                          'trikot_num': at.partner_id.trikot_num,
                                          'position': at.partner_id.position})
                ce['partner_answers'] = attendees_set
            else:
                attendees = partner_answers.browse(ce['partner_answers'])
                for at in attendees:
                    if at.partner_id == request.env.user.partner_id:
                        my_answer = at.answer
            ce['my_answer'] = my_answer
        return calendar_events

    @http.route('/calendar/event/attend', type='json', auth="user")
    def calendar_event_attend(self, **kwargs):
        calendar_event = request.env['calendar.event'].sudo().browse(kwargs.get('eid'))
        partner_answers = request.env['partner.answer'].sudo().search(['&', ('calendar_event', '=', kwargs.get('eid')),
                                                                ('partner_id', '=', request.env.user.partner_id.id)])
        if len(partner_answers) == 1:
            partner_answers.write({'answer': kwargs.get('answer')})
        else:
            partner_answers.create({'partner_id': request.env.user.partner_id.id,
                                    'calendar_event': calendar_event.id,
                                    'answer': kwargs.get('answer')})

    @http.route('/calendar/event/get', type='json', auth="user")
    def calendar_event_get(self, **kwargs):
        group_ids = request.env.user.partner_id.partner_group_ids.ids
        calendar_event = request.env['calendar.event'].sudo()\
            .browse(kwargs.get('eid'))
        if len(set(calendar_event.group_ids.ids).intersection(group_ids)) > 0:
            return self._populate_calendar_event_dict(calendar_event[0].read(['id', 'name', 'allday', 'start', 'stop', 'partner_answers', 'attendees_count', 'location', 'description', 'group_ids']), True)[0]
        return None

    @http.route('/profile/update', type='json', auth="user")
    def update_user_profile(self, **kwargs):
        return request.env['res.partner'].browse(request.env.user.partner_id.id).sudo().write(kwargs.get('partner'))


# class Http(models.AbstractModel):
#     _inherit = 'ir.http'
#
#     def session_info(self):
#         session_info = super().session_info()
#         return self._add_session_id_to_session_info(session_info)
#
#     @api.model
#     def _add_session_id_to_session_info(self, session_info):
#         session_info['token'] = request.session.session_id
#         return session_info
#
# def get_response_inherit(self, httprequest, result, explicit_session):
#     if isinstance(result, Response) and result.is_qweb:
#         try:
#             result.flatten()
#         except Exception as e:
#             if request.db:
#                 result = request.registry['ir.http']._handle_exception(e)
#             else:
#                 raise
#
#     if isinstance(result, (bytes, str)):
#         response = Response(result, mimetype='text/html')
#     else:
#         response = result
#         self.set_csp(response)
#
#     save_session = (not request.endpoint) or request.endpoint.routing.get('save_session', True)
#     if not save_session:
#         return response
#
#     if httprequest.session.should_save:
#         if httprequest.session.rotate:
#             self.session_store.delete(httprequest.session)
#             httprequest.session.sid = self.session_store.generate_key()
#             if httprequest.session.uid:
#                 httprequest.session.session_token = security.compute_session_token(httprequest.session, request.env)
#             httprequest.session.modified = True
#         self.session_store.save(httprequest.session)
#     # We must not set the cookie if the session id was specified using a http header or a GET parameter.
#     # There are two reasons to this:
#     # - When using one of those two means we consider that we are overriding the cookie, which means creating a new
#     #   session on top of an already existing session and we don't want to create a mess with the 'normal' session
#     #   (the one using the cookie). That is a special feature of the Session Javascript class.
#     # - It could allow session fixation attacks.
#     if not explicit_session and hasattr(response, 'set_cookie'):
#         response.set_cookie(
#             'session_id', httprequest.session.sid, max_age=90 * 24 * 60 * 60, httponly=False)
#
#     return response
#
#
# #root.get_response = get_response_inherit
# root.get_response = types.MethodType(get_response_inherit, root)
#
