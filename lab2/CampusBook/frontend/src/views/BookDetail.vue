<template>
  <div class="book-detail-container">
    <el-card v-loading="loading" class="book-card">
      <div v-if="book" class="book-detail">
        <div class="book-info">
          <div class="book-images">
            <el-image 
              v-for="(image, index) in book.images" 
              :key="index" 
              :src="image" 
              fit="cover"
              class="book-image"
            ></el-image>
          </div>
          <div class="book-details">
            <h2>{{ book.title }}</h2>
            <p class="author">作者：{{ book.author }}</p>
            <p class="isbn">ISBN：{{ book.isbn }}</p>
            <p class="category">分类：{{ book.category }}</p>
            <p class="condition">成色：{{ book.condition }}</p>
            <p class="price">价格：¥{{ book.price }}</p>
            <p class="delivery">交易方式：{{ book.delivery_type }}</p>
            <p class="stock">库存：{{ book.stock }}</p>
            <div class="seller-info">
              <h3>卖家信息</h3>
              <p>昵称：{{ book.seller.nickname }}</p>
              <p>注册时间：{{ book.seller.created_at }}</p>
            </div>
            <el-button type="primary" size="large" @click="buyNow" style="margin-top: 20px">立即购买</el-button>
          </div>
        </div>
        <div class="book-description">
          <h3>书籍描述</h3>
          <p>{{ book.description }}</p>
        </div>
      </div>
      <div v-else class="no-book">
        <el-empty description="书籍不存在"></el-empty>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const book = ref(null)

const getBookDetail = async () => {
  const id = route.params.id
  try {
    const { data } = await axios.get(`/api/books/${id}`)
    if (data.code === 200) {
      book.value = data.data
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    ElMessage.error('获取书籍详情失败')
  } finally {
    loading.value = false
  }
}

const buyNow = () => {
  // 跳转到订单创建页面或直接打开地址选择弹窗
  router.push('/address')
}

onMounted(() => {
  getBookDetail()
})
</script>

<style scoped>
.book-detail-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.book-card {
  margin-bottom: 20px;
}

.book-info {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
}

.book-images {
  flex: 0 0 300px;
}

.book-image {
  width: 100%;
  height: 400px;
  margin-bottom: 10px;
}

.book-details {
  flex: 1;
}

.book-details h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.book-details p {
  margin-bottom: 10px;
  font-size: 16px;
}

.price {
  font-size: 24px;
  font-weight: bold;
  color: #f56c6c;
}

.seller-info {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
}

.seller-info h3 {
  font-size: 18px;
  margin-bottom: 10px;
}

.book-description {
  margin-top: 30px;
  padding-top: 30px;
  border-top: 1px solid #e4e7ed;
}

.book-description h3 {
  font-size: 18px;
  margin-bottom: 10px;
}

.no-book {
  text-align: center;
  padding: 100px 0;
}
</style>