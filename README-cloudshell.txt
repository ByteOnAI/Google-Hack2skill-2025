
Welcome to Google Cloud Shell, a tool for managing resources hosted on Google Cloud Platform!
The machine comes pre-installed with the Google Cloud SDK and other popular developer tools.

Your 5GB home directory will persist across sessions, but the VM is ephemeral and will be reset
approximately 20 minutes after your session ends. No system-wide change will persist beyond that.

Type "gcloud help" to get help on using Cloud SDK. For more examples, visit
https://cloud.google.com/shell/docs/quickstart and https://cloud.google.com/shell/docs/examples

Type "cloudshell help" to get help on using the "cloudshell" utility.  Common functionality is
aliased to short commands in your shell, for example, you can type "dl <filename>" at Bash prompt to
download a file. Type "cloudshell aliases" to see these commands.

Type "help" to see this message any time. Type "builtin help" to see Bash interpreter help.
  
## Establish a script to run the agents

1. Prepare the `serve.sh` file and add permissions.
```
chmod +x serve.sh
```

2. Command to build and run docker images on cloud------
```
docker build -t mytripmate:local .
docker run --rm -p 8080:8080 \
  -e MODEL="gemini-2.5-flash" \
  -e GOOGLE_CLOUD_PROJECT="<your-project-id>" \
  -e GOOGLE_CLOUD_LOCATION="us-central1" \
  -e GOOGLE_PLACES_API_KEY="<your-maps-key>" \
  mytripmate:local

```

Example: 

docker run --rm -p 8080:8080 -e MODEL="gemini-2.5-flash" -e GOOGLE_CLOUD_PROJECT="serious-flight-472808-m3" -e GOOGLE_CLOUD_LOCATION="us-central1" mytripmate:local

3. Configure google authorization

```
gcloud auth login

gcloud config set project <PROJECT_ID>

gcloud services enable run.googleapis.com artifactregistry.googleapis.com aiplatform.googleapis.com

gcloud artifacts repositories create mytripmate-repo   --repository-format=docker --location=us-central1

gcloud builds submit --tag us-central1-docker.pkg.dev/<PROJECT_ID>/mytripmate-repo/mytripmate:latest

gcloud run deploy mytripmate   --image us-central1-docker.pkg.dev/<PROJECT_ID>/mytripmate-repo/mytripmate:latest   --region us-central1   --allow-unauthenticated   --port 8080   --cpu 2 --memory 2Gi   --min-instances 0 --max-instances 5   --set-env-vars GOOGLE_CLOUD_PROJECT="serious-flight-472808-m3",GOOGLE_CLOUD_LOCATION=us-central1,MODEL="gemini-2.5-flash"   --timeout 900

```