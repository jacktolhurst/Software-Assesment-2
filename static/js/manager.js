window.setInterval(CheckPassword, 20);

function CheckPassword() {
  var password = document.getElementById("password").value;
  if (IsStrongPassword(password)) {
    var btn = document.getElementById("btn");
    btn.style.color = "black";
    btn.disabled = false;
  } else {
    var btn = document.getElementById("btn");
    btn.style.color = "grey";
    btn.disabled = true;
  }
}

function IsStrongPassword(password) {
  if (password.length < 8 || password.length > 20) {
    return false;
  }
  if (!/[A-Za-z]/.test(password)) {
    return false;
  }
  if (!/[a-z]/.test(password)) {
    return false;
  }
  if (!/[0-9]/.test(password)) {
    return false;
  }
  if (!/[@$!%?&#]/.test(password)) {
    return false;
  }
  return true;
}
