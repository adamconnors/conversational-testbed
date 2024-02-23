To run locally:

Client:
  cd conversational-client
  ng serve

Server:
  cd py-server
  python main.py


To push to Cloud:

gcloud config set project <PROJECT_ID>
gcloud auth application-default set-quota-project <PROJECT_ID>

cd conversational-client
npm run prod

cd ../server
gcloud app deploy
