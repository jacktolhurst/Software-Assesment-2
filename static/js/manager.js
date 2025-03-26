async function CheckInputs() {
  var username = document.getElementById("username");
  var password = document.getElementById("password");
  var DOB = document.getElementById("DOB");
  var btn = document.getElementById("btn");

  if (username.value.length >= 4) {
    if (username.value.length <= 20) {
      if (IsStrongPassword(password.value)) {
        if (!(await IsPreExistingUsername(username.value))) {
          text.textContent = "";
          btn.disabled = false;
          btn.style.cursor = "pointer";
          btn.style.color = "black";
        } else {
          text.textContent = "This username is already in use.";
          GreyOutButton(btn);
        }
      } else {
        text.textContent =
          "A password must be at least 8 letters, have one capital letter and one special character";
        GreyOutButton(btn);
      }
    } else {
      text.textContent = "This username is too long";
      GreyOutButton(btn);
    }
  } else {
    text.textContent = "This username is too short";
    GreyOutButton(btn);
  }
}

function GreyOutButton(btn) {
  btn.disabled = true;
  btn.style.cursor = "default";
  btn.style.color = "grey";
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

function IsPreExistingUsername(username) {
  return fetch(`/checkDB?username=${username}`)
    .then((response) => response.json())
    .then((data) => {
      return data.result;
    })
    .catch((error) => {
      console.error("Error:", error);
      return false;
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const inputFields = document.querySelectorAll(".input__field");
  text = document.getElementById("description_text");

  inputFields.forEach((input) => {
    input.addEventListener("input", CheckInputs);
  });

  CheckInputs();
});
