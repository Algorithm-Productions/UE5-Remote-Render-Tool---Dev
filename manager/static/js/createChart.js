function createChart(data) {
    const color = (getCookie("theme") === "darkmode") ? '#000' : '#F5F5F5'
    const ticksColor = (getCookie("theme") === "darkmode") ? '#000' : '#fff'


    const convertedData = data.map((item) => parseFloat(item))
    const maxVal = Math.max(...convertedData)
    const axisGrade = Math.round(maxVal + (0.15*maxVal))
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