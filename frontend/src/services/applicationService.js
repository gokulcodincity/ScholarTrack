import api from "./api";

export const createApplication = (data) =>
  api.post("/applications/", data);

export const getStudentApplications = (studentId) =>
  api.get(`/applications/student/${studentId}`);

export const getApplicationDetail = (appId) =>
  api.get(`/applications/${appId}`);

export const getReviewerApplications = (reviewerId) =>
  api.get(`/applications/reviewer/${reviewerId}`);

export const submitReview = (appId, data) =>
  api.post(`/applications/${appId}/review`, data);

export const completeReview = (appId) =>
  api.patch(`/applications/${appId}/review`);

export const submitEssay = (data) =>
  api.post("/essays/", data);

export const getEssay = (appId) =>
  api.get(`/essays/${appId}`);

export const getAllApplications = () =>
  api.get("/applications/");

export const assignReviewer = (appId, data) =>
  api.patch(`/applications/${appId}/assign`, data);

export const recordDecision = (appId, data) =>
  api.patch(`/applications/${appId}/decision`, data);
