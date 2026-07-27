import axios from "axios";

const client = axios.create({
  baseURL: "http://localhost:8000/api",
});

export const fetchUsage = () => client.get("/usage").then(r => r.data);
export const fetchProjects = () => client.get("/projects").then(r => r.data.projects);

