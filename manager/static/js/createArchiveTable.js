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
    const lastTHeader = document.createElement("th");
    tr.appendChild(lastTHeader);

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

        const btn = document.createElement("button")
        btn.innerText = `🔗`
        btn.className = 'copyBtn'
        btn.addEventListener('click', () => openModal(list[i]), false)
        trow.appendChild(btn)
    }

    const el = document.getElementById("table");
    el.innerHTML = "";
    el.appendChild(table);
}

function openModal(item) {
    console.log(item)
}


