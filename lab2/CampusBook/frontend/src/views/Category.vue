<template>
  <div class="category-container">
    <el-card class="category-card">
      <template #header>
        <div class="category-header">
          <h2>{{ categoryName }}</h2>
        </div>
      </template>
      <div v-loading="loading" class="book-list">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="book in books" :key="book.id" class="book-item">
            <el-card :body-style="{ padding: '0px' }" @click="goToDetail(book.id)">
              <img :src="book.images[0] || 'https://via.placeholder.com/200'" class="book-img" alt="book cover" />
              <div class="book-info">
                <h3 class="book-title">{{ book.title }}</h3>
                <p class="book-author">{{ book.author }}</p>
                <p class="book-price">¥{{ book.price }}</p>
                <p class="book-condition">{{ book.condition }}</p>
                <p class="book-seller">卖家：{{ book.seller }}</p>
              </div>
            </el-card>
          </el-col>
        </el-row>
        <div v-if="books.length === 0" class="no-books">
          <el-empty description="暂无书籍"></el-empty>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const books = ref([])

const categoryName = computed(() => {
  const type = route.params.type
  const categoryMap = {
    '教材类': '教材类',
    '考研资料': '考研资料',
    '课外阅读': '课外阅读',
    '其他': '其他'
  }
  return categoryMap[type] || '分类浏览'
})

const getBooksByCategory = async () => {
  const type = route.params.type
  try {
    const { data } = await axios.get('/api/books/search', {
      params: {
        category: type
      }
    })
    if (data.code === 200) {
      books.value = data.data
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    ElMessage.error('获取书籍列表失败')
  } finally {
    loading.value = false
  }
}

const goToDetail = (id) => {
  router.push(`/book/${id}`)
}

onMounted(() => {
  getBooksByCategory()
})
</script>

<style scoped>
.category-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.category-card {
  margin-bottom: 20px;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-header h2 {
  margin: 0;
  color: #333;
}

.book-list {
  margin-top: 20px;
}

.book-item {
  margin-bottom: 20px;
  cursor: pointer;
}

.book-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.book-info {
  padding: 15px;
}

.book-title {
  font-size: 16px;
  margin: 0 0 10px 0;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.book-author {
  font-size: 14px;
  color: #666;
  margin: 0 0 10px 0;
}

.book-price {
  font-size: 18px;
  font-weight: bold;
  color: #f56c6c;
  margin: 0 0 10px 0;
}

.book-condition {
  font-size: 14px;
  color: #909399;
  margin: 0 0 10px 0;
}

.book-seller {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.no-books {
  text-align: center;
  padding: 100px 0;
}
</style>