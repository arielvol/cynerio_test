export const createErrorMessage = function (error) {
  let msg = "";
  msg = error.message;
  const details = error.response.data.message;
  if (details) {
    msg += ` Details: \n' ${details}`;
  }
  return msg;
};
