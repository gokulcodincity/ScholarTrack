import api from "./api";

export const getPendingReviewers = () =>
  api.get("/admin/pending-reviewers");

export const getActiveReviewers = () =>
  api.get("/admin/reviewers");

export const approveReviewer = (userId) =>
  api.patch(`/admin/users/${userId}/approve-reviewer`);

export const rejectReviewer = (userId) =>
  api.patch(`/admin/users/${userId}/reject-reviewer`);

export const getReviewerResumeUrl = (userId) =>
  `/admin/reviewer-requests/${userId}/resume`; // Used for blob downloading manually

export const updateDecision = (decisionId, data) =>
  api.patch(`/admin/decisions/${decisionId}`, data);

export const createDecision = (data) =>
  api.post("/admin/decisions", data);

export const getAllDecisions = () =>
  api.get("/admin/decisions");

export const getDecisionById = (decisionId) =>
  api.get(`/admin/decisions/${decisionId}`);

export const getApplicationDecision = (applicationId) =>
  api.get(`/admin/applications/${applicationId}/decision`);

export const deleteDecision = (decisionId) =>
  api.delete(`/admin/decisions/${decisionId}`);
