let text;

function CheckInputs() {
  var username = document.getElementById("username");
  var password = document.getElementById("password");
  var DOB = document.getElementById("DOB");
  var btn = document.getElementById("btn");

  if (username.value != "") {
    if (IsStrongPassword(password.value)) {
      if (IsValidDate(DOB.value)) {
        text.textContent = "";
        btn.disabled = false;
        btn.style.cursor = "pointer";
        btn.style.color = "black";
      } else {
        text.textContent = "Date must be in a DD/MM/YYYY format";
        btn.disabled = true;
        btn.style.cursor = "default";
        btn.style.color = "grey";
      }
    } else {
      text.textContent =
        "A password must be at least 8 letters, have one capital letter and one special character";
      btn.disabled = true;
      btn.style.cursor = "default";
      btn.style.color = "grey";
    }
  } else {
    text.textContent = "Must be a vaild username";
    btn.disabled = true;
    btn.style.cursor = "default";
    btn.style.color = "grey";
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

function IsValidDate(dateString) {
  const regex = /^(0[1-9]|1[0-2])\/([0-2][0-9]|3[01])\/\d{4}$/;
  if (!regex.test(dateString)) {
    return false;
  }

  const [month, day, year] = dateString.split("/").map(Number);
  const date = new Date(year, month - 1, day);

  return (
    date.getMonth() === month - 1 &&
    date.getDate() === day &&
    date.getFullYear() === year
  );
}

document.addEventListener("DOMContentLoaded", function () {
  const inputFields = document.querySelectorAll(".input__field");
  text = document.getElementById("description_text");

  inputFields.forEach((input) => {
    input.addEventListener("input", CheckInputs);
  });

  CheckInputs();
});
