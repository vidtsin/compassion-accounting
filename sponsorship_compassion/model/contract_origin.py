# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: Emanuel Cino <ecino@compassion.ch>
#
#    The licence is in the file __openerp__.py
#
##############################################################################

from openerp.osv import orm, fields
from openerp.tools.translate import _


class contract_origin(orm.Model):
    """ Origin of a contract """
    _name = 'recurring.contract.origin'

    def _get_origin_types(self, cr, uid, context=None):
        return [
            ('ambassador', _("Ambassador")),
            ('sponsor', _("Contact with sponsor")),
            ('event', _("Event")),
            ('marketing', _("Marketing campaign")),
            ('sub', _("SUB sponsorship")),
            ('transfert', _("Transfert")),
            ('already_sponsor', _("Is already sponsor")),
            ('other', _("Other")),
        ]

    def _define_name(self, cr, uid, ids, field_name, args, context=None):
        """ Returns a good name for related fields. """
        res = {}
        if not isinstance(ids, list):
            ids = [ids]
        for origin in self.browse(cr, uid, ids, context):
            name = ""
            if origin.type in ('ambassador', 'sponsor'):
                name = origin.type + ' - ' + origin.partner_id.name
            elif origin.type in ('event', 'marketing'):
                name = origin.lead_id.name or origin.analytics_id.name
            elif origin.type == 'sub':
                name = 'SUB Sponsorship - ' + origin.contract_id.child_id.name
            elif origin.type == 'transfert':
                name = 'Transfert from ' + origin.country_id.name
            elif origin.type == 'already_sponsor':
                name = 'Was already a sponsor'
            elif origin.type == 'other':
                name = origin.other_name or 'Other...'
            res[origin.id] = name
        return res

    _columns = {
        'name': fields.function(_define_name, type="char", string=_("Name"), store=True),
        'type': fields.selection(_get_origin_types, _("Type"), help=_(
            "Origin of contract : "
            " * Ambassador : an ambassador made this new sponsorship"
            " * Contact with sponsor : an other sponsor told the person about"
            " Compassion."
            " * Event : sponsorship was made during an event"
            " * Marketing campaign : sponsorship was made after specific "
            "campaign (magazine, ad, etc..)"
            " * SUB sponsorship : new sponsorship to replace a finished one."
            " * Transfert : sponsorship transfered from another country."
            " * Is already sponsor : the sponsor wanted a new sponsorship."
            " * Other : select only if none other type matches."
            ), required=True),
        'partner_id': fields.many2one('res.partner', _("Partner")),
        'lead_id': fields.many2one('crm.lead', _("Event")),
        'analytics_id': fields.many2one('account.analytic.plan.instance',
                                        _("Analytic Distribution")),
        'contract_ids': fields.one2many('recurring.contract', 'origin_id', _("Contracts originated"), readonly=True),
        'contract_id': fields.many2one('recurring.contract', _("Previous sponsorship")),
        'country_id': fields.many2one('res.country', _("Country")),
        'other_name': fields.char(_("Give details"), size=128),
    }
    
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', _("You cannot have two origins with same name."
                                        "The origin does probably already exist."))
    ]
    
    