<template>
  <div class="user_wrap">
    <BreadCrumb crumb="SPU管理>SPU修改"></BreadCrumb>  
    <div class="center_wrap">
      <h1 class="spu_form_title">SPU修改</h1>
      <el-form :model="SpuForm" status-icon ref="SpuForm" label-width="100px">
      <el-form-item label="SPU名称" prop="name">
        <el-input type="text" v-model="SpuForm.name" autocomplete="off" size="small"></el-input>
      </el-form-item>
      <el-form-item label="品牌：" prop="brand_id">
        <el-select v-model="SpuForm.brand_id" size="small">
          <el-option
            v-for="item in brand_list"
            :key="item.id"
            :label="item.name"
            :value="item.id">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="一级分类：" prop="category1_id">
        <el-select v-model="SpuForm.category1_id" size="small" @change="fnGetCategory_sub(SpuForm.category1_id,2)">
          <el-option
            v-for="item in category1_list"
            :key="item.id"
            :label="item.name"
            :value="item.id">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="二级分类：" prop="category2_id">
        <el-select v-model="SpuForm.category2_id" size="small"  @change="fnGetCategory_sub(SpuForm.category2_id,3)">
          <el-option
            v-for="item in category2_list"
            :key="item.id"
            :label="item.name"
            :value="item.id">
          </el-option>
        </el-select>
      </el-form-item>      
      <el-form-item label="三级分类：" prop="category3_id">
        <el-select v-model="SpuForm.category3_id" size="small">
          <el-option
            v-for="item in category3_list"
            :key="item.id"
            :label="item.name"
            :value="item.id">
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="商品详情:">
        <div><editor v-model="SpuForm.desc_detail" :init="init"></editor></div>        
      </el-form-item>

      <el-form-item label="商品包装:">  
        <div><editor v-model="SpuForm.desc_pack" :init="init"></editor></div>  
      </el-form-item>

      <el-form-item label="售后服务:">
        <div><editor v-model="SpuForm.desc_service" :init="init"></editor></div> 
      </el-form-item> 

      <el-form-item>
        <el-button type="primary" @click="submitForm">提交</el-button>
        <el-button><router-link to="/home/spu" style="color:#606266">取消</router-link></el-button>
      </el-form-item>
      </el-form>             
    </div>  
</div>
</template>

<script>
let token = localStorage.token
import tinymce from 'tinymce/tinymce'
import Editor from '@tinymce/tinymce-vue'
import 'tinymce/themes/modern/theme'
import 'tinymce/plugins/image'
import 'tinymce/plugins/media'
import 'tinymce/plugins/table'
import 'tinymce/plugins/lists'
import 'tinymce/plugins/contextmenu'
import 'tinymce/plugins/wordcount'
import 'tinymce/plugins/colorpicker'
import 'tinymce/plugins/textcolor'
import BreadCrumb from '@/components/widget/BreadCrumb'
import cons from '@/components/constant'
export default {
  name: 'SpuAdd',
  data () {
    return {
      edit_id:'',
      init: {
            language_url: '/static/tinymce/langs/zh_CN.js',
            language: 'zh_CN',
            skin_url: '/static/tinymce/skins/lightgray',
            width:'99%',
            height: 200,
            branding: false,
            menubar: false,
            plugins: 'lists image media table textcolor wordcount contextmenu',
            toolbar: 'undo redo |  styleselect | formatselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | lists image media table | removeformat'
      },
      brand_list:[],
      category1_list:[],
      category2_list:[],
      category3_list:[],
      SpuForm:{
        name:'',
        brand_id:'',
        category1_id:'',
        category2_id:'',
        category3_id:'',
        desc_detail:'',
        desc_pack:'',
        desc_service:''
      }      
    }
  },
  components:{
    BreadCrumb,
    Editor  
  },
  methods:{
    fnGetThisCategory(){
      this.axios.get(cons.apis + '/goods/' + this.edit_id + '/', {
          headers: {
            'Authorization': 'JWT ' + token
          },
          responseType: 'json'
      })
      .then(dat=>{
         this.SpuForm.name = dat.data.name;
         this.SpuForm.brand_id = dat.data.brand_id;
         this.SpuForm.category1_id = dat.data.category1_id;
         this.fnGetCategory_sub(dat.data.category1_id,2);
         this.SpuForm.category2_id = dat.data.category2_id;
         this.fnGetCategory_sub(dat.data.category2_id,3);
         this.SpuForm.category3_id = dat.data.category3_id;
         this.SpuForm.desc_detail = dat.data.desc_detail;
         this.SpuForm.desc_pack = dat.data.desc_pack;
         this.SpuForm.desc_service = dat.data.desc_service;
      }).catch(err=>{
         console.log(err);
      });
    },
    fnGetBrand:function(){
      this.axios.get(cons.apis + '/goods/brands/simple/', {
          headers: {
            'Authorization': 'JWT ' + token
          },
          responseType: 'json'
      })
      .then(dat=>{
          this.brand_list = dat.data;
      }).catch(err=>{
         console.log(err);
      });
    },
    fnGetCategories:function(){
      this.axios.get(cons.apis + '/goods/channel/categories/', {
          headers: {
            'Authorization': 'JWT ' + token
          },
          responseType: 'json'
      })
      .then(dat=>{
          this.category1_list = dat.data;
      }).catch(err=>{
         console.log(err);
      });
    },
    fnGetCategory_sub:function(sid,num){
      this.axios.get(cons.apis + '/goods/channel/categories/' + sid +'/', {
          headers: {
            'Authorization': 'JWT ' + token
          },
          responseType: 'json'
      })
      .then(dat=>{
          this['category' + num + '_list'] = dat.data;
      }).catch(err=>{
         console.log(err);
      });
    },
    submitForm(){
        this.axios.put(cons.apis + '/goods/'+ this.edit_id + '/',this.SpuForm, {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json'           
        })
        .then(dat=>{
            if(dat.status==200){
              this.$message({
                type: 'success',
                message: 'SPU修改成功!'
              });

              setTimeout(()=>{
                  this.$router.push({path:'/home/spu'});
              },2000);

            }
        }).catch(err=>{
            if(err.response.status==400){
              var errmsg = err.response.data;

              if(errmsg.name){
                this.$message({
                  type:'info',
                  message:errmsg.name[0]
                });
              }

              if(errmsg.non_field_errors){
                this.$message({
                  type:'info',
                  message:errmsg.non_field_errors[0]
                });
              }           
           }
        });
    }
  },
  mounted() {
    tinymce.init({});
    this.fnGetBrand();
    this.fnGetCategories();
    this.edit_id = this.$route.params.sEdit_id;
    this.fnGetThisCategory();
  }
}
</script>

<style scoped>
.center_wrap{
    width:95.2%;
    overflow:hidden;
    margin:10px auto 10px;
  }
.spu_form_title{
  line-height: 24px;
  font-size: 18px;
  color: #303133;
  margin:10px 0px 20px;
}

</style>
