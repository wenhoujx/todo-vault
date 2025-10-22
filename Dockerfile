FROM public.ecr.aws/lambda/python:3.12
# Copy the Web Adapter binary from its separate, language-agnostic image.
# The `aws-lambda-adapter` image tag `0.9.1` was the latest at the time of this answer.
# Always check the AWS ECR Public Gallery for the most current version.
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter

# Copy the requirements file from your `lambda_app` subdirectory.
COPY layer_build_assets/requirements.txt .

# Install dependencies into the /var/task directory where your code will live.
RUN pip3 install -r requirements.txt --target /var/task

# Copy your application code into the image.
# The path is relative to the Docker build context, which is the project root.
COPY server/app.py /var/task/app.py

# Set the CMD to run your application. The Web Adapter will automatically
# detect and run the Flask application.
CMD [ "app.py" ]
