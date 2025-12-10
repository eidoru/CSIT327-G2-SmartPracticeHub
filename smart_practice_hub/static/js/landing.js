document.addEventListener("DOMContentLoaded", () => {
    const loginButton = document.getElementById("loginButton")
    const loginButtonSignupDialog = document.getElementById("loginButtonSignupDialog")
    const loginDialog = document.getElementById("loginDialog")

    const signupButton = document.getElementById("signupButton")
    const signupButtonLoginDialog = document.getElementById("signupButtonLoginDialog")
    const signupDialog = document.getElementById("signupDialog")

    loginButton.addEventListener("click", () => {
        loginDialog.showModal();
    });

    loginButtonSignupDialog.addEventListener("click", () => {
        signupDialog.close();
        loginDialog.showModal();
    });

    signupButton.addEventListener("click", () => {
        signupDialog.showModal();
    });

    signupButtonLoginDialog.addEventListener("click", () => {
        loginDialog.close();
        signupDialog.showModal();
    });
});
