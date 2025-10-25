import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000/api";

export const analyzeMood = async (text) => {
  try {
    const res = await axios.post(`${BASE_URL}/analyze`, { text });
    return res.data;
  } catch (err) {
    console.error(err);
    return null;
  }
};

export const getHistory = async () => {
  try {
    const res = await axios.get(`${BASE_URL}/history`);
    return res.data;
  } catch (err) {
    console.error(err);
    return [];
  }
};
