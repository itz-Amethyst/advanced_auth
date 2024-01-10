<script>
// @ts-nocheck

  import { Router, Route, Link } from "svelte-routing";
  import Login from "./pages/Login.svelte";
  import Register from "./pages/Register.svelte";
  import ForgotPassword from "./pages/ForgotPassword.svelte";

  export let url = ""
</script>

<!-- <Router>
  <Route path="/login" component={Login} />
  <Route path="/register" component={Register} />
  <Route path="/forgot-password" component={ForgotPassword} />
</Router> -->

<Router {url}>
  <nav>
    <Link to="/">Home</Link>
    <Link to="/login">Login</Link>
    <Link to="/register">Register</Link>
  </nav>
  <div>
    <Route path="/login" component={Login} />
    <Route path="/register" component={Register} />
    <Route path="/forgot-password" component={ForgotPassword} />
  </div>
</Router>