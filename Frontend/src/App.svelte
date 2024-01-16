<script>

  import { Router, Route, Link } from "svelte-routing";
  import Login from "./pages/Login.svelte";
  import Register from "./pages/Register.svelte";
  import ForgotPassword from "./pages/ForgotPassword.svelte";
  import Index from "./pages/Index.svelte";
  import Dashboard from "./pages/Dashboard.svelte";
  import VerifyEmail from "./pages/VerifyEmail.svelte";
  import ResetPassword from "./pages/ResetPassword.svelte";

  import {ToastContainer, FlatToast} from "svelte-toasts"

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
    <Route path="/dashboard" component={Dashboard} />
    <Route path="/otp/verify" component={VerifyEmail} />
    <Route path="/password-reset/:uid/:token" component={ResetPassword} />
  </div>
</Router>

<!-- Initialize Toast -->
<ToastContainer let:data>
  <FlatToast {data} />
</ToastContainer>

<Index/>