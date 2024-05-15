function togglePassword() {
  var passwordInput = document.getElementById('password');
  passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
}

function togglePasswordRegister(passwordId, confirmId) {
  var passwordInput = document.getElementById(passwordId);
  var confirmInput = document.getElementById(confirmId);
  var type = passwordInput.type === 'password' ? 'text' : 'password';
  passwordInput.type = type;
  confirmInput.type = type;
}
