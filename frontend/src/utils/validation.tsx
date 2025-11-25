// src/utils/validation.ts

// Regex for password validation
export const passwordRegex = /^[a-zA-Z0-9{}:"<>,./;'[\]\\$]{8,}$/;

// Function wrapper for clarity
export const isValidPassword = (password: string): boolean => {
  return passwordRegex.test(password);
};

export const validatePassword = (password: string): string[] => {
  const errors: string[] = [];

  if (password.length < 8) {
    errors.push("Password must be at least 8 characters long.");
  }
  if (!/[A-Z]/.test(password)) {
    errors.push("Password must contain at least one uppercase letter (A-Z).");
  }
  if (!/[a-z]/.test(password)) {
    errors.push("Password must contain at least one lowercase letter (a-z).");
  }
  if (!/[0-9]/.test(password)) {
    errors.push("Password must contain at least one number (0-9).");
  }
  if (!/[{}:"<>,./;'[\]\\$]/.test(password)) {
    errors.push("Password must contain at least one special character ({}:\"<>,./;'[]\\$).");
  }

  return errors;
};
