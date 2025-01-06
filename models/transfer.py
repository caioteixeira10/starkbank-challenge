from flask_restx import fields
from server import api 

rule_model = api.model('Rule', {
    'key': fields.String(),
    'value': fields.Integer()
})

transfer = api.model('Transfer', {
    'amount': fields.Integer(required=True),
    'tax_id': fields.String(required=True),
    'name': fields.String(required=True),
    'bank_code': fields.String(required=True),
    'branch_code': fields.String(required=True),
    'account_number': fields.String(required=True),
    'external_id': fields.String(),
    'scheduled': fields.DateTime(),
    'tags': fields.List(fields.String()),
    'rules': fields.List(fields.Nested(rule_model))        
})