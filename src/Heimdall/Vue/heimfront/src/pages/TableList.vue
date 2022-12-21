<template>
    <div class="row">
      <div class="col-12">
        <card :title="table1.title" :subTitle="table1.subTitle">
          <div slot="raw-content" class="table-responsive">
            <paper-table :data="table1.data" :columns="table1.columns">

            </paper-table>
          </div>
        </card>
      </div>

    </div>
</template>
<script>
import { PaperTable } from "@/components";
import { getServerState } from '@/utils/GetAPIData';
var tableColumns = ["Id", "Name", "Salary", "Country", "City"];
var tableData = [];

export default {
  components: {
    PaperTable
  },
  data() {
    return {
      table1: {
        title: "Last 100 runs of Heimdall scanner",
        columns: [...tableColumns],
        data: [...tableData]
      },
    };
  },
  methods: {
    getServerState() {
      getServerState("http://localhost:5000/api/scanner-history/").then(response => {
        console.log(response["data"])
        tableColumns = response["data"]["headers"]
        console.log(response["data"]["headers"])
        console.log(response["data"]["runs"])
        this.table1.columns = response["data"]["headers"]
        this.table1.data = response["data"]["runs"]
      })
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
