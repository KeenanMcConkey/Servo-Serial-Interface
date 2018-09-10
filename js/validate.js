function validateIncremental() {
    var cts = document.getElementById("cts").checked;
    var stopAngle = document.getElementById("stopAngle").value;
    var incAngle = document.getElementById("incAngle").value;

    if (incAngle == "") {
        alert("Select an increment angle!");
        return false;
    }
    if (cts && stopAngle == "") {
        alert("Select a stop angle when using continuous increments!");
        return false;
    }

}
function validateSpecific() {
    var angle = document.getElementById("angle").value;

    if (angle == "") {
        alert("Select an angle!");
        return false;
    }
}
