FROM amazon/linux

FROM public.ecr.aws/lambda/python:3.10

ENV PYTHON_SITE_PACKAGES=/var/lang/lib/python3.8/site-packages
ENV NUMBA_CACHE_DIR=/tmp/

# Install the specified packages
RUN pip3.10 install --upgrade pip
RUN pip3.10 install tensorflow==2.11.0
# RUN pip3.8 install basic-pitch

# Install the code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# ENV MODELPATHBASICPITCH var/lang/bin/lib/python3.9/site-packages/basic_pitch/saved_models/icassp_2022/npm
# ENV MODELPATH /usr/local/lib


# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]