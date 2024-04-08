################### WIP ##################

FROM public.ecr.aws/lambda/python:3.8

ENV PYTHON_SITE_PACKAGES=/var/lang/lib/python3.10/site-packages
ENV NUMBA_CACHE_DIR=/tmp/

# install git and Github CLI
RUN yum install git - y &&
RUN type -p yum-config-manager >/dev/null || yum install yum-utils -y && \
    yum-config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo && \
    yum install gh -y

# install basic-pitch with tensorflow lite capabilities
RUN git clone https://github.com/spotify/basic-pitch && \
    cd basic-pitch && \
    gh pr checkout 100

# Install the specified packages
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip3.8 install --upgrade pip
RUN pip3.8 install -r requirements.txt

# Install the code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Environment variables to refer to the model location
# ENV MODELPATHBASICPITCH=var/lang/bin/lib/python3.9/site-packages/basic_pitch/saved_models/icassp_2022/npm
# ENV MODELPATH=/usr/local/lib


# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]

# Install the specified packages
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip3.8 install --upgrade pip
RUN pip3.8 install -r requirements.txt

# Install the code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Environment variables to refer to the model location
# ENV MODELPATHBASICPITCH=var/lang/bin/lib/python3.9/site-packages/basic_pitch/saved_models/icassp_2022/npm
# ENV MODELPATH=/usr/local/lib


# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]