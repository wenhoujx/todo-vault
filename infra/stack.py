from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
)

from constructs import Construct


class FullStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        table = ddb.Table(
            self,
            "Todos",
            partition_key={"name": "id", "type": ddb.AttributeType.STRING},
        )

        fn = _lambda.Function(
            self,
            "TodoFn",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.handler",
            code=_lambda.Code.from_asset("server"),
            environment={"TABLE_NAME": table.table_name},
        )

        table.grant_read_write_data(fn)

        _lambda.FunctionUrl(
            self,
            "TodoUrl",
            function=fn,
            auth_type=_lambda.FunctionUrlAuthType.NONE,
        )
        bucket = s3.Bucket(
            self,
            "FrontendBucket",
            website_index_document="index.html",
            website_error_document="index.html",
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            ),
        )

        s3deploy.BucketDeployment(
            self,
            "DeployWebsite",
            sources=[s3deploy.Source.asset("dist")],
            destination_bucket=bucket,
        )

        from aws_cdk import CfnOutput

        CfnOutput(self, "WebsiteURL", value=bucket.bucket_website_url)
