import json

from regopy import Interpreter

from app.config import settings
from app.schemas.opa import OpaInput



def query(input: OpaInput):
    rego = Interpreter()
    rego.add_module("btlr", settings.BLTR_POLICY)
    rego.set_input(input.model_dump())
    return json.loads(str(rego.query("data.btlr")))
