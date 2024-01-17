<script>
  import { Link, navigate } from "svelte-routing";
  import { showToast } from "../utils/toasthelper";
  import axiosInstanse from "../auth/axiosInstance";
  import {checkIsFormFilled} from "../utils/helper"
  import { onMount } from "svelte";
  import axios from "axios";
  import { BASE_URL } from "../utils/constants";

  let logindata = {
    username: "",
    password: "",
  };


  
  // Google
  const handleSigninWithGoogle = async (response) => {
    try{

      const payload = response.credential;
      const server_res = await axios.post(`${BASE_URL}/api/external-auth/google/`,{ access_token: payload });
      console.log(server_res.data);

      const user = {
        username: server_res.data.username,
        email: server_res.data.email,
      };

      if (server_res.status === 200) {
        localStorage.setItem("token", JSON.stringify(server_res.data.access_token));
        localStorage.setItem("refresh_token",JSON.stringify(server_res.data.refresh_token));
        localStorage.setItem("user", JSON.stringify(user));

        await navigate("/dashboard");
        showToast("Success", "login successful", "info");
      }
    }
    catch (error){
      console.log(error.response.data);
      showToast("Error", error.response.data.detail, "error")
    }
   
  };


  onMount(() => {
    google.accounts.id.initialize({
      client_id: "614714357603-3fqkav8io8506kikkiuou7qco3gefk8e.apps.googleusercontent.com",
      callback: handleSigninWithGoogle,
    });
    google.accounts.id.renderButton(
      document.getElementById("signInDiv"),
      { theme: "outline", size: "large", text: "continue_with", shape: "circle", width: "280" }
    );
  });



  const handleOnchange = (e) => {
    logindata = { ...logindata, [e.target.name]: e.target.value };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!checkIsFormFilled(logindata)) {
      showToast("Error", "Please fill in all the fields", "error");
      return;
    }

    if (logindata) {
      try {
        const res = await axiosInstanse.post("/api/auth/login/", logindata);
        const response = res.data;

        const user = {
          username: response.username,
          email: response.email,
        };

        if (res.status === 200) {
          localStorage.setItem("token", JSON.stringify(response.access_token));
          localStorage.setItem(
            "refresh_token",
            JSON.stringify(response.refresh_token)
          );
          localStorage.setItem("user", JSON.stringify(user));

          await navigate("/dashboard");
          showToast("Success", "login successful", "info");
        }
      } catch (error) {
        console.log(error.response.data.detail);
        showToast("Error", error.response.data.detail, "error")
      }
    }
  };
</script>

<div class="form-container">
  <div class="wrapper">
    <h2>Login to your account</h2>
    <form action="post" on:submit={handleSubmit}>
      <div class="form-group">
        <label for="">Username:</label>
        <input type="text" class="email-form" name="username" bind:value={logindata.username} on:change={handleOnchange}/>
      </div>

      <div class="form-group">
        <label for="">Password:</label>
        <input type="password" class="email-form" name="password" bind:value={logindata.password} on:change={handleOnchange}/>
      </div>

      <input type="submit" value="Login" class="submitButton" />

      <p class='pass-link'><Link to={'/forgot-password'}>forgot password</Link></p>
    </form>
    <h3 class="text-option">Or</h3>

    <div class="social-container">
      <div class="githubContainer">
        <button>Continue with Github</button>
      </div>
      <div class="googleContainer">
        <!-- <button>Login with Google</button> -->
        <div id="signInDiv" class="gsignIn"></div>
      </div>
    </div>
  </div>
</div>
