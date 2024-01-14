<script>
  import { onMount } from "svelte";
  import { navigate } from "svelte-routing";
  import {BASE_URL} from "../utils/constants"
  import axios from "axios";
  import { showToast } from "../utils/toasthelper";


  let jwt = localStorage.getItem("token");
  let user = JSON.parse(localStorage.getItem("user"));
  let refresh = JSON.parse(localStorage.getItem("refresh_token"));

  onMount(() => {
    if (jwt === null && !user) {
      navigate("/login");
    }
    //  else {
    //   fetchData();
    // }
  });

//   const fetchData = async () => {
//     try {
//       const res = await axios.get(`${BASE_URL}/auth/get-something/`);
//       console.log(res.data);
//     } catch (error) {
//       console.error("Error:", error);
//     }
//   };

  const handleLogout = async () => {
    try {
      const res = await axios.post(`${BASE_URL}/api/auth/logout/`, {
        refresh_token: refresh,
      });
      if (res.status === 204) {
        localStorage.removeItem("token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");
        navigate("/login");
        showToast("Info", "Logged out successfully", "info")
      }
    } catch (error) {
      console.error("Error:", error);
      showToast("Error", "something went wrong", "error")
    }
  };
</script>

<div class="container">
  <h2>
    hi {#if user}{user.username}{/if}
  </h2>
  <p style="text-align:center;">welcome to your profile</p>
  <button on:click={handleLogout} class="logout-btn">Logout</button>
</div>
