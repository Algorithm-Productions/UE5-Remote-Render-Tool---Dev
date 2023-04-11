function createTable(list){
    const cols = ['uuid', 'name', 'owner', 'worker', 'time_created', 'status', 'estimated_finish', 'time_estimate', 'progress', 'output_path'];
    const table = document.createElement("table");
    const tr = table.insertRow(-1);
    for (let i = 0; i < cols.length; i++) {
        const theader = document.createElement("th");
        if (cols[i] !== 'output_path')
            theader.innerHTML = cols[i];

        tr.appendChild(theader);
    }
    const deleteTHead = document.createElement("th");
    tr.appendChild(deleteTHead);

    for (let i = 0; i < list.length; i++) {
        const trow = table.insertRow(-1);
        const uuid = list[i]['uuid'];

        for (let j = 0; j < cols.length; j++) {
            const cell = trow.insertCell(-1);
            cell.innerHTML = list[i][cols[j]];

            if (cols[j] === 'output_path') {
                const btn = document.createElement("button")
                cell.className = 'copyCell'
                btn.innerText = `🔗`
                btn.className = 'copyBtn'
                btn.addEventListener('click', () => handleClick(list[i][cols[j]]), false)

                trow.deleteCell(-1)
                trow.appendChild(btn)
            }

            if (cols[j] === 'progress'){
                cell.innerHTML = '';
                cell.style.width = '200px';

                const container = document.createElement("div");
                cell.appendChild(container);
                container.setAttribute('class', 'progressContainer');

                const bar = document.createElement("div");
                container.appendChild(bar);

                bar.setAttribute('class', 'progressBar');
                bar.setAttribute('id', uuid + '_progress');

                bar.style.width = list[i]['progress'] + '%';
                bar.innerHTML = list[i]['progress'] + '%';

            }

            if (cols[j] === 'time_estimate'){
                cell.setAttribute('id', uuid + '_estimate');
            }

            if (cols[j] === 'estimated_finish'){
                cell.setAttribute('id', uuid + '_finished');
            }

            if (cols[j] === 'status'){
                cell.setAttribute('id', uuid + '_status');
            }

        }
        const deleteBtn = document.createElement("button")
        deleteBtn.innerText = `☓`
        deleteBtn.className = 'copyBtn'
        deleteBtn.addEventListener('click', () => deleteEntry(list[i]), false)
        trow.appendChild(deleteBtn)
    }

    const el = document.getElementById("table");
    el.innerHTML = "";
    el.appendChild(table);
}


function handleClick(path) {
    navigator.clipboard.writeText(path).catch(e => console.error(e.message))
}

async function deleteEntry(element) {
    console.log(element)

    const response = await fetch(`http://127.0.0.1:5000/api/delete/${element.uuid}`, {
        method: 'DELETE',
        headers: {
            'Content-type': 'application/json'
        }
    });

    const resData = 'resource deleted...';

    location.reload()
    return resData;
}


