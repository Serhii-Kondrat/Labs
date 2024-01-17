// script.js

const apiUrl = 'http://127.0.0.1:5000/api';

function getUsers() {
    fetch(`${apiUrl}/users`)
        .then(response => response.json())
        .then(data => document.getElementById('getUsersResult').innerText = JSON.stringify(data, null, 2));
}

function getUserById() {
    const userId = document.getElementById('userId').value;
    fetch(`${apiUrl}/user/${userId}`)
        .then(response => response.json())
        .then(data => document.getElementById('getUserByIdResult').innerText = JSON.stringify(data, null, 2));
}

function createUser() {
    const username = document.getElementById('createUsername').value;
    const email = document.getElementById('createEmail').value;
    fetch(`${apiUrl}/users`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email }),
    })
    .then(response => response.json())
    .then(data => document.getElementById('createUserResult').innerText = JSON.stringify(data, null, 2));
}

function updateUser() {
    const userId = document.getElementById('updateUserId').value;
    const newUsername = document.getElementById('updateUsername').value;
    const newEmail = document.getElementById('updateEmail').value;
    fetch(`${apiUrl}/user/${userId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: newUsername, email: newEmail }),
    })
    .then(response => response.json())
    .then(data => document.getElementById('updateUserResult').innerText = JSON.stringify(data, null, 2));
}

function deleteUser() {
    const userId = document.getElementById('deleteUserId').value;
    fetch(`${apiUrl}/user/${userId}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => document.getElementById('deleteUserResult').innerText = JSON.stringify(data, null, 2));
}
