FROM public.ecr.aws/lambda/python:3.10
RUN ldd --version

ENV PYTHON_SITE_PACKAGES=/var/lang/lib/python3.7/site-packages
ENV NUMBA_CACHE_DIR=/tmp/

# Install the specified packages
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip3.7 install --upgrade pip
RUN pip3.7 install basic-pitch

# Uninstalling the tensorflow-library basic-pitch is made with 
# because 2.x-versions use AVX-instructions and they're not supported on AWS lambda
RUN pip3.7 uninstall tensorflow -y

################# START OF TENSORFLOW INSTALLATION #################
# Before installing, check this link for the GLIBC incompatibility issue https://gist.github.com/michaelchughes/85287f1c6f6440c060c3d86b4e7d764b
# Building Tensorflow from source so that the GLIBC incompatibility issue does not persist
# Install system packages required for TensorFlow build
RUN yum update -y && yum install -y \
    gcc gcc-c++ python3-devel \
    java-1.8.0-openjdk-devel \
    git zip unzip \
    && yum clean all

# Install Bazel (you may need to adjust the version)
RUN curl -LO "https://github.com/bazelbuild/bazel/releases/download/3.7.2/bazel-3.7.2-installer-linux-x86_64.sh" \
    && chmod +x bazel-3.7.2-installer-linux-x86_64.sh \
    && ./bazel-3.7.2-installer-linux-x86_64.sh --user \
    && rm bazel-3.7.2-installer-linux-x86_64.sh

# Set up the environment variable for Bazel
ENV PATH="$PATH:$HOME/bin"

# Clone TensorFlow repository
RUN git clone -b r1.14 https://github.com/tensorflow/tensorflow.git /tensorflow
WORKDIR /tensorflow
# Checkout a 1.x branch, replace 'r1.x' with the specific version you need
RUN git checkout r1.14

# Configure the build for your system
RUN ./configure

# Build TensorFlow
RUN bazel build //tensorflow/tools/pip_package:build_pip_package

# Package TensorFlow and install
RUN ./bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
RUN pip install /tmp/tensorflow_pkg/tensorflow-*.whl
################# FINALISED TENSORFLOW INSTALLATION #################

# Install the code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Environment variables to refer to the model location
# ENV MODELPATHBASICPITCH=var/lang/bin/lib/python3.9/site-packages/basic_pitch/saved_models/icassp_2022/npm
# ENV MODELPATH=/usr/local/lib


# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]