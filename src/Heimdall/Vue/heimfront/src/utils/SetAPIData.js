import axios from "axios";

export async function setServerState(url, data) {
  const path = url;
  var response = null;
  var respDict = {};
  var axiosConfig = {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
    },
  };
  await axios
    .post(path, data, axiosConfig)
    .then((res) => {
      response = res;
      if (response.status === 200) {
        respDict["status"] = response.status;
        respDict["response"] = "accepted";
        respDict["data"] = response.data;
      } else {
        respDict["response"] = "declined";
        respDict["data"] = "declined";
        respDict["status"] = response.status;
      }
    })
    .catch((error) => {
      // eslint-disable-next-line
      respDict["response"] = "declined";
      respDict["data"] = "declined";
      respDict["status"] = 404;
      console.error(error);
    });
  respDict["timestamp"] = new Date().toLocaleTimeString();
  return respDict;
}
