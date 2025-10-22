#!/usr/bin/env python3
import aws_cdk as cdk
from infra.stack import FullStack

app = cdk.App()
FullStack(app, "BackendStack")
app.synth()
