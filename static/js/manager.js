// ! goes through the elements and checks if their valid
// ! if they are valid, then the button is cickable, if not it is greyed out
async function CheckInputs() {
  var username = document.getElementById("username");
  var password = document.getElementById("password");
  var DOB = document.getElementById("DOB");
  var btn = document.getElementById("btn");

  if (username.value.length >= 4) {
    if (username.value.length <= 20) {
      if (IsStrongPassword(password.value)) {
        if (IsValidDate(DOB.value)) {
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
            "Date must be older then 13 years and younger than 120";
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

// ! simply greys out the btn given
function GreyOutButton(btn) {
  btn.disabled = true;
  btn.style.cursor = "default";
  btn.style.color = "grey";
}

// ! when given a password, returns true if meets all requirements, and false if not
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

// ! runs a get request to the flask server to check if the username exists
// NOTE should only run when nessiasry, expesive and sensitive data retrieval
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

// ! checks if the date is valid and if the user is older then 13 and younger then 120
function IsValidDate(date) {
  newDate = new Date(date);
  console.log(new Date().getFullYear() - 13);
  if (newDate != "Invalid Date") {
    if (
      new Date().getFullYear() - 13 > newDate.getFullYear() &&
      new Date().getFullYear() - 120 < newDate.getFullYear()
    ) {
      return true;
    }
  }
  return false;
}

// ! adds event listeners to all input fields as to call the CheckInputs() function only when needed
document.addEventListener("DOMContentLoaded", function () {
  const inputFields = document.querySelectorAll(".input__field");
  text = document.getElementById("description_text");

  inputFields.forEach((input) => {
    input.addEventListener("input", CheckInputs);
  });

  CheckInputs();
});
