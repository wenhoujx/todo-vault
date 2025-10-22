from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
)
from constructs import Construct

class BackendStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        table = ddb.Table(
            self, "Todos",
            partition_key={"name": "id", "type": ddb.AttributeType.STRING}
        )

        fn = _lambda.Function(
            self, "TodoFn",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="app.handler",
            code=_lambda.Code.from_asset("server"),
            environment={"TABLE_NAME": table.table_name},
        )

        table.grant_read_write_data(fn)

        _lambda.FunctionUrl(
            self, "TodoUrl",
            function=fn,
            auth_type=_lambda.FunctionUrlAuthType.NONE,
        )
