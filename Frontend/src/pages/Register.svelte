<script>
  let email = "";
  let password = "";

  const handleRegister = () => {
    // Implement your registration logic here
  };
</script>

<div class="form-container">
  <div class="wrapper">
    <h2>Create your account</h2>
    <form action="post">
      <div class="form-group">
        <label for="">Email Address:</label>
        <input type="text" class="email-form" name="email" />
      </div>

      <div class="form-group">
        <label for="">Username:</label>
        <input type="text" class="email-form" name="username" />
      </div>

      <div class="form-group">
        <label for="">Password:</label>
        <input type="text" class="email-form" name="password" />
      </div>

      <div class="form-group">
        <label for="">Confirm Password:</label>
        <input type="text" class="email-form" name="confirm_password" />
      </div>

      <input type="submit" value="Submit" class="submitButton" />
    </form>
    <h3 class="text-option">Or</h3>

    <div class="social-container">

      <div class="githubContainer">
        <button>Sign up with Github</button>
      </div>
      <div class="googleContainer">
        <button>Sign up with Google</button>
      </div>
    </div>
    
  </div>
</div>
