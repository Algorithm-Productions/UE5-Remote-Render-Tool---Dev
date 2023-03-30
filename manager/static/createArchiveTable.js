function createArchiveTable(list){
    const cols = ['uuid', 'name', 'owner', 'worker', 'time_created', 'status'];
    const table = document.createElement("table");
    const tr = table.insertRow(-1);
    for (let i = 0; i < cols.length; i++) {
        const theader = document.createElement("th");
        theader.innerHTML = cols[i];
        tr.appendChild(theader);
    }

    for (let i = 0; i < list.length; i++) {
        const trow = table.insertRow(-1);
        const uuid = list[i]['uuid'];

        for (let j = 0; j < cols.length; j++) {
            const cell = trow.insertCell(-1);
            cell.innerHTML = list[i][cols[j]];

            if (cols[j] === 'status'){
                cell.setAttribute('id', uuid + '_status');
            }

        }
    }

    const el = document.getElementById("table");
    el.innerHTML = "";
    el.appendChild(table);
}



