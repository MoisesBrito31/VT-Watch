import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
      dominio: 'http://localhost:8000',
      logado: false,
      nome: 'Desconhecido',
      inicial: '',
      token: '',
      avatar: '',
      dxm:false,
  },
  getters: {	  
    logado(state){return state.logado},
    getToken(state){return state.token},
    getDominio(state){return state.dominio},
    getNome(state){return state.nome},
    getInicial(state){return state.inicial},
    dxmOnline(state){return state.dxm},
  },
  mutations: {	
    logar(state,token){
      state.logado = true
      state.token = token
    },
    setUser(state, nome){
      state.nome = nome
    },
    logout(state){
      state.logado = false
      state.token = ''
      state.nome = ''
    },
    dxmSetOn(state){
      state.dxm = true
    },
    dxmSetOff(state){
      state.dxm = false
    }
  },
  actions: {
  },
  modules: {
  }
})