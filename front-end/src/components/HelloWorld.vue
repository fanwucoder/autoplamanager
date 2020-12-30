<template>
  <a-table :columns="columns" :data-source="data">
    <a slot="name" slot-scope="text">{{ text }}</a>
    <span slot="customTitle"><a-icon type="smile-o" /> Name</span>
    <span slot="tags" slot-scope="tags">
      <a-tag
        v-for="tag in tags"
        :key="tag"
        :color="
          tag === 'loser' ? 'volcano' : tag.length > 5 ? 'geekblue' : 'green'
        "
      >
        {{ tag.toUpperCase() }}
      </a-tag>
    </span>
    <span slot="imgs" slot-scope="imgs">
      <img
        v-for="(img,index) in imgs"
        :key="img"
        :src="'./static/results/' + img"
        :style="'padding-left:'+(index*100)+'px;z-index:'+(99+index)"
        class="myimg"
      />
    </span>

    <span slot="action" slot-scope="text, record">
      <a>Invite 一 {{ record.name }}</a>
      <a-divider type="vertical" />
      <a>Delete</a>
      <a-divider type="vertical" />
      <a class="ant-dropdown-link"> More actions <a-icon type="down" /> </a>
    </span>
  </a-table>
</template>
<style scoped>
.myimg {
  position: absolute;
   clip-path: polygon(50px 0px, 50px 50px, 100px 50px, 100px 0px);
}
</style>
<script>
const columns = [
  {
    dataIndex: "name",
    key: "name",
    slots: { title: "customTitle" },
    scopedSlots: { customRender: "name" },
  },
  {
    title: "Age",
    dataIndex: "age",
    key: "age",
  },
  {
    title: "Imgs",
    dataIndex: "imgs",
    key: "imgs",
    scopedSlots: { customRender: "imgs" },
  },
  {
    title: "Address",
    dataIndex: "address",
    key: "address",
  },
  {
    title: "Tags",
    key: "tags",
    dataIndex: "tags",
    scopedSlots: { customRender: "tags" },
  },
  {
    title: "Action",
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
const data = [
  {
    key: "1",
    name: "John Brown",
    age: 32,
    imgs: images,
    address: "New York No. 1 Lake Park",
    tags: ["nice", "developer"],
  },
  {
    key: "2",
    name: "Jim Green",
    age: 42,
    imgs: images,
    address: "London No. 1 Lake Park",
    tags: ["loser"],
  },
  {
    key: "3",
    name: "Joe Black",
    age: 32,
    imgs: images,
    address: "Sidney No. 1 Lake Park",
    tags: ["cool", "teacher"],
  },
];

export default {
  data() {
    return {
      data,
      columns,
    };
  },
};
</script>
