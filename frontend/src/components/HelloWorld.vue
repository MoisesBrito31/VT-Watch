<template>
<div class="fundo">
    <!-- Mask & flexbox options-->
    <div class=" mask rgba-black-light align-items-center">
        <!-- Content -->
        <div class="container">
            <!--Grid row-->
            <div class="row">
                <!--Grid column-->

                <div class="container mb-auto" style="max-width:400px; opacity:1;">
                    <div class="card text-center mt-5 mb-5">
                        <div class="card-text">
                            <h2>VT Watch <br /> 1.0</h2>
                        </div>
                        <img class="mr-auto ml-auto mt-3 mb-3 " :src="getLog" height="250"
                            width="180" />
                        <div class="card-footer text-center">Interface responsiva de visualização de aplicação de VT na
                            Plataforma DXM's Series Banner.</div>
                    </div>



                </div>
                <!--Grid column-->
            </div>
            <!--Grid row-->
        </div>
        <!-- Content -->
    </div>
    <!-- Mask & flexbox options-->
</div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  computed:{
    getLog(){
      return this.$getImgUrl("dxm100","png")
    },
    getfundo(){
      return this.$getImgUrl("back25","png")
    }
  }
}
</script>

<style>
.fundo {
    min-height: 660px;
    background-image: url("");
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center center;
}
</style>