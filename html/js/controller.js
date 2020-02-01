var id = Math.round(Math.random() * 10000000000);

function post_to_server(dir) {
    var xhttp = new XMLHttpRequest();
    var url = document.getElementById("ip").value;
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("id=" + id + "&dir=" + dir);
}

window.onbeforeunload = function() {
    this.post_to_server("kill");
    return true;
};

function butt_top_left_click() {
    post_to_server("tl");
}
function butt_top_click() {
    post_to_server("t");
}
function butt_top_right_click() {
    post_to_server("tr");
}
function butt_middle_click() {
    alert(id);
}
function butt_bottom_left_click() {
    post_to_server("bl");
}
function butt_bottom_click() {
    post_to_server("b");
}
function butt_bottom_right_click() {
    post_to_server("br");
}
