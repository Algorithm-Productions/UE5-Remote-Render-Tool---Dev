const createQueueTable = (list) => {
    const dataCols = ['uuid', 'name', 'owner', 'worker', 'time_created', 'status', 'estimated_finish', 'time_estimate', 'progress'];
    const table = document.createElement("table");
    const tr = table.insertRow(-1);

    dataCols.forEach((item) => {
        const theader = document.createElement("th");
        theader.innerHTML = item;
        tr.appendChild(theader);
    });

    const pathTHead = document.createElement("th");
    tr.appendChild(pathTHead);
    const deleteTHead = document.createElement("th");
    tr.appendChild(deleteTHead);

    list.forEach((item) => {
        const trow = table.insertRow(-1);
        const uuid = item['uuid'];

        dataCols.forEach((innerItem, innerIdx) => {
            const cell = trow.insertCell(-1);
            cell.innerHTML = item[`${innerItem}`];

            if (innerItem === 'progress') {
                cell.innerHTML = '';
                cell.style.width = '200px';

                const container = document.createElement("div");
                cell.appendChild(container);
                container.setAttribute('class', 'progressContainer');

                const bar = document.createElement("div");
                container.appendChild(bar);

                bar.setAttribute('class', 'progressBar');
                bar.setAttribute('id', uuid + '_progress');

                bar.style.width = item[`${innerItem}`] + '%';
                bar.innerHTML = item[`${innerItem}`] + '%';

            }

            if (innerItem === 'time_estimate') {
                cell.setAttribute('id', uuid + '_estimate');
            }

            if (innerItem === 'estimated_finish') {
                cell.setAttribute('id', uuid + '_finished');
            }

            if (innerItem === 'status') {
                cell.setAttribute('id', uuid + '_status');
            }
        });

        const pathBtn = document.createElement("button")
        pathBtn.innerText = `🔗`
        pathBtn.className = 'copyBtn'
        pathBtn.addEventListener('click', () => copyPath(item['output_path']), false)
        const pathCell = trow.insertCell(-1);
        pathCell.appendChild(pathBtn)

        const deleteBtn = document.createElement("button")
        deleteBtn.innerText = `☓`
        deleteBtn.className = 'copyBtn'
        deleteBtn.addEventListener('click', () => deleteEntry("", uuid), false)
        const deleteCell = trow.insertCell(-1);
        deleteCell.appendChild(deleteBtn)
    });

    const tableElement = document.getElementById("table");
    tableElement.innerHTML = "";
    tableElement.appendChild(table);
}

const copyPath = (path) => {
    navigator.clipboard.writeText(path).catch(e => console.error(e.message))
}

const clearCompleted = async (queue) => {
    const completedList = queue.filter(value => value['status'] === "Finished")

    for (const item of completedList) {
        const response = await fetch(`http://127.0.0.1:5000/api/delete/${item['uuid']}`, {
            method: 'DELETE',
            headers: {
                'Content-type': 'application/json'
            }
        });
    }

    window.location.reload()
    return completedList;
}

$(document).ready(() => {
    setInterval(
        function(){ajaxRequest()},
        2000)
})


const ajaxRequest = () => {
    $.getJSON('/api/get', function(data){
        updateProgress(data);
    })
}


const updateProgress = (data) => {
    const requests = data['results'];

    requests.forEach((item, idx) => {
        const uuid = item['uuid'];
        const progress = item['progress'];
        const time_estimate = item['time_estimate'];
        const estimated_finish = item['estimated_finish'];
        const status = item['status'];

        const bar = document.getElementById(uuid + '_progress');
        bar.style.width = progress + '%';
        bar.innerHTML = progress + '%';

        document.getElementById(uuid + '_estimate').innerHTML = time_estimate;
        document.getElementById(uuid + '_finished').innerHTML = estimated_finish;
        document.getElementById(uuid + '_status').innerHTML = status;
    });
}