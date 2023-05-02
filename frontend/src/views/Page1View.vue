
<template>
    <div>
      <h3>Pagina 1</h3>
      <p>essa pagina precisa de login</p>
      <button type="button" @click="getDados"> atuar</button>
      <!--<button type="button" @click="setRelogio"> chamar Set</button>-->
      <div>
      <input type="number" v-model="registro">
      <input type="number" v-model="quantidade">
      <input type="number" v-model="modbusid">
      <button type="button" @click="getRegistro"> enviar</button>
      <div>
        <button type="button" @click="setRegistro"> set 5 registros</button>
      </div>
      <div>
        <button type="button" @click="getNodes"> nodes Setups</button>
      </div>
    </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { mapMutations } from 'vuex';
export default {
  data(){
    return {
      esperando: false,
      falha: false,
      data:[],
      registro: 1,
      quantidade: 1,
      modbusid: 199,
    }
  },
  created(){
    //this.getDados();
  },
  computed:{
    ...mapGetters(['getDominio','getToken'])
  },
  methods:{
    ...mapMutations(['logout']),
    async getDados(){
      try{
        this.esperando = true
        const response = await fetch(`${this.getDominio}/api/dxm/reboot/`,{
          headers:{
            'Authorization': `Token ${this.getToken}`
          }
        });
        if(!response.ok){
          throw new Error('Failed to fetch data');
        }
        const data = await response.json()
        this.esperando = false
        alert(data.valor)
        alert(data.erro)
        this.falha = false
      }catch(error){
        this.falha = true
        this.esperando = false
        alert(error)
      }
    },
    async setRelogio(){
      try{
        this.esperando = true
        const response = await fetch(`${this.getDominio}/api/dxm/setrelogio/`,{
          method:"POST",
          headers:{
            'Authorization': `Token ${this.getToken}`
          }
        });
        if(!response.ok){
          throw new Error('Failed to fetch data');
        }
        const data = await response.json()
        this.esperando = false
        alert(data.valor)
        alert(data.erro)
        this.falha = false
      }catch(error){
        this.falha = true
        this.esperando = false
        alert(error)
      }
    },
    dataFormatGetRegs(){
                const formData = new FormData()
                formData.append('registro',`${this.registro}`)
                formData.append('quantidade',`${this.quantidade}`)
                formData.append('modbusid',`${this.modbusid}`)
                return formData
    },
    dataFormatSetRegs(){
                const formData = new FormData()
                formData.append('registro',`${this.registro}`)
                formData.append('quantidade',`5`)
                formData.append('modbusid',`${this.modbusid}`)
                formData.append('ar',"12,1,4,2,1")
                return formData
    },
    async getRegistro(){
      try{
        this.esperando = true
        const response = await fetch(`${this.getDominio}/api/dxm/getregs/`,{
          method:"POST",
          headers:{
            'Authorization': `Token ${this.getToken}`
          },
          body: this.dataFormatGetRegs()
        });
        if(!response.ok){
          throw new Error('Failed to fetch data');
        }
        const data = await response.json()
        this.esperando = false
        alert(data.valor)
        alert(data.erro)
        this.falha = false
      }catch(error){
        this.falha = true
        this.esperando = false
        alert(error)
      }
    },
    async setRegistro(){
      try{
        this.esperando = true
        const response = await fetch(`${this.getDominio}/api/dxm/setregs/`,{
          method:"POST",
          headers:{
            'Authorization': `Token ${this.getToken}`
          },
          body: this.dataFormatSetRegs()
        });
        if(!response.ok){
          throw new Error('Failed to fetch data');
        }
        const data = await response.json()
        this.esperando = false
        alert(data.valor)
        alert(data.erro)
        this.falha = false
      }catch(error){
        this.falha = true
        this.esperando = false
        alert(error)
      }
    },
    async getNodes(){
      try{
        this.esperando = true
        const response = await fetch(`${this.getDominio}/api/nodesetup/`,{
          method:"GET",
          headers:{
            'Authorization': `Token ${this.getToken}`
          },
        });
        if(!response.ok){
          throw new Error('Failed to fetch data');
        }
        const data = await response.json()
        this.esperando = false
        alert(data)
        this.falha = false
      }catch(error){
        this.falha = true
        this.esperando = false
        alert(error)
      }
    },
  }
}
</script>
