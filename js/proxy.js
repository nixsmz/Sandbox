const http = require('http');
const https = require('https');
const { URL } = require('url');

const SERVER_PORT = 7070;

const server = http.createServer((clientReq, clientRes) => {
  // CORS
  clientRes.setHeader('Access-Control-Allow-Origin', '*');
  clientRes.setHeader('Access-Control-Allow-Methods', '*');
  clientRes.setHeader('Access-Control-Allow-Headers', '*');
  // Options
  if(clientReq.method === 'OPTIONS') {
    clientRes.writeHead(204);
    clientRes.end();
    return;
  }
  // Find and parse URL
  const forwardedUrl = clientReq.headers["forwarded"];
  if (!forwardedUrl) {
    clientRes.writeHead(400, { "Content-Type": "text/plain" });
    clientRes.end('Forwarded field missing');
    return;
  }
  let url;
  try { url = new URL(forwardedUrl); } catch (err) {
    clientRes.writeHead(400, { "Content-Type": "text/plain" });
    clientRes.end("URL Forwarded not valid");
    return;
  }
  // Set request options
  delete clientReq.headers["host"];
  delete clientReq.headers["forwarded"];
  const options = {
    host: url.hostname,
    port: url.port || (url.protocol === 'https:' ? 443 : 80),
    path: url.pathname + url.search,
    method: clientReq.method,
    headers: clientReq.headers
  };
  const protocol = url.protocol === 'https:' ? https : http;
  // Send request and pipe result
  console.log("Options:", options);
  const proxyReq = protocol.request(options, (proxyRes) => {
    console.log(`Proxy reponse (${proxyRes.statusCode}): ${proxyRes.headers}`);
    clientRes.writeHead(proxyRes.statusCode, proxyRes.headers);
    proxyRes.pipe(clientRes, { end: true });
  });
  proxyReq.on('error', (err) => {
    console.error('Error:', err.message);
    clientRes.writeHead(500);
    clientRes.end('Error');
  });
  clientReq.pipe(proxyReq, { end: true });
});

server.listen(SERVER_PORT, () => {
  console.log(`Proxy in ascolto su http://localhost:${SERVER_PORT}`);
});
