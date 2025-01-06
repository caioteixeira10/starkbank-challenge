from flask_restx import fields
from server import api

rule_model = api.model('Rule', {
    'key': fields.String(),
    'value': fields.List(fields.String())
})

splits_model = api.model('splits', {
    'receiverId': fields.String(),
    'amount': fields.Integer()
})

discounts_model = api.model('discounts', {
    'percentage': fields.Float(),
    'due': fields.DateTime()
})

description_model = api.model('discounts', {
    'key': fields.String(),
    'value': fields.String()
})

invoice = api.model('Invoice', {
    'amount': fields.Integer(required=True),
    'tax_id': fields.String(required=True),
    'name': fields.String(required=True),
    'due': fields.DateTime(),
    'fine': fields.Float(default=2.0),
    'interest': fields.Float(default=1.0),
    'expiration': fields.String(),
    'splits': fields.List(fields.Nested(splits_model)),
    'discounts': fields.List(fields.Nested(discounts_model)),
    'descriptions': fields.List(fields.Nested(description_model)),
    'tags': fields.List(fields.String()),
    'rules': fields.List(fields.Nested(rule_model))        
})

