from odoo import models, fields, api
import urllib.request
import json

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        # Yeh function tab chalta hai jab Odoo mein Invoice "Confirm/Post" hoti hai
        res = super(AccountMove, self).action_post()
        
        for record in self:
            if record.move_type == 'out_invoice' and record.partner_id:
                raw_phone = record.partner_id.mobile or record.partner_id.phone
                if raw_phone:
                    clean_phone = "".join([c for c in str(raw_phone) if c.isdigit()])
                    if clean_phone:
                        # 5MinutesAPI Integration
                        api_key = self.env['ir.config_parameter'].sudo().get_param('fiveminutesapi.api_key', 'YOUR_DEFAULT_KEY')
                        
                        # Invoice Amount aur Number
                        inv_name = record.name or "Invoice"
                        amount = str(record.amount_total)
                        
                        payload = json.dumps({
                            "to": clean_phone,
                            "whatsapp_template": "new_invoice_alert" 
                        }).encode("utf-8")

                        req = urllib.request.Request(
                            "https://api.5minutesapi.com/v1/send-message",
                            data=payload,
                            headers={
                                "Authorization": f"Bearer {api_key}",
                                "Content-Type": "application/json"
                            },
                            method="POST"
                        )
                        try:
                            urllib.request.urlopen(req, timeout=5)
                        except Exception as e:
                            pass
        return res