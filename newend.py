from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField

from wtforms import validators, ValidationError

class EndForm(Form):
   cep = TextField("cep",[validators.Required("Campo Requerido")])
   logradouro = TextAreaField("Address",[validators.Required("Campo Requerido")])
   inicio = IntegerField("inicio",[validators.Required("Campo Requerido")])
   fim = IntegerField("fim",[validators.Required("Campo Requerido")])
   latitude = TextField("latitude",[validators.Required("Campo Requerido")])
   longitude = TextField("longitude",[validators.Required("Campo Requerido")])
   submit = SubmitField("Send")