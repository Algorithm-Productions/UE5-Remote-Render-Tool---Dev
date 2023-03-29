$(document).ready(function(){
    setInterval(
        function(){ajaxRequest()},
        2000)
})


function ajaxRequest(){
    $.getJSON('/api/get', function(data){
        updateProgress(data);
    })
}


function updateProgress(data){
    const requests = data.results;

    for (let i = 0; i < requests.length; i++){
        const uuid = requests[i]['uuid'];
        const progress = requests[i]['progress'];
        const time_estimate = requests[i]['time_estimate'];
        const status = requests[i]['status'];

        const bar = document.getElementById(uuid + '_progress');
        bar.style.width = progress + '%';
        bar.innerHTML = progress + '%';

        document.getElementById(uuid + '_estimate').innerHTML = time_estimate;
        document.getElementById(uuid + '_status').innerHTML = status;
    }
}