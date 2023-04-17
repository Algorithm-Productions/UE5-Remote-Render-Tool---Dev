const createLogsTable = (list) => {
    const dataCols = ['uuid', 'notificationType', 'jobUUID', 'timestamp', 'message', 'cleared'];
    const table = document.createElement("table");
    const tr = table.insertRow(-1);

    dataCols.forEach((item) => {
        const theader = document.createElement("th");
        theader.innerHTML = item;
        tr.appendChild(theader);
    });

    const infoTHead = document.createElement("th");
    tr.appendChild(infoTHead);
    const deleteTHead = document.createElement("th");
    tr.appendChild(deleteTHead);

    list.forEach((item) => {
        const trow = table.insertRow(-1);
        const uuid = item['uuid'];

        dataCols.forEach((innerItem) => {
            const cell = trow.insertCell(-1);
            cell.innerHTML = item[`${innerItem}`];
        });

        const infoBtn = document.createElement("button");
        infoBtn.innerText = `ℹ`;
        infoBtn.className = 'copyBtn';
        infoBtn.addEventListener('click', () => navigateToPage("logs", uuid, "?return=logs"), false);
        const infoCell = trow.insertCell(-1);
        infoCell.appendChild(infoBtn)

        const deleteBtn = document.createElement("button");
        deleteBtn.innerText = `☓`;
        deleteBtn.className = 'copyBtn';
        deleteBtn.addEventListener('click', () => deleteEntry("logs", uuid), false);
        const deleteCell = trow.insertCell(-1);
        deleteCell.appendChild(deleteBtn)
    });

    const tableElement = document.getElementById("table");
    tableElement.innerHTML = "";
    tableElement.appendChild(table);
}

const getReturnPath = () => {
    const url = new URL(window.location.toLocaleString());
    const searchArray = url.search.replace("?", "").split("&");

    const returnOptions = searchArray.filter((item) => {
        const splitItem = item.split("=");
        return splitItem.length === 2 && splitItem[0] === "return";
    });

    const itemArray = (returnOptions.length !== 0) ? returnOptions[0].split("=") : [];
    const path = (itemArray.length === 2) ? itemArray[1] : ""

    return path;
}

const specialDeleteLog = async (uuid) => {
    const response = await fetch(`http://127.0.0.1:5000/api/logs/delete/${uuid}`, {
        method: 'DELETE',
        headers: {
            'Content-type': 'application/json'
        }
    });

    const returnUrl = getReturnPath();
    console.log(returnUrl)
    if (returnUrl === "logs")
        window.location.replace("http://127.0.0.1:5000/logs/")
    else
        window.location.replace("http://127.0.0.1:5000/")

    return response
}

const specialNavigate = () => {
    const returnUrl = getReturnPath();
    if (returnUrl === "logs")
        window.location.replace("http://127.0.0.1:5000/logs/")
    else
        window.location.replace("http://127.0.0.1:5000/")
}

const clearNotification = async (uuid) => {
    const response = await fetch(`http://127.0.0.1:5000/api/logs/put/${uuid}`, {
        method: 'PUT',
        body: '{"cleared": True}',
        headers: {
            'Content-type': 'application/json'
        }
    });

    window.location.reload()

    return response
}



