<script>
// @ts-nocheck

  import AxiosInstance from '../auth/axiosInstance';
  import { showToast } from '../utils/toasthelper';


  let email = '';

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (email) {
      try {
        const res = await AxiosInstance.post('api/auth/password-reset/', { 'email': email });
        if (res.status === 200) {
          console.log(res.data);
          showToast("Success", 'A link to reset your password has been sent to your email', "success");
        }
      } catch (error) {
        console.error('Error submitting form:', error);
        showToast("Error", "somethign went wrong", "error")
      }
      email = "";
    }
};


</script>

<div>
  <h2>Enter your registered email</h2>
  <div class='wrapper'>
    <form on:submit={handleSubmit}>
      <div class='form-group'>
        <label for='email'>Email Address:</label>
        <input
          type='text'
          class='email-form'
          name='email'
          bind:value={email}
          on:input={(e) => email= e.target.value}
        />
      </div>
      <button class='vbtn'>Send</button>
    </form>
  </div>
</div>