const express = require('express');
const os = require('os');

const app = express();
const PORT = process.env.PORT || 8080;
const VERSION = process.env.APP_VERSION || '1.0';
const COLOR = process.env.APP_COLOR || '#2e025e';

app.get('/', (req, res) => {
  res.send(`
    <body style="font-family:sans-serif;border-top:12px solid ${COLOR};padding:16px">
      <h1>Hello from this NodeJS app!</h1>
      <p><b>Version:</b> ${VERSION}</p>
      <p><b>Served by pod:</b> ${os.hostname()}</p>
      <p>Refresh to see the Service spread requests across pods.</p>
      <p>Send a request to <code>/error</code> to crash this pod and watch Kubernetes replace it.</p>
    </body>
  `);
});

// Liveness/readiness endpoint used by the probes in deployment.yaml and the Helm chart
app.get('/healthz', (req, res) => res.status(200).send('ok'));

// Crash on purpose: demonstrates restarts (RESTARTS column) and self-healing
app.get('/error', (req, res) => {
  console.error(`Crashing on purpose (pod ${os.hostname()})`);
  process.exit(1);
});

app.listen(PORT, () => console.log(`nodejs-app v${VERSION} listening on ${PORT}`));
