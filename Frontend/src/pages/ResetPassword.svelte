<script>
  import {onMount} from "svelte"
  import { navigate } from "svelte-routing";
  import { capitalize } from "../utils/helper";
  import { showToast } from "../utils/toasthelper";
  import axiosInstanse from "../auth/axiosInstance";
  import { checkIsFormFilled } from "../utils/helper";

  let formdata = {
    password: "",
    confirm_password: "",
  };

  let uid;
  let token;
  
  const handleOnChange = (e) => {
    formdata = { ...formdata, [e.target.name]: e.target.value };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!checkIsFormFilled(formdata)) {
      showToast("Error", "You must filled all the blanks", "error");
      return;
    }

    if (formdata.password !== formdata.confirm_password) {
      showToast("Error", "Passwords do not match", "info");
      return;
    }

    try {
      const baseURI = e.target.baseURI
      console.log(baseURI);

      const segments = baseURI.split("/");
      uid = segments[segments.length - 3];
      token = segments[segments.length - 2];

      const res = await axiosInstanse.patch("api/auth/set-new-password/", {
        password: formdata.password,
        confirm_password: formdata.confirm_password,
        uidb64: uid,
        token: token,
      });
      const response = res.data;
      if (res.status === 200) {
        navigate("/login");
        showToast("Success", response.message, "success");
      }
      console.log(response);
    } catch (error) {
      console.log(error.response.data.detail);
      showToast("Error", error.response.data.detail, "error")
    }
  };
</script>

<div>
  <div class="form-container">
    <div class="wrapper" style="width: 100%;">
      <h2>Enter your New Password</h2>
      <form on:submit={handleSubmit}>
        {#each Object.entries(formdata) as [key, value] (key)}
          <div class="form-group">
            <label for={key}>{capitalize(key.replace("_", " "))}: </label>
            <input
              type="password"
              class="password-form"
              minlength=6
              name={key}
              bind:value={formdata[key]}
              on:input={handleOnChange}
            />
          </div>
        {/each}
        <button type="submit" class="vbtn">Submit</button>
      </form>
    </div>
  </div>
</div>
