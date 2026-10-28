from odoo import models, fields, api
import urllib.request
import json
import random

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        record = super(ResPartner, self).create(vals)
        raw_phone = record.mobile or record.phone
        if raw_phone:
            clean_phone = "".join([c for c in str(raw_phone) if c.isdigit()])
            if clean_phone:
                # Get API Key from Odoo Settings (System Parameters)
                api_key = self.env['ir.config_parameter'].sudo().get_param('fiveminutesapi.api_key', 'YOUR_DEFAULT_KEY')
                otp_code = str(random.randint(100000, 999999))
                
                payload = json.dumps({
                    "to": clean_phone,
                    "code": otp_code
                }).encode("utf-8")

                req = urllib.request.Request(
                    "https://api.5minutesapi.com/v1/send-otp",
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
        return record