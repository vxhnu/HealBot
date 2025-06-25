function appendMessage(sender, text) {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);

    if (sender === 'bot') {
        msgDiv.innerHTML = text; // allows clickable HTML links
    } else {
        msgDiv.textContent = text;
    }

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Show locate button if bot message mentions hospital lookup
    if (sender === 'bot' && /find hospitals near you/i.test(text)) {
        document.getElementById('locate-btn').style.display = 'inline-block';
    }
}

document.getElementById('send-btn').onclick = sendMessage;
document.getElementById('user-input').addEventListener('keypress', e => {
    if (e.key === 'Enter') sendMessage();
});

function sendMessage() {
    const input = document.getElementById('user-input');
    const text = input.value.trim();
    if (!text) return;
    appendMessage('user', text);
    input.value = '';

    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
    })
    .then(res => res.json())
    .then(data => appendMessage('bot', data.response))
    .catch(console.error);
}

document.getElementById('locate-btn').onclick = () => {
    if (!navigator.geolocation) {
        appendMessage('bot', 'Geolocation not supported.');
        return;
    }

    navigator.geolocation.getCurrentPosition(pos => {
        fetch('/hospitals', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                lat: pos.coords.latitude,
                lon: pos.coords.longitude
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.hospitals) {
                data.hospitals.forEach(h => appendMessage('bot', h));
            } else {
                appendMessage('bot', 'Could not fetch hospitals.');
            }
            document.getElementById('locate-btn').style.display = 'none';
        })
        .catch(() => appendMessage('bot', 'Error fetching hospitals.'));
    }, () => appendMessage('bot', 'Unable to retrieve location.'));
};
















// function appendMessage(sender, text) {
//     const chatBox = document.getElementById('chat-box');
//     const msgDiv = document.createElement('div');
//     msgDiv.classList.add('message', sender);
//     msgDiv.textContent = text;
//     chatBox.appendChild(msgDiv);
//     chatBox.scrollTop = chatBox.scrollHeight;

//     // Show locate button on medical_centers prompt
//     if (sender === 'bot' && /find hospitals near you/i.test(text)) {
//         document.getElementById('locate-btn').style.display = 'inline-block';
//     }
// }

// document.getElementById('send-btn').onclick = sendMessage;
// document.getElementById('user-input').addEventListener('keypress', e => {
//     if (e.key === 'Enter') sendMessage();
// });

// function sendMessage() {
//     const input = document.getElementById('user-input');
//     const text = input.value.trim();
//     if (!text) return;
//     appendMessage('user', text);
//     input.value = '';

//     fetch('/predict', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ message: text })
//     })
//     .then(res => res.json())
//     .then(data => appendMessage('bot', data.response))
//     .catch(console.error);
// }

// document.getElementById('locate-btn').onclick = () => {
//     if (!navigator.geolocation) {
//         appendMessage('bot', 'Geolocation not supported.');
//         return;
//     }
//     navigator.geolocation.getCurrentPosition(pos => {
//         fetch('/hospitals', {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({
//                 lat: pos.coords.latitude,
//                 lon: pos.coords.longitude
//             })
//         })
//         .then(res => res.json())
//         .then(data => {
//             if (data.hospitals) {
//                 data.hospitals.forEach(h => appendMessage('bot', h));
//             } else {
//                 appendMessage('bot', 'Could not fetch hospitals.');
//             }
//             document.getElementById('locate-btn').style.display = 'none';
//         })
//         .catch(() => appendMessage('bot', 'Error fetching hospitals.'));
//     }, () => appendMessage('bot', 'Unable to retrieve location.'));
// };
