from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    # aws_lambda_python_alpha as lambda_python, 
    # aws_apigateway as apigw,
    # Duration,
    # CfnOutput,
    # aws_iam as iam, 
)
from constructs import Construct
import os

class FlaskStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

        docker_lambda = _lambda.DockerImageFunction(
            self, "WebAdapterFunction",
            code=_lambda.DockerImageCode.from_image_asset(
                directory=project_root
            )
        )

        # Add a Function URL for public access to the Lambda function.
        function_url = docker_lambda.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE
        )

        # Output the function URL so you can access it after deployment.
        self.output_web_adapter_url = function_url.url
