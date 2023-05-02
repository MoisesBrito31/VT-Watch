<template>
   <div>
        
        <b-navbar toggleable="lg" type="dark" variant="dark">
        <b-navbar-brand href="#">
          <img class="mr-3" src="../assets/logo novo.jpeg" width="120" height="40">
        </b-navbar-brand>
    
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
    
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item><router-link to="/">Home</router-link></b-nav-item>
            <b-nav-item><router-link to="/fabrica/">Fábrica</router-link></b-nav-item>
            <b-nav-item-dropdown>
              <template #button-content>
                <em>
                  Historico
                </em>
              </template>
              <div v-for="no in node" :key="no.id" >
                 <b-button @click="goHistorico(no.id)" variant="primary">{{ no.name }}</b-button>
              </div>
            </b-nav-item-dropdown>
          </b-navbar-nav>
         
          <b-navbar-nav class="ml-auto mr-2">
            <div class="m-auto" v-if="data.configurar">
                <p class="text-info"> {{ data.msg }}</p>
                <b-progress max="100" :value="data.percent"></b-progress>
            </div>
            <div class="m-auto">
              <img :src="dxm_online" width="30" height="30" />
            </div>
            <b-nav-item-dropdown right v-if="logado">
              <template #button-content>
                <em>
                  Olá {{getNome}}
                  <b-avatar badge-variant="danger" variant="primary"></b-avatar>
                </em>
              </template>
              <div>
                 <b-button @click="gravar" variant="primary">Gravar DXM</b-button>
              </div>
              <div>
                 <b-button @click="deslogar" variant="primary">sair</b-button>
              </div>
            </b-nav-item-dropdown>
            <div  class="m-auto" v-else>
              <b-nav-item><router-link to="/login/">Logar</router-link></b-nav-item>
            </div>
          </b-navbar-nav>
    
        </b-collapse>
      </b-navbar>
        
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { mapMutations } from 'vuex'
export default {
    name:'main_menu',
    created(){      
      this.getNodes()
      this.load()
      setInterval(()=>{this.load()},5000)
    },
    data(){
      return{
        data:[],
        node:[]
      }
    },
    methods:{
      ...mapMutations(['logout','dxmSetOn','dxmSetOff']),
      load(){
        this.getDados()
      },
      async gravar() {
        try {
          const response = await fetch(`${this.getDominio}/api/config/`, {
            method: 'GET',
            headers: {
                'Authorization': `Token ${this.getToken}`
            },
          });
  
          if (response.ok) {
            console.log("foi")
          } else {
            console.error('Erro ao fazer login');
          }
            } catch (error) {
                console.error(error);
            }
        },
      goHistorico(id){
        this.$router.push( {path: `/historico/${id}`,forceRefresh: true} )
        document.location.reload()
      },
      deslogar(){
        this.$apagaCookies()
        this.logout()
        setTimeout(() => {
          this.$apagaCookies()
          this.$router.push('/');
        }, 1000);
      },
      async getDados() {
        try {
          const response = await fetch(`${this.getDominio}/api/dxm/`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Token ${this.getToken}`
            },
          });
  
          if (response.ok) {
            const data = await response.json();
            this.data = data
            if(data.online){
              this.dxmSetOn()
             }else{
              this.dxmSetOff()
             }
          } else {
            console.error('Erro ao fazer login');
          }
        } catch (error) {
          console.error(error);
        }
      },
      async getNodes() {
        try {
          const response = await fetch(`${this.getDominio}/api/node/`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Token ${this.getToken}`
            },
          });
  
          if (response.ok) {
            const data = await response.json();
            this.node = data
          } else {
            console.error('Erro ao fazer login');
          }
        } catch (error) {
          console.error(error);
        }
      }
    },
    computed:{
      ...mapGetters(['logado','getNome','getInicial','dxmOnline','getDominio','getToken']),
      dxm_online(){
        if(this.dxmOnline){
          return this.$getImgUrl("notifiOk","png")
        }else{
          return this.$getImgUrl("notifiFalha","png")
        }
      }
    },
}
</script>