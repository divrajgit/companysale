import axios from "axios";

const client = axios.create({
  baseURL: ".",
});

export const fetchSaleItems = () =>
  client.get("./data/sale_data.json").then((response) => response.data.items || []);
