function createChart(data) {
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
                backgroundColor: '#000',
            }],
        },
        options: {
            responsive: false,
            scales: {
                yAxes: [
                    {
                        display: true,
                        ticks: {
                            suggestedMax: axisGrade
                        }
                    }
                ]
            },
        },
    });
}