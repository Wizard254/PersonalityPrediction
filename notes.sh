# User should not run this script
exit

# Delete all docker images and stopped containers
docker system prune -a

# List all docker volumes
docker volume ls

# delete a given docker volume named, vol1
docker volume rm vol1

# When you run this command, it will start printing the contents of
# the file (logger.txt) to the console. It will continue to monitor the file
# and display any new lines that are written to it in real-time.
tail -f logger.txt