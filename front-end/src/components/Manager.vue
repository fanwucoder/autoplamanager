<template>
  <a-layout>
    <a-layout-header></a-layout-header>

    <a-layout-content>
      <a-row type="flex" justify="center" align="top">

        <a-col :span="20">
          <a-table :columns="columns" :data-source="data" size="middle" rowKey="index">
            <a slot="name" slot-scope="text">{{ text }}</a>

            <span slot="last_img" slot-scope="last_img,record">
         <img :src="last_img" class="last_img" v-on:click="get_img(record)"/>
        </span>
            <span slot="img" slot-scope="img">
         <img v-for="im in img" :src="im"/>
        </span>
            <span slot="is_in_android" slot-scope="is_in_android">
          {{ is_in_android ? "运行中" : "停止" }}
        </span>

            <span slot="action" slot-scope="text, record">
          <a v-on:click="start_mnq(record)">启动</a>
          <a-divider type="vertical"/>
          <a v-on:click="stop_mnq(record)">停止</a>
              <a-divider type="vertical"/>
          <a v-on:click="show_history(record)"> 查看历史 </a>
          <a-divider type="vertical"/>
          <a v-on:click="delete_mnq"> 删除 </a>
        </span>
          </a-table>
        </a-col>

      </a-row>

      <a-modal v-model="pic_history" title="历史截图" width="900px" height="600px"
               :bodyStyle="{width:'900px',height:'600px',overflow:'scroll'}">
        <div style="text-align: center;width:100%;">
          <img v-for="img in history_imgs" :src="img" class="his_img"/>
        </div>

      </a-modal>
    </a-layout-content>
    <a-layout-footer></a-layout-footer>
  </a-layout>
</template>
<style scoped>
.his-imgs {
  width: 800px;
  height: 600px;
  overflow: scroll;
}

.ant-layout-header {
  background: #ffffff;
}

.his_img {
  margin: 5px;
  width: 320px;
  height: 180px;

}

.last_img {
  width: 160px;
  height: 90px;
}
</style>
<script>
const columns = [
  {
    title: "序号",
    dataIndex: "index",
    key: "index",
  },
  {
    title: "名字",
    dataIndex: "name",
    key: "name",
  },
  {
    title: "运行状态",
    dataIndex: "is_in_android",
    key: "is_in_android",
    scopedSlots: {customRender: "is_in_android"},
  },
  {
    title: "截图",
    dataIndex: "last_img",
    key: "last_img",
    scopedSlots: {customRender: "last_img"},
  },
  {
    title: "状态截图",
    key: "img",
    dataIndex: "img",
    scopedSlots: {customRender: "img"},
  },
  {
    title: "操作",
    key: "action",
    scopedSlots: {customRender: "action"},
  },
];
const images = [
  "11_20201230122702_finish_game_1.png",
  "11_20201230122703_start_game_1.png",
  "11_20201230122704_start_login_ok.png",
  "11_20201230122704_start_run.png",
];

export default {
  data() {
    return {
      rowKey: "index",
      history_imgs: [],
      pic_history: false,
      data: [],
      columns,
    };
  },
  mounted: function () {
    this.refresh();
  },
  methods: {
    get_img: function (record) {
      // this.$axios.get("")

      this.$axios.post("/api/last_img", this.$qs.stringify({
        "idx": record.index
      })).then(res => {
        record.last_img = res.data.data
      })

    },
    delete_mnq: function (evt) {
      alert("暂不支持")
    },
    refresh: function (evt) {
      this.$axios.get("/api/list").then((res) => (this.data = res.data));
    },
    show_result: function (res) {
      let msg
      if (res.data.success) {
        msg = "操作成功"
      } else {
        msg = "操作失败"
      }
      alert(msg)
      this.refresh()
    }, stop_mnq: function (record) {
      this.$axios.post("/api/stop_mnq", this.$qs.stringify({
        "idx": record.index
      })).then(res => {
        this.show_result(res);
      })
    },
    show_history: function (record) {
      this.$axios.post('/api/history_pic', this.$qs.stringify({
        "idx": record.index
      })).then(res => {
        this.history_imgs = res.data.data
        this.pic_history = true
      })

    },
    start_mnq: function (record) {
      this.$axios.post("/api/start_mnq", this.$qs.stringify({
        "idx": record.index
      })).then(res => {
        this.show_result(res);
      })
    }
  },
};
</script>
