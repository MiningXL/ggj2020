function post_to_server(dir) {
    var xhttp = new XMLHttpRequest();
    var url = "http://localhost:8080";
    var id = "0";
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("var1=" + id + "&var2=" + dir);
}

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
    post_to_server("m");
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
