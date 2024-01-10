<script>
    let email = "";
    let password = "";
  
    const handleRegister = () => {
      // Implement your registration logic here
    };
  </script>
  
  <div>
    <h2>Register</h2>
    <form on:submit={handleRegister}>
      <label>Email:</label>
      <input type="email" bind:value={email} required />
  
      <label>Password:</label>
      <input type="password" bind:value={password} required />
  
      <button type="submit">Register</button>
    </form>
  </div>