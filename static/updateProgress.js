// run ajax request to auto update progress field

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
    var requests = data.results;

    for (var i = 0; i < requests.length; i++){
        var uuid = requests[i]['uuid'];
        var progress = requests[i]['progress'];
        var time_estimate = requests[i]['time_estimate'];
        var status = requests[i]['status'];

        var bar = document.getElementById(uuid + '_progress');
        bar.style.width = progress + '%';
        bar.innerHTML = progress + '%';

        document.getElementById(uuid + '_estimate').innerHTML = time_estimate;
        document.getElementById(uuid + '_status').innerHTML = status;
    }
}