// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

import router from './router'
import {Button, Modal, Layout, Table} from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css'
import App from './App'
import axios from 'axios'
import qs from 'qs'

// axios.defaults.baseURL = 'http://127.0.0.1:5000';
// axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
Vue.prototype.$axios = axios
Vue.prototype.$qs = qs
Vue.config.productionTip = false

Vue.component(Button.name, Button)
Vue.component(Modal.name, Modal)
Vue.component(Layout.name, Layout)
Vue.component(Table.name, Table)


// Vue.use(Antd)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>'
})
