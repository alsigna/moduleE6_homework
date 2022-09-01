let connectionString
let msgText
let roomId
let userName
let roomList

const msgList = document.getElementById("messages-list");
const msgForm = document.getElementById("msg-form");

if (msgForm !== null) {
    msgText = document.getElementById("msg-text");
    roomId = msgForm.getAttribute("room-id");
    userName = msgForm.getAttribute("username");
    connectionString = "ws://" + window.location.host + "/ws/room/" + roomId + "/" + userName + "/";

    msgForm.onsubmit = () => {
        let data = {
            "room_id": roomId,
            "username": userName,
            "text": msgText.value,
        }
        msgText.value = "";

        websocket.send(JSON.stringify(data));
        return false;
    };

} else {
    roomList = document.getElementsByClassName("j-new-msg-notif");
    userName = roomList[0].getAttribute("username");
    connectionString = "ws://" + window.location.host + "/ws/roomlist/" + userName + "/";
    console.log("roomList :>> ", roomList);

}

let websocket;

console.log("connectionString :>> ", connectionString);

const writeToConsole = message => {
    console.log("message :>> ", message);
}

const displayNotification = message => {
    json_data = JSON.parse(message);
    for (const room of roomList) {
        let roomId = room.getAttribute("room-id");
        if (roomId == json_data.room_id) {
            room.textContent = "новые сообщения"
        }
    }
}

function displayNewMessage(message) {
    let div = document.createElement("div");
    div.className = "pl-3"
    json_data = JSON.parse(message);
    const newMessage = `<span><b>${json_data.username}</b>: ${json_data.text}</span>`
    div.innerHTML = newMessage;
    msgList.appendChild(div);
}

window.addEventListener("load", () => {
    websocket = new WebSocket(connectionString);
    websocket.onopen = function () {
        writeToConsole("CONNECTED");
    };
    websocket.onclose = function () {
        writeToConsole("DISCONNECTED");
    };
    websocket.onmessage = function (event) {
        writeToConsole("NEW MESSAGE");
        if (msgForm !== null) {
            displayNewMessage(event.data);
        } else {
            displayNotification(event.data);
        }
    };
    websocket.onerror = function (event) {
        writeToConsole("ERROR");
        writeToConsole(event.data);
    };
});

