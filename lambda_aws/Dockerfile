#FROM amazon/aws-lambda-python:3.8
FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Copy dependencies
COPY lambda_requirements.txt /tmp/

# Install dependencies
RUN python -m pip install -r /tmp/lambda_requirements.txt

# Install ffmpeg to parse the videos:
# https://gist.github.com/willmasters/382fe6caba44a4345a3de95d98d3aae5
# https://github.com/pulumi/examples/blob/master/aws-ts-lambda-thumbnailer/docker-ffmpeg-thumb/Dockerfile
RUN yum install tar xz -y
RUN curl https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -o ffmpeg.tar.xz -s
RUN tar -xf ffmpeg.tar.xz
RUN mv ffmpeg-*-amd64-static/ffmpeg /usr/bin
# Check ffmpeg version works
RUN ffmpeg -version

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]