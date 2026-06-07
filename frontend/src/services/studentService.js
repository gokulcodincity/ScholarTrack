import api from "./api";

export const getStudent = (studentId) =>
  api.get(`/students/${studentId}`);

export const createStudent = (data) =>
  api.post("/students", data);
