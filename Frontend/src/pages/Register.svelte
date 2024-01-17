<script>
  import { toasts } from "svelte-toasts";
  import { writable } from "svelte/store";
  import { capitalize, checkIsFormFilled } from "../utils/helper";
  import { showToast, showToastInfDuration } from "../utils/toasthelper";
  import { navigate } from "svelte-routing";
  import { BASE_URL } from "../utils/constants";
  import axiosInstanse from "../auth/axiosInstance";
  import axios from "axios";
  import { onMount } from "svelte";

  let formdata = {
    email: "",
    username: "",
    password: "",
    confirm_password: "",
  };

  $: loading = writable(false);
  $: clear = writable(false);

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
      client_id: import.meta.env.VITE_CLIENT_ID,
      callback: handleSigninWithGoogle,
    });
    google.accounts.id.renderButton(
      document.getElementById("signInDiv"),
      { theme: "outline", size: "large", text: "continue_with", shape: "circle", width: "280" }
    );
  });


  const handleOnChange = (e) => {
    formdata = { ...formdata, [e.target.name]: e.target.value };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!checkIsFormFilled(formdata)) {
      showToast("Error", "Please fill in all the fields", "error");
      return;
    }

    if (formdata.password !== formdata.confirm_password) {
      showToast("Error", "Passwords do not match", "error");
      return;
    }

    console.log(formdata);

    try {
      loading.set(true)
      const response = await axiosInstanse.post(`${BASE_URL}/api/auth/register/`,formdata);
      const result = response.data;

      console.log(result);
      console.log(response.status);

      if (response.status === 201) {
        navigate("/otp/verify");
        setTimeout(() => {
          showToast("Success", result.message, "success");
        }, 1000);
      }
    } catch (error) {
      // Handle other errors
      console.log(error.response.data.detail);
      showToast("Error", error.response.data.detail, "error")
    }
    loading.set(false)
    clear.set(true)
  };

  $: if ($loading && !$clear) {
    showToastInfDuration();
  }

  $: if ($clear) {
    toasts.clearAll()
  }
</script>

<div>
  <div class="form-container">
    <div style="width: 100%;" class="wrapper">
      <h2>create account</h2>
      <form on:submit={handleSubmit}>
        {#each Object.entries(formdata) as [key, value] (key)}
          <div class="form-group">
            <label for={key}>{capitalize(key.replace("_", " "))}: </label>
            {#if key === "email"}
              <input
                type="email"
                class="email-form"
                name={key}
                bind:value={formdata[key]}
                on:input={handleOnChange}
              />
            {:else if key === "password" || key === "confirm_password"}
              <input
                type="password"
                class="password-form"
                minlength=6
                name={key}
                bind:value={formdata[key]}
                on:input={handleOnChange}
              />
            {:else}
              <input
                type="text"
                class="text-form"
                name={key}
                bind:value={formdata[key]}
                on:input={handleOnChange}
              />
            {/if}
          </div>
        {/each}
        <input type="submit" value="Submit" class="submitButton" />
      </form>
      <h3 class="text-option">Or</h3>
      <div class="githubContainer">
        <button>Sign up with Github</button>
      </div>
      <div class="googleContainer">
        <!-- <button>Sign up with Google</button> -->
        <div id="signInDiv" class="gsignIn"></div>
      </div>
    </div>
  </div>
</div>
