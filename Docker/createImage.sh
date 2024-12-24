echo "clean docker paths"
rm -rf host
rm -rf app

echo "Coping all the python files"
mkdir -p app
cp -R ../src/* app/.

echo "create directory for mount volume"
mkdir -p host/resources
echo "coping the configuration yaml file"
cp ../CosmWebex-config.yaml host/resources

echo "Docker image 'CosmWebex' generating"
docker build -t cosm-bot .

