<template>
  <card class="card" title=" ">

    <!--Stats cards-->
    <div class="row">
      <div class="col-md-6 col-xl-4" v-for="stats in statsCards" :key="stats.title">
        <stats-card>
          <div class="icon-big text-center" :class="`icon-${stats.type}`" slot="header">
            <i :class="stats.icon"></i>
          </div>
          <div class="numbers" slot="content">
            <p>{{stats.title}}</p>
            {{stats.value}}
          </div>
          <fg-input type="text"
                      :disabled="false"
                      placeholder=""
                      v-model="stats.info">
            </fg-input>
        </stats-card>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6 col-xl-6" v-for="stats in checkBox" :key="stats.title">
        <stats-card>
          <div class="icon-big text-center" :class="`icon-${stats.type}`" slot="header">
            <i>{{stats.title}}</i>
          </div>
          <div class="numbers" slot="content">
            {{stats.value}}
          </div>
          <fg-input type="checkbox"
                      :checked="stats.info"
                      >
            </fg-input>
        </stats-card>
      </div>
    </div>
    <div>
        <div class="text-center">
          <p-button type="info"
                    round
                    @click.native.prevent="setServerState">
            Update Configuration
          </p-button>
        </div>
        <div class="clearfix"></div>
      </form>
    </div>
  </card>
</template>
<script>
import { getServerState } from '@/utils/GetAPIData';
import { setServerState } from '@/utils/SetAPIData';
import 'vue-notifyjs/themes/default.css'
export default {
  data() {
    return {
      statsCards: [
        {
          type: "warning",
          icon: "ti-cloud",
          title: "IP space",
          info: "",
          value: "",
          footerText: "Updated now",
          footerIcon: "ti-reload"
        },
        {
          type: "warning",
          icon: "ti-infinite",
          title: "Subnet",
          info: "",
          value: "",
          footerText: "Last day",
          footerIcon: "ti-calendar"
        },
        {
          type: "danger",
          icon: "ti-timer",
          title: "Sleep time",
          info: "",
          value: "",
          footerText: "In the last hour",
          footerIcon: "ti-timer"
        },
        {
          type: "info",
          icon: "ti-direction",
          title: "Elastic\naddress",
          info: "",
          value: "",
          footerText: "Updated now",
          footerIcon: "ti-reload"
        },
        {
          type: "warning",
          icon: "ti-stats-up",
          title: "Portscan start",
          info: "",
          value: this.serverStatus,
          footerText: "Updated now",
          footerIcon: "ti-reload"
        },
        {
          type: "warning",
          icon: "ti-stats-down",
          title: "Portscan stop",
          info: "",
          value: this.serverStatus,
          footerText: "Updated now",
          footerIcon: "ti-reload"
        },
      ],
      checkBox: [
        {
          type: "success",
          icon: "ti-server",
          title: "Vulnerability discovery",
          info: "",
          value: this.serverStatus,
          footerText: "Updated now",
          footerIcon: "ti-reload"
        },
        {
          type: "success",
          icon: "ti-wallet",
          title: "Port scan",
          info: "",
          value: "",
          footerText: "Last day",
          footerIcon: "ti-calendar"
        },
      ],
      scanner: {
        ip_space: "N/A",
        elastic_address: "N/A",
        subnet: "N/A",
        sleeptime: "N/A",
        start: "N/A",
        end: "N/A",
        vuln_discovery: "N/A",
        port_scan: "N/A"
      },
      type: ["", "info", "success", "warning", "danger"],
      notifications: {
        topCenter: false
      }
    };
  },
  methods: {
    getServerState() {
      getServerState("http://localhost:5000/api/scanner-config/").then(response => {
        console.log(response["data"])
        if (response["status"] !== "offline") {
        this.statsCards[0].info = response["data"]["ip_space"]
        this.statsCards[1].info = response["data"]["elastic_address"];
        this.statsCards[2].info = response["data"]["subnet"];
        this.statsCards[3].info = response["data"]["sleeptime"];
        this.statsCards[4].info = response["data"]["start"];
        this.statsCards[5].info = response["data"]["end"];
        this.checkBox[0].info = response["data"]["vuln_discovery"];
        this.checkBox[1].info = response["data"]["port_scan"];
        }
      })
      .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    setServerState() {
      var sendDict = {
        ip_space: this.statsCards[0]["info"],
        elastic_address: this.statsCards[1]["info"],
        subnet: this.statsCards[2]["info"],
        sleeptime: this.statsCards[3]["info"],
        start: this.statsCards[4]["info"],
        end: this.statsCards[5]["info"],
        vuln_discovery: this.checkBox[0]["info"],
        port_scan: this.checkBox[1]["info"]
      };
      console.log(sendDict);
      setServerState("http://localhost:5000/api/scanner-config/", sendDict).then(response => {
        console.log(response["status"])
        if (response["status"] !== 200) {
        this.$notify({
        // component: NotificationTemplate,
        icon: "ti-alert",
        horizontalAlign: "center",
        verticalAlign: "top",
        type: "warning",
        title: "Backend not responding!\nDid not update configuration"
      });
    }
        if (response["status"] === 200) {
          this.$notify({
        // component: NotificationTemplate,
        icon: "ti-check",
        horizontalAlign: "center",
        verticalAlign: "bottom",
        type: "success",
        title: "Configuration updated"
      });
        }
        }
      )
      .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created()  {
      this.getServerState();
  },
};
</script>
<style>
</style>
