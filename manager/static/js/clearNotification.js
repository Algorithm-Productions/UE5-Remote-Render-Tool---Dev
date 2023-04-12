async function clearNotification(notification) {
    console.log(notification)

    const response = await fetch(`http://127.0.0.1:5000/api/notification/delete/${notification.uuid}`, {
        method: 'DELETE',
        headers: {
            'Content-type': 'application/json'
        }
    });

    const resData = 'resource deleted...';

    location.reload()
    return resData;
}