function submitUserForm(){
    user_socket.emit('post', {form: { 
        first_name: $('#first_name').val(), 
        last_name: $('#last_name').val(),
        csrf_token: $('#csrf_token').val() 
    } });
    return false;
}
