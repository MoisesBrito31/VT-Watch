<template>
    <div>
        <b-container fluid>
        <div class="card-title mt-5 mb-3 pt-3">
            <div class="row">
                <div class="col text-left"><h2>Fábrica</h2></div>    
            </div>
        </div>
        <hr>
        <div class="container-fluid row m-auto">
            <div v-for="itens in data" :key="itens.id" class="col-auto">
                <painelComp :endereco="itens.id" ></painelComp>                
            </div>
            <b-table 
                    striped 
                    hover 
                    :items="data"
                    :busy="esperando"
                ></b-table>
        </div>
        </b-container>
    </div>
</template>

<script>
import painelComp from '@/components/painelComp.vue'
import { mapGetters } from 'vuex'
export default {
    name:'IndexView',
    components: {
    painelComp
  },
  data(){
    return {
        esperando: false,
        falha:false,
        data:[]
    }
  },
  created(){
    this.getDados()
  },
  computed:{...mapGetters(['getDominio','getToken'])},
  methods:{
    estruturar(){

    },
    async getDados(){
      try{
        this.esperando = true
        const response = await fetch(`${this.getDominio}/api/node/`,{
          headers:{
            'Authorization': `Token ${this.getToken}`
          }
        });
        if(!response.ok){
          throw new Error('Failed to fetch data');
        }
        const data = await response.json()
        this.esperando = false
        this.data = data
        this.falha = false
      }catch(error){
        this.falha = true
        this.esperando = false
        this.logout()
        alert(error)
        this.$router.push('/login/')
      }
    }
  }
}
</script>