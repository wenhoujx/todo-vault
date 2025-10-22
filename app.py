#!/usr/bin/env python3
import aws_cdk as cdk
from infra.backend_stack import FlaskStack

app = cdk.App()
FlaskStack(app, "FlaskStack")
app.synth()
