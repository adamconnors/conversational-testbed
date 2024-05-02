# To run locally:


## Start backend server:
To run the server locally, you must first install the Google Cloud CLI and set up your default project and application default credentials.


Follow [Google Cloud Installation Instructions](https://cloud.google.com/sdk/docs/install) to install the Google Cloud CLI.


Follow [Set up Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc) to set up application default credentials.


```sh
gcloud auth login


# Ensure your project has the Vertex APIs enabled
gcloud config set project [PROJECT_ID]
gcloud auth application-default login
gcloud auth application-default set-quota-project [PROJECT_ID]
```


```sh
 cd py-server
 pip install -r requirements.txt
 python main.py
```


You can test the server by pointing your browser at:
http://localhost:8080/chat?q=hello


## Start the client development server:
Install npm at: https://nodejs.org/en/download/.
Install the Angular CLI if necessary: ```npm install -g @angular/cli```


Then:
```sh
cd conversational-client
npm install
ng serve
```


Navigate to http://localhost:4200 and click the microphone icon to begin speaking.


# To push to Cloud
Set your cloud project and authenticate as above. Then:


```sh
cd conversational-client
npm run prod


cd ../py-server
gcloud app deploy
```
