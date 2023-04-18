eel.expose("setConnectionStatus")
const setConnectionStatus = (value) => {
    document.getElementById("notification").hidden = value
    document.getElementById("retryBtn").hidden = value
    document.getElementById("newRenderBtn").hidden = !value
}

eel.expose("setWorkers")
const setWorkers = (workers) => {
    const workerSelect = document.getElementById("worker")
    workers.forEach((worker) => {
        const option = new Option(worker, worker)
        workerSelect.add(option, undefined)
    })
}