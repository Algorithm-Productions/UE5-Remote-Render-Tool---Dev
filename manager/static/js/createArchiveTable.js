function createArchiveTable(list){
    const renderCols = ['uuid', 'name', 'owner', 'worker'];
    const metaCols = ['project_name', 'finish_time', 'total_time', 'avg_frame'];
    const table = document.createElement("table");
    const tr = table.insertRow(-1);
    for (let i = 0; i < renderCols.length; i++) {
        const theader = document.createElement("th");
        theader.innerHTML = renderCols[i];
        tr.appendChild(theader);
    }
    for (let i = 0; i < metaCols.length; i++) {
        const theader = document.createElement("th");
        theader.innerHTML = metaCols[i];
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
            cell.innerHTML = list[i]["render_request"][renderCols[j]];
        }

        for (let j = 0; j < metaCols.length; j++) {
            const cell = trow.insertCell(-1);
            cell.innerHTML = list[i][metaCols[j]];
        }

        const infoBtn = document.createElement("button")
        infoBtn.innerText = `ℹ`
        infoBtn.className = 'copyBtn'
        infoBtn.addEventListener('click', () => navigateToPage(list[i]), false)
        trow.appendChild(infoBtn)

        const deleteBtn = document.createElement("button")
        deleteBtn.innerText = `☓`
        deleteBtn.className = 'copyBtn'
        deleteBtn.addEventListener('click', () => deleteArchive(list[i]), false)
        trow.appendChild(deleteBtn)
    }

    const el = document.getElementById("table");
    el.innerHTML = "";
    el.appendChild(table);
}


function navigateToPage(element) {
    window.location.replace(`http://127.0.0.1:5000/archive/${element.uuid}`)
}

async function deleteArchive(element) {
    const response = await fetch(`http://127.0.0.1:5000/api/archive/delete/${element.uuid}`, {
        method: 'DELETE',
        headers: {
            'Content-type': 'application/json'
        }
    });

    const resData = 'resource deleted...';

    location.reload()
    return resData;
}


