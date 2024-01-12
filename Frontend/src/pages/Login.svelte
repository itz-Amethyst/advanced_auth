<!-- pages/Login.svelte -->
<script>

</script>

<div class="form-container">
  <div class="wrapper">
    <h2>Login to your account</h2>
    <form action="post">

      <div class="form-group">
        <label for="">Username:</label>
        <input type="text" class="email-form" name="username" />
      </div>

      <div class="form-group">
        <label for="">Password:</label>
        <input type="text" class="email-form" name="password" />
      </div>

      <input type="submit" value="Login" class="submitButton" />
    </form>
    <h3 class="text-option">Or</h3>

    <div class="social-container">
      <div class="githubContainer">
        <button>Login with Github</button>
      </div>
      <div class="googleContainer">
        <button>Login with Google</button>
      </div>
    </div>
  
  </div>
</div>
