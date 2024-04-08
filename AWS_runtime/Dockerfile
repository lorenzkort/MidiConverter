FROM public.ecr.aws/lambda/python:3.8

RUN yum update -y && yum groupinstall -y "Development Tools"
RUN yum install -y gcc-c++  development 
RUN yum install -y python3-devel

# ENV
ENV PYTHON_SITE_PACKAGES=/var/lang/lib/python3.8/site-packages
ENV NUMBA_CACHE_DIR=/tmp/

# install Tensorflow Lite Runtime
RUN pip3 install numpy wheel
COPY tflite_runtime-2.2.0rc0-cp38-cp38-linux_x86_64.whl ${LAMBDA_TASK_ROOT}
# If we ever need to install an updated version of TF-lite, this is how to compile it for the AWS-lambda base image
    # RUN yum install -y git
    # WORKDIR ${LAMBDA_TASK_ROOT}/tflite
    # RUN git clone --branch v2.2.0-rc0 https://github.com/tensorflow/tensorflow.git
    # RUN sh ./tensorflow/tensorflow/lite/tools/pip_package/build_pip_package.sh
    # RUN pip3 install tensorflow/tensorflow/lite/tools/pip_package/gen/tflite_pip/python3/dist/tflite_runtime-2.2.0rc0-cp38-cp38-linux_x86_64.whl

# Install tf-lite runtime for Python 3.8
RUN pip install tflite_runtime-2.2.0rc0-cp38-cp38-linux_x86_64.whl
RUN pip install tflite-runtime

# Copy and install a PR-version of basic-pitch which supports Tensorflow Lite, for effective model serving:
# https://github.com/spotify/basic-pitch/pull/100
COPY ./basic-pitch ${LAMBDA_TASK_ROOT}/basic-pitch
RUN pip3 install ./basic-pitch

# Copy over the lambda function
WORKDIR ${LAMBDA_TASK_ROOT}
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]