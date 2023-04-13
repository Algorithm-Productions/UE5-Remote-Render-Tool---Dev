const createArchiveTable = (list) => {
    const dataCols = ['uuid', 'name', 'owner', 'worker'];
    const metaCols = ['project_name', 'finish_time', 'total_time', 'avg_frame'];
    const table = document.createElement("table");
    const tr = table.insertRow(-1);

    dataCols.forEach((item) => {
        const theader = document.createElement("th");
        theader.innerHTML = item;
        tr.appendChild(theader);
    });

    metaCols.forEach((item) => {
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
            cell.innerHTML = item.render_request[`${innerItem}`];
        });

        metaCols.forEach((innerItem) => {
            const cell = trow.insertCell(-1);
            cell.innerHTML = item[`${innerItem}`];
        });

        const infoBtn = document.createElement("button")
        infoBtn.innerText = `ℹ`
        infoBtn.className = 'copyBtn'
        infoBtn.addEventListener('click', () => navigateToPage("archive", uuid), false)
        const infoCell = trow.insertCell(-1);
        infoCell.appendChild(infoBtn)

        const deleteBtn = document.createElement("button")
        deleteBtn.innerText = `☓`
        deleteBtn.className = 'copyBtn'
        deleteBtn.addEventListener('click', () => deleteEntry("archive", uuid), false)
        const deleteCell = trow.insertCell(-1);
        deleteCell.appendChild(deleteBtn)
    })

    const tableElement = document.getElementById("table");
    tableElement.innerHTML = "";
    tableElement.appendChild(table);
}

const handleTabSwitch = (page) => {
    document.getElementById("generalInformationSelect").classList.remove("selected");
    document.getElementById("renderStatisticsSelect").classList.remove("selected");
    document.getElementById("hardwareInfoSelect").classList.remove("selected");
    document.getElementById("outputSettingsSelect").classList.remove("selected");
    document.getElementById("aaSettingsSelect").classList.remove("selected");
    document.getElementById("consoleSettingsSelect").classList.remove("selected");
    document.getElementById("highResSettingsSelect").classList.remove("selected");

    document.getElementById(page + "Select").classList.add("selected")

    document.getElementById("generalInformation").hidden = (page !== "generalInformation");
    document.getElementById("renderStatistics").hidden = (page !== "renderStatistics");
    document.getElementById("hardwareInfo").hidden = (page !== "hardwareInfo");
    document.getElementById("outputSettings").hidden = (page !== "outputSettings");
    document.getElementById("aaSettings").hidden = (page !== "aaSettings");
    document.getElementById("consoleSettings").hidden = (page !== "consoleSettings");
    document.getElementById("highResSettings").hidden = (page !== "highResSettings");
}


const createChart = (data) => {
    const color = (getCookie("theme") === "darkmode") ? '#000' : '#F5F5F5'
    const ticksColor = (getCookie("theme") === "darkmode") ? '#000' : '#fff'

    const convertedData = data.map((item) => parseFloat(item))
    const maxVal = Math.max(...convertedData)
    const axisGrade = Math.round(maxVal + (0.15 * maxVal))

    const graphLabels = convertedData.map((item, idx) => (idx + 1).toString())
    const chrt = document.getElementById("chartId").getContext("2d");

    const chartId = new Chart(chrt, {
        type: 'bar',
        data: {
            labels: graphLabels,
            datasets: [{
                label: "Frame Render Time",
                data: convertedData,
                backgroundColor: color,
            }],
        },
        options: {
            responsive: false,
            scales: {
                yAxes: [
                    {
                        display: true,
                        ticks: {
                            suggestedMax: axisGrade,
                        },
                        grid: {
                            tickColor: ticksColor,
                        },
                        gridLines: {
                            color: ticksColor,
                        },
                    },
                ],
                xAxes: [
                    {
                        display: true,
                        gridLines: {
                            color: ticksColor,
                        },
                    }
                ],
            },
        },
    });
}


