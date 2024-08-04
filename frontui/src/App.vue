<template>
  <div style="margin: 0 auto; width: 100%">
    <h1 style="text-align: center">数据</h1>
    <el-button
      @click="drawer = !drawer"
      type="primary"
      style="margin-left: 16px"
    >
      筛选
    </el-button>
    <el-drawer title="设置" v-model="drawer" :with-header="false">
      <el-form :model="paramsd" label-width="auto" style="max-width: 700px">
        <el-form-item label="关键字">
          <el-input v-model="paramsd.keyword" />
        </el-form-item>
        <el-form-item label="城市">
          <el-select
            v-model="paramsd.cty"
            placeholder="please select your zone"
          >
            <el-option
              v-for="(item, index) in cityname"
              :label="item"
              :value="item === '全部' ? '' : item"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="分类">
          <el-select
            v-model="paramsd.ctl"
            placeholder="please select your zone"
          >
            <el-option
              v-for="(item, index) in categoryname"
              :label="item"
              :value="item === '全部' ? '' : item"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="子类">
          <el-select
            v-model="paramsd.sctl"
            placeholder="please select your zone"
          >
            <el-option
              v-for="(item, index) in subcatgoryname"
              :label="item"
              :value="item === '全部' ? '' : item"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">更改</el-button>
        <!-- <el-button>取消</el-button> -->
      </el-form-item>
    </el-drawer>

    <!-- 数据表格 -->
    <el-table :data="tickets" style="width: 100%">
      <el-table-column label="名称" prop="name" />
      <el-table-column label="日期" prop="date" />
      <el-table-column label="艺人" prop="actors" />
      <el-table-column label="类型" prop="categoryName" />
      <el-table-column label="地点" prop="location" />
      <el-table-column label="详细地点" prop="location_details" />
      <el-table-column label="价格" prop="price" />
      <el-table-column label="最低价" prop="lowPrice" sortable />
      <el-table-column label="最高价" prop="highPrice" sortable />
    </el-table>
    <!-- <el-pagination
      background
      layout="prev, pager, next"
      :total="1000"
      style="margin: 0 auto"
    >
    </el-pagination> -->
  </div>
</template>

<script setup>
import axios from "axios";
import { reactive, ref, onMounted } from "vue";
import { ElMessageBox } from "element-plus";

const tickets = reactive([]);

const paramsd = reactive({
  keyword: "",
  cty: "",
  ctl: "",
  currPage: "1",
  singleChar: "",
  tn: "",
  sctl: "",
  tsg: "0",
  order: "1",
});

let categoryname = reactive(["全部"]);
let cityname = reactive(["全部"]);
let subcatgoryname = reactive(["全部"]);

let drawer = ref(false);
const getData = () => {
  if (paramsd.cty === "全部") {
    paramsd.cty = "";
  }
  if (paramsd.sctl === "全部") {
    paramsd.sctl = "";
  }
  if (paramsd.ctl === "全部") {
    paramsd.ctl = "";
  }
  axios.post("http://localhost:5000/app", paramsd).then((res) => {
    console.log(paramsd);
    console.log(res.data);
    tickets.splice(0, tickets.length);
    tickets.push(...res.data);
    tickets.map((item) => {
      if (item.actors !== "") {
        item.actors = item.actors.split("：")[1];
      } else {
        item.actors = "无";
      }
      return item;
    });

    console.log("更新数据");
  });
  console.log(tickets);
};

const getTag = () => {
  axios.post("http://localhost:5000/tags", paramsd).then((res) => {
    categoryname.splice(1, categoryname.length - 1);
    cityname.splice(1, cityname.length - 1);
    subcatgoryname.splice(1, subcatgoryname.length - 1);
    res.data["categoryname"].map((item) => {
      categoryname.push(item.name);
    });
    res.data["cityname"].map((item) => {
      cityname.push(item.name);
    });
    res.data["subcategoryname"].map((item) => {
      subcatgoryname.push(item.name);
    });
    console.log(res.data, 682);
  });
};

const onSubmit = () => {
  getData();
  getTag();
};

// 页面渲染之后添加数据
onMounted(() => {
  getData();
  getTag();
});
</script>

<style>
</style>
