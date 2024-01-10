<script>
// @ts-nocheck

  import { Router, Route, Link } from "svelte-routing";
  import Login from "./pages/Login.svelte";
  import Register from "./pages/Register.svelte";
  import ForgotPassword from "./pages/ForgotPassword.svelte";

  export let url = ""
</script>

<style>
  .active {
    color: red;
    font-weight: bold;
  }
</style>

<!-- <Router>
  <Route path="/login" component={Login} />
  <Route path="/register" component={Register} />
  <Route path="/forgot-password" component={ForgotPassword} />
</Router> -->

<Router {url}>
  <nav>
    <a href="/">Home</a>
    <a href="/login">Login</a>
    <a href="/register">Register</a>
    <!-- <Link to="/" cla>Home</Link> -->
    <!-- <Link to="/login" active={location === '/login'}>Login</Link>
    <Link to="/register" active={location === '/register'}>Register</Link> -->
  </nav>
  <div>
    <Route path="/login" component={Login} />
    <Route path="/register" component={Register} />
    <Route path="/forgot-password" component={ForgotPassword} />
  </div>
</Router>