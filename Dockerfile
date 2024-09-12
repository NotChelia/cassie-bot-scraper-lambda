FROM public.ecr.aws/lambda/python:3.12

WORKDIR /var/task

RUN microdnf -y install nodejs npm


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["lambda_function.lambda_handler"]

