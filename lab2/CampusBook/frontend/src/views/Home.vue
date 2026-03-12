<template>
  <div class="home-container">
    <!-- 搜索栏 -->
    <div class="search-bar">
      <div class="search-content">
        <el-input
          v-model="searchKeyword"
          placeholder="请输入书名搜索"
          class="search-input"
          @keyup.enter="search"
        >
          <template #append>
            <el-button @click="search"><el-icon><Search /></el-icon></el-button>
          </template>
        </el-input>
        <div class="category-buttons">
          <el-button v-for="category in categories" :key="category.value" @click="goToCategory(category.value)">{{ category.label }}</el-button>
        </div>
      </div>
    </div>

    <!-- 书籍列表 -->
    <el-card class="books-card">
      <template #header>
        <div class="books-header">
          <h2>最新发布</h2>
          <el-button type="primary" @click="$router.push('/publish')">发布书籍</el-button>
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { Search } from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(true)
const books = ref([])
const searchKeyword = ref('')

const categories = [
  { label: '教材类', value: '教材类' },
  { label: '考研资料', value: '考研资料' },
  { label: '课外阅读', value: '课外阅读' },
  { label: '其他', value: '其他' }
]

const getBooks = async () => {
  try {
    const { data } = await axios.get('/api/books')
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

const search = () => {
  if (searchKeyword.value) {
    router.push({ path: '/search', query: { keyword: searchKeyword.value } })
  }
}

const goToCategory = (category) => {
  router.push(`/category/${category}`)
}

const goToDetail = (id) => {
  router.push(`/book/${id}`)
}

onMounted(() => {
  getBooks()
})
</script>

<style scoped>
.home-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.search-bar {
  background-color: #409eff;
  padding: 30px 0;
  margin-bottom: 20px;
}

.search-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.search-input {
  width: 400px;
  margin-right: 20px;
}

.category-buttons {
  margin-top: 20px;
}

.books-card {
  margin-bottom: 20px;
}

.books-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.books-header h2 {
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