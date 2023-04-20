eel.expose("setConnectionStatus")
const setConnectionStatus = (value) => {
    document.getElementById("notification").hidden = value
    document.getElementById("retryBtn").hidden = value
    document.getElementById("newRenderBtn").hidden = !value
}

const closeWorker = () => {
    console.log("GGG")
    eel.closeWorker()(closeCallback)
}

const closeCallback = () => {
    window.location.href = "landing.html"
}