import { fetch_json_with_retry } from "./fetch_data";

window.onload = function() {
    const element = document.getElementById("the_button");
    if (element) {
        console.log("Found the button!");
        element.onclick = function() {
            fetch_json_with_retry("/api/v1/test", 3, 1000)
        };
    }
}