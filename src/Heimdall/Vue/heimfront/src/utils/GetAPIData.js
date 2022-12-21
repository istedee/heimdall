import axios from "axios";

export async function getServerState(url) {
  const path = url;
  var response = null;
  var respDict = {};
  await axios
    .get(path)
    .then((res) => {
      response = res;
      if (response.status === 200) {
        respDict["status"] = "online";
        respDict["data"] = response.data;
      } else respDict["status"] = "offline";
    })
    .catch((error) => {
      // eslint-disable-next-line
      respDict["status"] = "offline";
      respDict["data"] = "offline";
      console.error(error);
    });
  respDict["timestamp"] = new Date().toLocaleTimeString();
  return respDict;
}
