import Home from '@/views/HomeView.vue'
import Fabrica from '@/views/IndexView.vue'
import Historico from '@/views/HistoricoView.vue'
import Page1 from '@/views/Page1View.vue'
import Page2 from '@/views/Page2View.vue'
import Login from '@/views/LoginView.vue'
import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store'

Vue.use(VueRouter)

function getCookie(name) {
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

const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/page1',
    component: Page1,
    meta: { requiresAuth: true }
  },
  {
    path: '/fabrica',
    component: Fabrica,
    meta: { requiresAuth: true }
  },
  {
    path: '/historico/:node',
    name: 'historico',
    component: Historico,
    meta: { requiresAuth: true }
  },
  {
    path: '/page2',
    component: Page2,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    component: Login
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

router.beforeEach((to, from, next) => {
  try{
    const token = getCookie('token')
    if(token == null){ throw new Error('token inexistente');}
    store.commit('logar',token)
    store.commit('setUser',getCookie('nome'))
  }catch(erro){
    store.commit('logout')
  }
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.logado) {
      next('/login');
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router