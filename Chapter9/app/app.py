#!/usr/bin/env python3

from aws_cdk import core
from app.core_stack import CoreStack
from app.web_stack import WebStack
from app.rds_stack import RdsStack


app = core.App()
core = CoreStack(app, "core")
web = WebStack(app, "web", vpc=core.vpc)
rds = RdsStack(app, "rds", vpc=core.vpc, webserver_sg=web.webserver_sg)
app.synth()
