const handleTabSwitch = (page) => {
    document.getElementById("basicSettingsSelect").classList.remove("selected");
    document.getElementById("outputSettingsSelect").classList.remove("selected");
    document.getElementById("aaSettingsSelect").classList.remove("selected");

    document.getElementById(page + "Select").classList.add("selected")

    document.getElementById("basicSettings").hidden = (page !== "basicSettings");
    document.getElementById("outputSettings").hidden = (page !== "outputSettings");
    document.getElementById("aaSettings").hidden = (page !== "aaSettings");
}

const changeCheckBox = (target, secondary='') => {
    const element = document.getElementById(target)
    if (element.disabled)
        element.disabled = false
    else {
        element.disabled = true
        element.value = ""
        if (element.type === "select-one")
            element.value = "False"

        if (secondary !== '') {
            document.getElementById(secondary).disabled = true
            document.getElementById(secondary).hidden = true
        }
    }
}

const toggleValue = (event, value='', inner = '') => {
    document.getElementById(event.target.id).value = event.target.value
    if (value !== '') {
        document.getElementById(value).hidden = event.target.value === "False"
        if (inner !== '') {
            const split = inner.split(";")
            split.forEach((element) => {
                document.getElementById(element).value = ""
                document.getElementById(element).disabled = true
                document.getElementById(element + "Flag").checked = false
            })
        }
    }
}
