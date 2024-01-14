import axios from "axios";
import { BASE_URL } from "../utils/constants";

const token = localStorage.getItem("access") ? JSON.parse(localStorage.getItem("access")) : ""
const refresh_token = localStorage.getItem("refresh_token") ? JSON.parse(localStorage.getItem("refresh_token")) : ""

const axiosInstanse = axios.create({
    baseURL:BASE_URL,
    headers: {
        Authorization: localStorage.getItem('access') ? `Bearer ${token}` : null
    }
})

export default axiosInstanse