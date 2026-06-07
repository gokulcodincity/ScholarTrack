import api from "./api";

export const addReviewerNote = (data) =>
  api.post("/reviewer-notes/", data);

export const getReviewerNote = (applicationId) =>
  api.get(`/reviewer-notes/${applicationId}`);
