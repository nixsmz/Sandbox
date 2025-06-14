const { PassThrough } = require('stream');
const ffmpeg = require('fluent-ffmpeg');
const http = require('http');
const fs = require('fs');
const os = require('os');

const PORT = 10000;

const audioStream = ffmpeg({ end: true })
  .input('input.mp3')
  .inputOptions('-re')
  .outputFormat('mp3')
  .audioCodec('libmp3lame')
  .on('start', () => console.log(`Streaming started at http://localhost:${PORT}`))
  .on('error', (err) => console.error('Streaming error:', err))
  .on('end', () => process.exit(1))
  .pipe();

const server = http.createServer((request, response) => {
  response.writeHead(200, {
    'Content-Type': 'audio/mpeg',
    'Transfer-Encoding': 'chunked',
    'Connection': 'keep-alive',
  });
  const clientStream = new PassThrough();
  audioStream.pipe(clientStream).pipe(response);
  request.on('close', () => {
    clientStream.destroy();
    response.end();
  });
});

audioStream.pipe(fs.createWriteStream(os.devNull));
server.on('close', () => audioStream.end());
server.listen(PORT);
