<template>
  <a-layout>
      <a-layout-header></a-layout-header>
  
    <a-layout-content>
        <a-row type="flex" justify="center" align="top">
    
      <a-col  :span="20" >
        <a-table :columns="columns" :data-source="data" size="middle">
        <a slot="name" slot-scope="text">{{ text }}</a>

        <span slot="last_img" slot-scope="last_img">
         <img :src="last_img" class="last_img"/>
        </span>
         <span slot="img" slot-scope="img">
         <img v-for="im in img" :src="im" />
        </span>
        <span slot="is_in_android" slot-scope="is_in_android">
          {{ is_in_android ? "运行中" : "停止" }}
        </span>

        <span slot="action" slot-scope="text, record">
          <a>启动</a>
          <a-divider type="vertical" />
          <a v-on:click="test">停止</a>
          <a-divider type="vertical" />
          <a> 删除 </a>
        </span>
      </a-table>
      </a-col>

    </a-row>


      
      </a-layout-content    >
       <a-layout-footer></a-layout-footer>
  </a-layout>
</template>
<style scoped>
.ant-layout-header{
  background: #ffffff;
}
.last_img{
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
    scopedSlots: { customRender: "is_in_android" },
  },
  {
    title: "截图",
    dataIndex: "last_img",
    key: "last_img",
      scopedSlots: { customRender: "last_img" },
  },
  {
    title: "状态截图",
    key: "img",
    dataIndex: "img",
     scopedSlots: { customRender: "img" },
  },
  {
    title: "操作",
    key: "action",
    scopedSlots: { customRender: "action" },
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
      props: {
        rowKey: "index",
      },
      data: [],
      columns,
    };
  },
  mounted: function () {
    this.refresh();
  },
  methods: {
    refresh: function () {
      this.$axios.get("/list").then((res) => (this.data = res.data));
    },
    test: function (evt) {
      this.$axios.get("/").then((res) => alert(res.data));
    },
  },
};
</script>
