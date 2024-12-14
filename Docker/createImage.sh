echo "Coping all the python files"
mkdir -p app
cp -R ../src/* app/.


echo "coping the configuration yaml file"
mkdir -p resources
cp ../resources/config.yaml resources

echo "Docker image generating"
docker build -t cosm-bot .

echo "clean docker paths"
rm -rf resources/*
rm -rf app/*

