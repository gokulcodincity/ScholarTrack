import api from "./api";

export const getScholarships = (params = {}) =>
  api.get("/scholarships", { params });

export const getScholarshipById = (id) =>
  api.get(`/scholarships/${id}`);

export const createScholarship = (data) =>
  api.post("/scholarships/", data);

export const getScholarshipStats = (id) =>
  api.get(`/scholarships/${id}/stats`);

export const updateScholarship = (id, data) =>
  api.patch(`/scholarships/${id}`, data);

export const deleteScholarship = (id) =>
  api.delete(`/scholarships/${id}`);
