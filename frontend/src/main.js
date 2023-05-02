import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

Vue.prototype.$getCookie = function(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
Vue.prototype.$setCookie = function(cname, cvalue, exdays=1, secure=false) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  if(secure){
    document.cookie = cname + "=" + cvalue +  "; " + expires + "; secure; HttpOnly";
  }else{
    document.cookie = cname + "=" + cvalue + "; " + expires;
  }
  
},
Vue.prototype.$apagaCookies = function() {
  var cookies = document.cookie.split(";");
  for (var i = 0; i < cookies.length; i++) {
    var cookie = cookies[i];
    var eqPos = cookie.indexOf("=");
    var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
    document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
  }
},
Vue.prototype.$getImgUrl = function(pet,ext) {
  var images = ''
  if (ext =='png'){
      images = require.context('./assets/', false, /\.png$/)
      return images('./' + pet + ".png")
    }else if(ext=='jpg'){
       images = require.context('./assets/', false, /\.jpg$/)
        return images('./' + pet + ".jpg")
    }else{
      images = require.context('./assets/', false, /\.bmp$/)
        return images('./' + pet + ".bmp")
    }
},

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
