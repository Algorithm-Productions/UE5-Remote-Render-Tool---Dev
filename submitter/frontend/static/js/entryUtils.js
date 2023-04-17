const handleTabSwitch = (page) => {
    document.getElementById("basicSettingsSelect").classList.remove("selected");
    document.getElementById("outputSettingsSelect").classList.remove("selected");

    document.getElementById(page + "Select").classList.add("selected")

    document.getElementById("basicSettings").hidden = (page !== "basicSettings");
    document.getElementById("outputSettings").hidden = (page !== "outputSettings");
}

const submitForm = () => {
    const basicSettingsForm = document.getElementById("basicSettingsForm")

    const basicSettings = {
        'name': basicSettingsForm.elements.name.value,
        'owner': '',
        'worker': basicSettingsForm.elements.worker.value,
        'project_path': basicSettingsForm.elements.project_path.value,
        'level_path': basicSettingsForm.elements.level_path.value,
        'sequence_path': basicSettingsForm.elements.sequence_path.value,
        'config_path': basicSettingsForm.elements.config_path.value,
        'output_path': basicSettingsForm.elements.output_path.value
    }

    eel.send_request(basicSettings)(callBack)
}

const callBack = (res) => {
    if (res === "200")
        window.location.href = "landing.html"
    else {
        document.getElementById("notificationWrapper").hidden = false
        document.getElementById("notificationText").innerText = res
    }
}