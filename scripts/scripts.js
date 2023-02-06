var client_id = '6d750bda24bb4ac8be2d2f6f13a24d40';
var redirect_uri = 'http://localhost:8888/callback';

var app = express();

app.get('/login', function(req, res) {
    
    var state = generateRandomString(16);
    var scope = 'user-read-private user-read-email';

    res.redirect('https://accounts.spotify.com/authorize?' +
        querystring.stringify({
            response_type: 'code',
            client_id: client_id,
            scope: scope,
            redirect_uri: redirect_uri,
            state: state
        }));

});