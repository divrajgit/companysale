import axios from "axios";

const client = axios.create({
  baseURL: ".",
});

export const fetchSaleItems = () =>
  client.get("./data/sale_data.json").then((response) => {
    const payload = response.data;

    if (Array.isArray(payload)) {
      return payload;
    }

    if (payload && Array.isArray(payload.items)) {
      return payload.items;
    }

    return [];
  });
