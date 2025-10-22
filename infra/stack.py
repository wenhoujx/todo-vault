from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
)
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_s3_deployment as s3deploy
import aws_cdk.aws_cloudfront as cloudfront
import aws_cdk.aws_cloudfront_origins as origins

from constructs import Construct

class FullStack(Stack):
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
        # deploy FE 
        bucket = s3.Bucket(self, "FrontendBucket",
                website_index_document="index.html",
                public_read_access=True
            )

        distribution = cloudfront.Distribution(self, "FrontendDist",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(bucket)
            ),
            default_root_object="index.html"
        )

        s3deploy.BucketDeployment(self, "DeployFrontend",
            sources=[s3deploy.Source.asset("../dist")],
            destination_bucket=bucket,
            distribution=distribution,
            distribution_paths=["/*"]
        )
