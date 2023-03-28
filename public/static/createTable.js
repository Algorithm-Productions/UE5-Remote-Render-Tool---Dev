function createTable(list){
    const cols = ['uid', 'name', 'owner', 'worker', 'time_created', 'status', 'priority', 'time_estimate', 'progress'];
    const table = document.createElement("table");
    const tr = table.insertRow(-1);
    for (let i = 0; i < cols.length; i++) {
        const header = document.createElement("th");
        header.innerHTML = cols[i];
        tr.appendChild(header);
    }

    for (let i = 0; i < list.length; i++) {
        const trow = table.insertRow(-1);
        const uid = list[i]['uid'];

        for (let j = 0; j < cols.length; j++) {
            const cell = trow.insertCell(-1);
            cell.innerHTML = list[i][cols[j]];

            if (cols[j] === 'progress'){
                cell.innerHTML = '';
                cell.style.width = '200px';

                var container = document.createElement("div");
                cell.appendChild(container);
                container.setAttribute('class', 'progressContainer');

                const bar = document.createElement("div");
                container.appendChild(bar);

                bar.setAttribute('class', 'progressBar');
                bar.setAttribute('id', uid + '_progress');

                bar.style.width = list[i]['progress'] + '%';
                bar.innerHTML = list[i]['progress'] + '%';

            }

            if (cols[j] === 'time_estimate'){
                cell.setAttribute('id', uid + '_estimate');
            }

            if (cols[j] === 'status'){
                cell.setAttribute('id', uid + '_status');
            }

        }
    }

    const el = document.getElementById("table");
    el.innerHTML = "";
    el.appendChild(table);
}