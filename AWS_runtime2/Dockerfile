FROM public.ecr.aws/lambda/python:3.11

# ENV
RUN pip install basic-pitch

# Copy over the lambda function
WORKDIR ${LAMBDA_TASK_ROOT}
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
RUN pip install tflite-runtime

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]