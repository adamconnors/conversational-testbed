gcloud config set project <PROJECT_ID>
gcloud auth application-default set-quota-project <PROJECT_ID>

cd conversational-client
ng build

cd ../server
gcloud app deploy
