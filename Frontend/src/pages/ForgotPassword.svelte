<script>
    let email = "";
  
    const handleForgotPassword = () => {
      // Implement your forgot password logic here
    };
  </script>
  
  <div>
    <h2>Forgot Password</h2>
    <form on:submit={handleForgotPassword}>
      <label>Email:</label>
      <input type="email" bind:value={email} required />
  
      <button type="submit">Reset Password</button>
    </form>
  </div>