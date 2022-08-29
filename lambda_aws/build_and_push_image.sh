
# Copied from: https://github.com/aws-samples/aws-lambda-docker-serverless-inference/blob/main/tensorflow-train-in-sagemaker-deploy-with-lambda/tensorflow_script_mode_training_in_sagemaker_and_serving_with_lambda.ipynb
# The name of our lambda function
lambda_function_name=<INSERT-IMAGE-NAME>

#cd container

account=$(aws sts get-caller-identity --query Account --output text)

# Get the region defined in the current configuration (default to us-east-1 if none defined)
region=$(aws configure get region)
region=${region:-us-east-1}

fullname="${account}.dkr.ecr.${region}.amazonaws.com/${lambda_function_name}:latest"

# If the repository doesn't exist in ECR, create it.

aws ecr describe-repositories --repository-names "${lambda_function_name}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${lambda_function_name}" > /dev/null
fi

# Get the login command from ECR and execute it directly
#$(aws ecr get-login --region ${region} --no-include-email)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${account}.dkr.ecr.us-east-1.amazonaws.com
# Build the docker image locally with the image name and then push it to ECR
# with the full name.

docker build  -t ${lambda_function_name} .
docker tag ${lambda_function_name} ${fullname}

docker push ${fullname}