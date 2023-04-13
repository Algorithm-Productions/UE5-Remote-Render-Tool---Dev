async function clearCompleted(queue) {
    console.log(queue)

    const completedList = queue.filter(value => value.status === "Finished")
    console.log(completedList)

    for (const item of completedList) {
        const response = await fetch(`http://127.0.0.1:5000/api/delete/${item.uuid}`, {
            method: 'DELETE',
            headers: {
                'Content-type': 'application/json'
            }
        });

        const resData = 'resource deleted...';
    }

    window.location.reload()
}