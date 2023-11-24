let loc = window.location
let wsStart = loc.protocol === 'https:' ? 'wss://' : 'ws://'
let endpoint = wsStart + loc.host + '/ws/chat/chatpage/';  
const USER_ID = $('#logged-in-user').val();
const recipient_user = $('#recipient-user-id').val();

let input_message = $('#input-message')
let message_body = $('.msg_card_body')
var socket = new WebSocket(endpoint);

socket.onopen = async function (e){
    console.log('open', e)
    $('#send-message-form').on('submit', function (e){
        e.preventDefault();
        let message = input_message.val();
        let send_to;
        let thread_id = get_active_thread_id();

        if (USER_ID && recipient_user){
            send_to = recipient_user
            console.log(recipient_user)
        }else{
            send_to = recipient_user
            console.log(recipient_user)
        }

        let data = {
            'message': message,
            'send_by':USER_ID,
            'send_to':send_to,
            'thread_id':thread_id
        }

        data = JSON.stringify(data);
        socket.send(data);
        $(this)[0].reset();
    });
}

socket.onmessage = async function (e){
    console.log('message', e)
    let data = JSON.parse(e.data);
    let message = data['message']
    let send_by_id =  data['send_by']
    console.log(send_by_id)
    newMessage(message, send_by_id)
}
socket.onerror = async function (e){
    console.log('error', e)
}
socket.onclose = async function (e){
    console.log('close', e)
}

message_body.find('.alert').removeClass('alert-primary alert-dark');

function newMessage(message,send_by_id) {
    if($.trim(message) === '') {
        return false;
    }
    if (send_by_id == USER_ID) {
        // Message sent by the user (align to the right)
        message_element = `
            <div class="d-flex mb-4 replied justify-content-start ">
                <div class="msg_cotainer_send alert alert-primary">
                    ${message} <br>
                    <span class="msg_time_send" style="font-size: 10px;">8:55 AM, Today</span>
                </div>
            </div>
        `;
    } else {
        // Message received (align to the left)
        message_element = `
        <div class="d-flex mb-4 replied justify-content-end">
                    <div class="msg_cotainer_admin alert alert-dark">
                    ${message} <br>
                        <span class="msg_time_send" style="font-size: 10px;">9:00 AM, Today</span>
                    </div>
                </div>
        `;
    }
    
    message_body.append($(message_element))
    message_body.animate({
        scrollTop: $(document).height()
    },100);
    input_message.val(null);

    
}
function get_active_thread_id() {
    let thread_id = $('.thread-id-input').val();
    if (!thread_id) {
        return null;
    }
    return thread_id;
}
