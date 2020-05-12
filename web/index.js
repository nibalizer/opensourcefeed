var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var port = process.env.PORT || 3000;
bodyParser = require('body-parser');
app.use(bodyParser.json());


app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

app.use(express.static('public'))

app.get('/web', function(req, res){
  res.sendFile(__dirname + '/webview.html');
});

app.post('/submit', function(req, res){
  console.log(req.body);
  io.emit('chat message', req.body.message);
  res.send('ok')
});

io.on('connection', function(socket){
  socket.on('chat message', function(msg){
    io.emit('chat message', msg);
  });
});

http.listen(port, function(){
  console.log('listening on *:' + port);
});
