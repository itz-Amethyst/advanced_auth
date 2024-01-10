<!-- pages/Login.svelte -->
<script>
    let email = "";
    let password = "";
  
    const handleLogin = () => {
      // Implement your login logic here
    };
  </script>
  
  <div>
    <h2>Login</h2>
    <form on:submit={handleLogin}>
      <label>Email:</label>
      <input type="email" bind:value={email} required />
  
      <label>Password:</label>
      <input type="password" bind:value={password} required />
  
      <button type="submit">Login</button>
    </form>
  </div>