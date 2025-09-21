**STEP I**
Enable all required google services.

```
gcloud services enable run.googleapis.com  artifactregistry.googleapis.com  cloudbuild.googleapis.com aiplatform.googleapis.com bigquery.googleapis.com storage.googleapis.com pubsub.googleapis.com iam.googleapis.com firebase.googleapis.com logging.googleapis.com monitoring.googleapis.com maps-backend.googleapis.com cloudtasks.googleapis.com sqladmin.googleapis.com cloudscheduler.googleapis.com 
```
**STEP II**
Set IAM roles for the project

```bash
# Set your project ID and service account details
PROJECT_ID="serious-flight-472808-m3"
SA_NAME="adk-deployer"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"


# Create service account if it doesn't exist
gcloud iam service-accounts describe "$SA_EMAIL" --project "$PROJECT_ID" >/dev/null 2>&1 || \
  gcloud iam service-accounts create "$SA_NAME" --display-name="ADK Deployer" --project "$PROJECT_ID"

# Grant necessary roles to the service account
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/aiplatform.admin"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/storage.admin"
```

**STEP III**
Create virtual environment, activate and then install all requirements.
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**STEP IV**
create a adk tool agent.
```
adk create multi_tool_agent
```