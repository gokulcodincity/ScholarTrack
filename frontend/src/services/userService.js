import api from "./api";

export const getAllUsers = () =>
  api.get("/users/");

export const getUserById = (userId) =>
  api.get(`/users/${userId}`);
