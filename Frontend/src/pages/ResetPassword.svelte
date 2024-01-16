<script>
  import { navigate } from "svelte-routing";
  import { capitalize } from "../utils/helper";
  import { showToast } from "../utils/toasthelper";
  import axiosInstanse from "../auth/axiosInstance";


  let formdata = {
    password: "",
    confirm_password: "",
  };

  const isFormFilled = () => {
    return Object.values(formdata).every((value) => value.trim() !== "");
  };

  const handleOnChange = (e) => {
    formdata = { ...formdata, [e.target.name]: e.target.value };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isFormFilled()) {
      try {
        const res = await axiosInstanse.patch("api/auth/set-new-password/", {
          password: formdata.password,
          confirm_password: formdata.confirm_password,
          uidb64: e.useParams.uid,
          token: e.useParams.token,
        });
        const response = res.data;
        if (res.status === 200) {
          navigate("/login");
          showToast("Success", response.message, "success");
        }
        console.log(response);
      } catch (error) {
        console.error("Error submitting form:", error);
      }
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
