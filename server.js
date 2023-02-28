/* load HTTP library */
const http = require('http');

var host = 'localhost';
var port = 8888;

/* Create an HTTP server to handle responses */
const requestListener = function(req, res) {
    res.writeHead(200);
    res.write("Hello World!\n");
    res.end("My first server\n")
};

const server = http.createServer(requestListener);
server.listen(port,host, () => {
    console.log(`Server is running on http://${host}:${port}`);
});