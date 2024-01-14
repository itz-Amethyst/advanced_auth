<script>
  import { navigate } from "svelte-routing";
  import { showToast } from "../utils/toasthelper";
  import axios from "axios";
  import { BASE_URL } from "../utils/constants";
  import axiosInstanse from "../auth/axiosInstance";

  let logindata = {
    username: "",
    password: "",
  };

  const handleOnchange = (e) => {
    logindata = { ...logindata, [e.target.name]: e.target.value };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (Object.values(logindata).some((value) => !value.trim())) {
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
        if (error.response && error.response.status === 403) {
          showToast("Error!","Invalid credentials or email not verified","error");
        } else {
          showToast("Error!", error.message, "error");
        }
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
        <input type="text" class="email-form" name="password" bind:value={logindata.password} on:change={handleOnchange}/>
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
