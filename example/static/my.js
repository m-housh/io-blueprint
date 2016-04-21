var global_socket;
var test_socket;

$(document).ready(function(){
    namespace = '/';
    global_socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    test_socket = io('/test');

    global_socket.on('flash', function(msg){
        $('#flashes').append('<br>' + $('<div/>').text(msg).html());
    });

    $('form#echo').submit(function(event){
        test_socket.emit('echo', {data: $('#message').val()});
        return false;
    });
})
