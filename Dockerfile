FROM ubuntu:latest

# ------ datadog ------ #

# Get curl:
RUN apt-get update && apt-get install -y curl
RUN DD_API_KEY=a8d87779d248091bddc2f18a15467d88 \
    DD_SITE="us5.datadoghq.com" \
    DD_APM_INSTRUMENTATION_ENABLED=host \
    DD_HOSTNAME=default \
    bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script_agent7.sh)"
# ------ python app ------ #

RUN apt-get update && apt-get install -y python3.9 python3-pip libpq-dev
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

# ------ run the app ------ #

EXPOSE 8000

ENV GATEWAY_URL https://gateway-api-service-merok23.cloud.okteto.net
ENV DB_URI postgresql://cwfvbvxl:jtsNDRjbVqGeBgYcYvxGps3LLlX_t-P5@berry.db.elephantsql.com:5432/cwfvbvxl
ENV RABBITMQ_URL amqps://skglvayb:RVulev-DurTkD_kARAFR5idNzUPqO88T@jackal.rmq.cloudamqp.com/skglvayb
ENV UPTRACE_DSN https://SAe6OtAs8ysrYmkJmM8t-Q@api.uptrace.dev?grpc=4317

CMD ["bash", "-c", "service datadog-agent start && exec uvicorn control.controller:app --host 0.0.0.0 --port 8000"]
