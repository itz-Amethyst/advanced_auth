<script>
  import {BASE_URL} from "../utils/constants"
  import { navigate } from "svelte-routing";
  import { showToast } from "../utils/toasthelper";
  import { isValidInput } from "../utils/helper";
  import axiosInstance from "../auth/axiosInstance";

  let otpCode = "";

  const handleOtpSubmit = async (e) => {
    e.preventDefault();

    if (!isValidInput(otpCode)) {
      showToast("Error","Invalid input. Please enter a positive integer.","error");
      return;
    }

    try {
      console.log(BASE_URL);
      const res = await axiosInstance.post(`${BASE_URL}/api/auth/verify/`, {
        otp_code: otpCode,
      });

      const resp = res.data;

      if (res.status === 200) {
        navigate("/login");
        showToast("Success", resp.message, "success");
      }

    } catch (error) {
      showToast("Error", error.response.data.message, "error");
    }
  };
</script>

<div class="form-container">
  <div class="wrapper">
    <h2>Verify your account</h2>
    <form action="post" on:submit={handleOtpSubmit}>
      <div class="form-group">
        <label for="">Otp Code:</label>
        <input
          type="text"
          class="email-form"
          name="otpCode"
          bind:value={otpCode}
        />
      </div>
      <input type="submit" class="vbtn" value="Submit" />
    </form>
  </div>
</div>
