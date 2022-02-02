function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
    }
    return "";
}

function stayLoggedIn() {
    setCookie("logged_in","true",30);
    setCookie("username", username,30);
    setCookie("password",encryptedPassword,30);
    return null;
}

window.onload {
    var loggedIn = getCookie("logged_in");
    if(loggedIn == true) {
        var username = getCookie("username");
        var password = getCookie("password");
        var usernameTextBox = document.getElementById("username");
        var passwordTextBox = document.getElementById("password");
//decrypt password here.
        usernameTextBox.value = username;
        passwordTextBox.value = password;
    }
    else {}
}