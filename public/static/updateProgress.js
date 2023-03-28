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
        const uid = requests[i]['uid'];
        const progress = requests[i]['progress'];
        const time_estimate = requests[i]['time_estimate'];
        const status = requests[i]['status'];

        const bar = document.getElementById(uid + '_progress');
        bar.style.width = progress + '%';
        bar.innerHTML = progress + '%';

        document.getElementById(uid + '_estimate').innerHTML = time_estimate;
        document.getElementById(uid + '_status').innerHTML = status;
    }
}