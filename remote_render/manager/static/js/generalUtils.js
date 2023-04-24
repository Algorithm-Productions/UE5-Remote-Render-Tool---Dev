const toggleMode = (page)  => {
    let currMode = getCookie("theme");
    if (currMode === "darkmode")
        currMode = "lightmode";
    else
        currMode = "darkmode";

    if (page === "archive_entry" || page === "logs_entry")
        location.href = "/set/" + currMode + "-" + page + "-" + location.href.split("/")[4];
    else
        location.href = "/set/" + currMode + "-" + page;
}

const getCookie = (name) => {
      const key = name + "=";
      const decoded = decodeURIComponent(document.cookie);
      const cookies = decoded.split('; ');

      let res;
      cookies.forEach(val => {
          if (val.indexOf(key) === 0) res = val.substring(key.length);
      })
      return res;
}

const navigateToPage = (server_url, type, uuid, args='') => {
    window.location.replace(`${server_url}/${type}/${uuid}${args}`);
}

const deleteEntry = async (server_url, key, uuid) => {
    let url = `${server_url}/api/${key}/delete/${uuid}`;
    if (key === '')
        url = `${server_url}/api/delete/${uuid}`;

    const response = await fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-type': 'application/json'
        }
    });

    window.location.reload();
    return response;
}