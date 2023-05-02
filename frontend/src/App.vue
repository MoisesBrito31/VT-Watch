<template>
  <div id="app">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <main_menu></main_menu>
    <b-container fluid>
      <router-view/>
    </b-container>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import main_menu from '@/components/main_menuComp.vue'
export default {
  computed: {
    ...mapGetters(['logado'])
    },
  components:{
    main_menu
  }
}
</script>

