let button = document.getElementById("auth2");

let endpoint = "https://accounts.google.com/o/oauth2/v2/auth";
let info = {
  clientId:
    "48231090303-eelp5r7prhev89t13ng9mt8f609pqqhg.apps.googleusercontent.com",
  redirectUri: "http://localhost:8000/auth/api/v1/google/token",
  responseType: "token",
  scope:
    "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
  state: "letslogin",
  loginHint: "sungwook.csw@gmail.com", // optional
};

button.addEventListener("click", function (event) {
  let { clientId, redirectUri, responseType, scope, state, loginHint } = info;
  let uri = `${endpoint}?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=${responseType}&scope=${scope}&state=${state}&login_hint=${loginHint}`;
  window.location.href = uri;
});
