<script>
  import { writable } from "svelte/store";

  import AxiosInstance from "../auth/axiosInstance";
  import { showToast, showToastInfDuration } from "../utils/toasthelper";
  import { toasts } from "svelte-toasts";

  $: loading = writable(false);
  $: clear = writable(false);

  let email = "";

  const handleSubmit = async (e) => {
    loading.set(true);
    e.preventDefault();
    if (email) {
      try {
        const res = await AxiosInstance.post("api/auth/password-reset/", {email: email,});
        if (res.status === 200) {
          console.log(res.data);
          setTimeout(() => {
            showToast("Success", res.data.message, "success");
          }, 1000);
        }
      } catch (error) {
        console.log(error.response.data.detail);
        showToast("Error", error.response.data.detail, "error");
      }
      loading.set(false);
      clear.set(true);
      email = "";
    }
  };

  $: if ($loading && !$clear) {
    showToastInfDuration();
  }

  $: if ($clear) {
    toasts.clearAll();
  }
</script>

<div>
  <div class="form-container">
    <div style="width: 100%;" class="wrapper">
      <h2>Enter your registered email</h2>
      <form on:submit={handleSubmit}>
        <div class="form-group">
          <label for="email">Email Address:</label>
          <input
            type="email"
            class="email-form"
            name="email"
            bind:value={email}
            on:input={(e) => (email = e.target.value)}
          />
        </div>
        <button class="vbtn">Send</button>
      </form>
    </div>
  </div>
</div>
