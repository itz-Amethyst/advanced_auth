<script>
  import { capitalize } from "../utils/helper";
  import { showToast } from "../utils/toasthelper";
  import { navigate } from "svelte-routing";
  import axios from "axios";

  let formdata = {
    email: "",
    username: "",
    password: "",
    confirm_password: "",
  };

  // const { email, username, password, confirm_password } = formdata;

  $: error = "";

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
    error = "";

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/auth/register/",
        formdata
      );
      const result = response.data;

      console.log(result);
      console.log(response.status);

      if (response.status === 201) {
        navigate("/otp/verify");
        showToast("Success", result.message, "success");
      }
    } catch (error) {
      // Handle other errors
      console.error("Error:", error.response.data);
      showToast("Error", "An error occurred", "error");
    }
  };
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
