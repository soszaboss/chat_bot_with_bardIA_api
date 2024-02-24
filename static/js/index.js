'strict mode';

let btnNewDiscussionDisabled = true;
const chatContainer = $('#chat-container');
const textArea = $('#floatingTextarea2');

const form = $('#form-submit').on("submit", function (e) {
    e.preventDefault();
    sendRequest()
})

textArea.on('keyup', function (e){
      if (e.key === 'Enter' || e.keyCode === 13) {
    // Do something when Enter is pressed
        sendRequest();
  }
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function sendRequest() {
    const userRequest = textArea.text()
    const data = {userRequest: userRequest, btnNewDiscussionDisabled: btnNewDiscussionDisabled}
    $.ajax('chatroom/', {
        data: data,
        type: 'POST',
        header: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        success: function (response) {
            chatContainer.text(`<p class="user-discussion mb-5"><span class="rounded-pill me-5 bg-secondary-subtle py-4 px-4">You</span><span>${userRequest}</span> </p>`)
            chatContainer.text(`<p class="ai-discussion mb-5"><span class="rounded-pill me-5 bg-info-subtle p-4">AI</span><span>${response.response}</span></p>`)
            if (btnNewDiscussionDisabled){
                const discussionTitle = textArea.split(' ')[0];
                $('#btn-add-discussion-section, #btn-add-discussion').removeClass('area-disabled"');
                $('#btn-add-discussion').removeProp('disabled');
                $('#discussion-section').html(`${discussion(discussionTitle)}`);
                textArea.val('');
                btnNewDiscussionDisabled = false
            }
        }
    })
}


function minimizeString(str) {
  if (str.length > 20) {
    return str.substring(0, 20) + '...';
  } else {
    return str;
  }
}

const discussion = (string) => {
    const newString = minimizeString(string)
    return `            <p class="discussion-section mb-3 container" id="discussion-section">
                <button class="btn btn-select-discussion rounded-pill btn-lg">
                    <span>
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-chat-right" viewBox="0 0 16 16">
                          <path d="M2 1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h9.586a2 2 0 0 1 1.414.586l2 2V2a1 1 0 0 0-1-1zm12-1a2 2 0 0 1 2 2v12.793a.5.5 0 0 1-.854.353l-2.853-2.853a1 1 0 0 0-.707-.293H2a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2z"/>
                        </svg>
                    </span>
                    <span class="ms-2">
                        ${newString}
                    </span>
                </button>
            </p> `
}


