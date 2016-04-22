var global_socket;
var user_socket;

$(document).ready(function(){
    global_socket = io.connect('http://' + document.domain + ':' + location.port + '/');
    user_socket = io('/user');

    global_socket.on('flash', function(msg){
        $('#flashes').fadeOut('slow', function(){
            $('#flashes').empty();
            $('#flashes').append(msg);
            $('#flashes').fadeIn('slow');
        });
    });

    global_socket.on('load content', function(content){
        $('#content').fadeOut('slow', function(){
            $('#content').empty();
            $('#content').append(content);
            $('#content').fadeIn('slow');
        });
    });

});
