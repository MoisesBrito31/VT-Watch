<template>
    <div>
         <div class="col-auto">
            <div class="bg-light border rounded mb-5 p-2 painel">
                <h3 class="text-center">{{data.name}}</h3>
                <div class="m-auto text-center" v-if="data.online==true"><img :src="motorImg" height="160px"></div>
                <div class="m-auto text-center" v-else><img :src="this.$getImgUrl('motorOffLine','png')" height="160px"></div>
                <b-form-group v-if="data.vibraX>0" class="m-2" label="RMS X(mm/s):" label-for="x">
                    <b-form-input v-model="data.vibraX" v-bind:class="alerta1"  name="x" disabled size="lg" type="text"></b-form-input>
                </b-form-group>
                <b-form-group v-if="data.vibraZ>0" class="m-2" label="RMS Z(mm/s):" label-for="z">
                    <b-form-input v-model="data.vibraZ" v-bind:class="alerta2"  name="z" disabled size="lg" type="text"></b-form-input>
                </b-form-group>
                 <b-form-group v-if="data.vibraX2>0" class="m-2" label="Pico X(mm/s):" label-for="x2">
                    <b-form-input v-model="data.vibraX2" v-bind:class="alerta3"  name="x2" disabled size="lg" type="text"></b-form-input>
                </b-form-group>
                <b-form-group v-if="data.vibraZ2>0" class="m-2" label="Pico Z(mm/s):" label-for="z2">
                    <b-form-input v-model="data.vibraZ2" v-bind:class="alerta4"  name="z2" disabled size="lg" type="text"></b-form-input>
                </b-form-group>
                <b-form-group v-if="data.corrente>0" class="m-2" label="Corrente(A):" label-for="z2">
                    <b-form-input v-model="data.corrente" v-bind:class="alerta6"  name="z2" disabled size="lg" type="text"></b-form-input>
                </b-form-group>
                <b-form-group v-if="data.temp>0" class="m-2" label="Temperatura(Cº):" label-for="temp">
                    <b-form-input v-model="data.temp" v-bind:class="alerta5" name="temp" disabled size="lg" type="text"></b-form-input>
                </b-form-group>
                <div>
                    <button type="button" @click="aprende(data.id)" class="btn btn-block btn-primary">Aprender</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
    name: "painelComp",
    created(){
      this.load()
      setInterval(()=>{this.load()},5000)
    },
    data(){
      return{
          data:{
            id:0
          }
      }
    },
    methods:{
        load(){
            this.readData()
        },
        dataFormat(){
            const formData = new FormData()
            formData.append('alvo',`${this.id}`)
            return formData
        },
        async aprende(valor) {
            this.id = valor
        try {
          const response = await fetch(`${this.getDominio}/api/aprende/`, {
            method: 'POST',
            headers: {
                'Authorization': `Token ${this.getToken}`
            },
            body: this.dataFormat()
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
        async readData() {
        fetch(`${this.getDominio}/api/node/${this.endereco}/`,{
                method: 'get',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${this.getToken}`
                }
        }).then(res=>{
            if(res.status === 200){
                return res.text()
            }
        }).then(result=>{
             this.data = JSON.parse(result)
             this.erro= false
        }).catch(erro=>{
            console.log(erro)
            this.erro= true
        })
      },
        alerta(id){
            switch (id) {
                case "0":
                    return "text-center text-primary"
                case "1":
                    return "text-center text-warning"
                case "2":
                    return "text-center text-danger"
                default:
                    return "text-center"
            }
        },
    },
    computed:{
        ...mapGetters(['getDominio','getToken']),
        motorImg(){
          switch (this.data.estado) {
              case "1":
                    return this.$getImgUrl("motorOk","png")
                case "2":
                    return this.$getImgUrl("motorFalha","png")
                case "3":
                    return this.$getImgUrl("motorAlerta","png")
                case "4":
                    return this.$getImgUrl("motorLearn","png")
              default:
                  return this.$getImgUrl("motorPreto","png")
          }
        },
        alerta1(){
            return this.alerta(this.data.alerta[0])
        },
         alerta2(){
            return this.alerta(this.data.alerta[1])
        },
         alerta3(){
            return this.alerta(this.data.alerta[2])
        },
         alerta4(){
            return this.alerta(this.data.alerta[3])
        },
        alerta5(){
            return this.alerta(this.data.alerta[4])
        },
        alerta6(){
            return this.alerta(this.data.alerta[5])
        },

    },
    props:{
        endereco: Number
    },
}
</script>

