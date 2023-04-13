function createArchiveTable(list){
    const renderCols = ['uuid', 'notificationType', 'jobUUID', 'timestamp', 'message'];
    const table = document.createElement("table");
    const tr = table.insertRow(-1);
    for (let i = 0; i < renderCols.length; i++) {
        const theader = document.createElement("th");
        theader.innerHTML = renderCols[i];
        tr.appendChild(theader);
    }
    const infoTHead = document.createElement("th");
    tr.appendChild(infoTHead);
    const deleteTHead = document.createElement("th");
    tr.appendChild(deleteTHead);


    for (let i = 0; i < list.length; i++) {
        const trow = table.insertRow(-1);

        for (let j = 0; j < renderCols.length; j++) {
            const cell = trow.insertCell(-1);
            cell.innerHTML = list[i][renderCols[j]];
        }

        const infoBtn = document.createElement("button")
        infoBtn.innerText = `ℹ`
        infoBtn.className = 'copyBtn'
        infoBtn.addEventListener('click', () => navigateToPage(list[i]), false)
        trow.appendChild(infoBtn)

        const deleteBtn = document.createElement("button")
        deleteBtn.innerText = `☓`
        deleteBtn.className = 'copyBtn'
        deleteBtn.addEventListener('click', () => clearNotification(list[i]), false)
        trow.appendChild(deleteBtn)
    }

    const el = document.getElementById("table");
    el.innerHTML = "";
    el.appendChild(table);
}

async function clearNotification(notification) {
    console.log(notification)

    const response = await fetch(`http://127.0.0.1:5000/api/notification/delete/${notification.uuid}`, {
        method: 'DELETE',
        headers: {
            'Content-type': 'application/json'
        }
    });

    const resData = 'resource deleted...';

    location.reload()
    return resData;
}

async function specialClearNotification(notification) {
    const restData = await clearNotification(notification)
    window.location.replace(`http://127.0.0.1:5000/`)
}

function navigateToPage(element) {
    window.location.replace(`http://127.0.0.1:5000/log/${element.uuid}`)
}

