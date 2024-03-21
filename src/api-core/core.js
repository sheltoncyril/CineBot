export {
    createChat,
    getChat,
    sendQuery
}
const baseURL = "http://localhost:5000"

const createChat = () => {
    return fetch(baseURL + `/chat`, {
        method: "POST",
        headers: {
            'accept': 'application/json',
        }
    })
        .then((res) => res.json())
        .then((data) => { return data })
        .catch((err) => console.log(err))
}

const getChat = (chatID) => {
    return fetch(baseURL + `/chat/${chatID}`, {
        method: "GET",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
        .then((res) => { return res })
        .catch((err) => console.log(err))
}

const sendQuery = (payload, chatID) => {
    return fetch(baseURL + `/chat/${chatID}/message`, {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: payload,
        })
    })
        .then((res) => res.json())
        .then((data) => { return data })
        .catch((err) => console.log(err))

}
