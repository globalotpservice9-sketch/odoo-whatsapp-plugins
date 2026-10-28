from odoo import models, fields, api
import urllib.request
import json

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def create_from_ui(self, orders, draft=False):
        # Jab POS par receipt generate hogi, yeh function chalega
        res = super(PosOrder, self).create_from_ui(orders, draft=draft)
        for order in res:
            pos_order = self.browse(order['id'])
            if pos_order.partner_id:
                raw_phone = pos_order.partner_id.mobile or pos_order.partner_id.phone
                if raw_phone:
                    clean_phone = "".join([c for c in str(raw_phone) if c.isdigit()])
                    if clean_phone:
                        api_key = self.env['ir.config_parameter'].sudo().get_param('fiveminutesapi.api_key', 'YOUR_KEY')
                        payload = json.dumps({
                            "to": clean_phone,
                            "whatsapp_template": "pos_receipt"
                        }).encode("utf-8")
                        req = urllib.request.Request(
                            "https://api.5minutesapi.com/v1/send-message",
                            data=payload,
                            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                            method="POST"
                        )
                        try:
                            urllib.request.urlopen(req, timeout=5)
                        except:
                            pass
        return res