
#!/bin/bash

while true; do

    # This should be another background process, maybe another script, since okteto logs is blocking
    # maybe we can do something like: okteto logs > /tmp/okteto_logs &
    # and then read the logs from /tmp/okteto_logs
    # curl -X POST -H "Content-Type: application/json" -d "$okteto_logs" http://example.com/logs
    # rm /tmp/okteto_logs
    # kill $!
    # sleep 60
    # Fetch okteto logs
    okteto_logs=$(okteto logs)

    # Post logs to another service
    curl -X POST -H "Content-Type: application/json" -d "$okteto_logs" http://example.com/logs

    # Get resource information
    ram_usage=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
    cpu_usage=$(top -bn1 | grep load | awk '{printf "%.2f%%", $(NF-2)}')
    disk_usage=$(df -h | awk '$NF=="/"{printf "%s", $5}')

    # Create JSON payload with resource information
    resource_info="{\"ram_usage\": \"$ram_usage\", \"cpu_usage\": \"$cpu_usage\", \"disk_usage\": \"$disk_usage\"}"

    # Post resource information to another service
    curl -X POST -H "Content-Type: application/json" -d "$resource_info" http://example.com/resources

    # Sleep for 60 seconds
    sleep 60
done
