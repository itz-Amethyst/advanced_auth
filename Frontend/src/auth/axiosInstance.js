import axios from "axios";
import { BASE_URL } from "../utils/constants";
import dayjs from "dayjs";
import { jwtDecode } from "jwt-decode";


const CancelToken = axios.CancelToken;
const source = CancelToken.source();

let accessToken = localStorage.getItem("token") ? JSON.parse(localStorage.getItem("token")) : ""
let refresh_token = localStorage.getItem("refresh_token") ? JSON.parse(localStorage.getItem("refresh_token")) : ""

const axiosInstanse = axios.create({
    baseURL:BASE_URL,
    cancelToken: source.token,
    headers: {
        Authorization: localStorage.getItem('token') ? `Bearer ${accessToken}` : ""
    }
})

axiosInstanse.interceptors.request.use(async req => {
    if (accessToken) {
        req.headers.Authorization = localStorage.getItem('token') ? `Bearer ${accessToken}` : ""
        const user = jwtDecode(accessToken)
        const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1
        if (!isExpired) {
            console.log("not expired");
            return req
        }
        
        console.log("isExpired:", isExpired)
        const res = await axios.post(`${BASE_URL}/api/auth/token/refresh/`, {refresh: refresh_token})
        console.log('new_accesstoken: ',res.data.access)
        localStorage.setItem('token', JSON.stringify(res.data.access))
        req.headers.Authorization = `Bearer ${res.data.access}`
        return req
    }

    else {
        req.headers.Authorization = localStorage.getItem('token') ? `Bearer ${JSON.parse(localStorage.getItem('token'))}` : " "
        return req 
    }
});
export default axiosInstanse