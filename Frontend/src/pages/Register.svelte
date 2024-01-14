<script>
  import {toasts} from 'svelte-toasts'
  import { writable } from 'svelte/store'
  import { capitalize } from "../utils/helper";
  import { showToast, showToastInfDuration } from "../utils/toasthelper";
  import { navigate } from "svelte-routing";
  import axios from "axios";
  import { BASE_URL } from '../utils/constants';

  let formdata = {
    email: "",
    username: "",
    password: "",
    confirm_password: "",
  };

  $: loading = writable(false);
  $: clear = writable(false)

  const handleOnChange = (e) => {
    formdata = { ...formdata, [e.target.name]: e.target.value };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (Object.values(formdata).some((value) => !value.trim())) {
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
      const response = await axios.post(`${BASE_URL}/api/auth/register/`,formdata);
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
      console.error("Error:", error.response.data);
      showToast("Error", "An error occurred", "error");
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
        <button>Sign up with Google</button>
      </div>
    </div>
  </div>
</div>
