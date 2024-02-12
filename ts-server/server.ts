/**
 * @license
 * Copyright Google LLC All Rights Reserved.
 *
 * Use of this source code is governed by an Apache2 license that can be
 * found in the LICENSE file and http://www.apache.org/licenses/LICENSE-2.0
==============================================================================*/

import express, { Express, Request, Response } from 'express';
import { GoogleAuth } from 'google-auth-library';
import * as path from 'path';

export const app: Express = express();
app.use(express.static('./static'));
app.use(express.json());  // for POST requests
app.use(express.urlencoded({ extended: true }));  // for PUT requests

export interface LlmOptions {
  modelId?: string; // e.g. text-bison
  candidateCount?: number, // e.g. 1 to 8 = number of completions
  maxOutputTokens?: number, // e.g. 256, 1024
  stopSequences?: string[], // e.g. ']
  temperature?: number,  // e.g. 0.8 (0=deterministic, 0.7-0.9=normal, x>1=wild)
  topP?: number,  // e.g. 0.8 (0-1, smaller = restricts crazyiness)
  topK?: number  // e.g. 40 (0-numOfTokens, smaller = restricts crazyiness)
}

export interface LlmRequest {
  text: string
  params?: LlmOptions
}

export interface SimpleEmbedRequest {
  text: string;
}

async function main() {

  const auth = new GoogleAuth({
    scopes: [
      'https://www.googleapis.com/auth/cloud-platform',
    ]
  });
  const projectId = await auth.getProjectId();
  const client = await auth.getClient();
  const credentials = await auth.getCredentials();
  const serviceAccountEmail = credentials.client_email;
  console.log('Running as serviceAccountEmail: ', serviceAccountEmail);

  app.get('/api', (req, res) => {
    res.send('Hello from App Engine!');
  });

  // Listen to the App Engine-specified port, or 8080 otherwise
  const PORT = process.env.PORT || 8080;
  app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}...`);
  });
}

main().catch(console.error);
