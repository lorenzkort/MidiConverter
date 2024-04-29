FROM public.ecr.aws/lambda/python:3.10

RUN pip install basic-pitch[onnx]

ENV NUMBA_CACHE_DIR=/tmp
ENV JOBLIB_TEMP_FOLDER=/tmp 

# Copy over the lambda function
WORKDIR ${LAMBDA_TASK_ROOT}
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]