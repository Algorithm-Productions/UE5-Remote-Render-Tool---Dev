function handleSwitch(page) {
    document.getElementById("generalInformationSelect").classList.remove("selected");
    document.getElementById("renderStatisticsSelect").classList.remove("selected");
    document.getElementById("hardwareInfoSelect").classList.remove("selected");
    document.getElementById("outputSettingsSelect").classList.remove("selected");
    document.getElementById("aaSettingsSelect").classList.remove("selected");
    document.getElementById("consoleSettingsSelect").classList.remove("selected");
    document.getElementById("highResSettingsSelect").classList.remove("selected");

    document.getElementById(page + "Select").classList.add("selected")

    document.getElementById("generalInformation").hidden = (page !== "generalInformation");
    document.getElementById("renderStatistics").hidden = (page !== "renderStatistics");
    document.getElementById("hardwareInfo").hidden = (page !== "hardwareInfo");
    document.getElementById("outputSettings").hidden = (page !== "outputSettings");
    document.getElementById("aaSettings").hidden = (page !== "aaSettings");
    document.getElementById("consoleSettings").hidden = (page !== "consoleSettings");
    document.getElementById("highResSettings").hidden = (page !== "highResSettings");
}