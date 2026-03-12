<template>
  <div class="search-container">
    <el-card class="search-card">
      <template #header>
        <div class="search-header">
          <h2>搜索结果</h2>
          <el-input
            v-model="searchForm.keyword"
            placeholder="请输入书名"
            class="search-input"
            @keyup.enter="search"
          >
            <template #append>
              <el-button @click="search"><el-icon><Search /></el-icon></el-button>
            </template>
          </el-input>
        </div>
      </template>
      <div class="filter-container">
        <el-form :model="searchForm" inline>
          <el-form-item label="分类">
            <el-select v-model="searchForm.category" placeholder="全部">
              <el-option label="全部" value=""></el-option>
              <el-option label="教材类" value="教材类"></el-option>
              <el-option label="考研资料" value="考研资料"></el-option>
              <el-option label="课外阅读" value="课外阅读"></el-option>
              <el-option label="其他" value="其他"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="成色">
            <el-select v-model="searchForm.condition" placeholder="全部">
              <el-option label="全部" value=""></el-option>
              <el-option label="全新" value="全新"></el-option>
              <el-option label="九成新" value="九成新"></el-option>
              <el-option label="八成新" value="八成新"></el-option>
              <el-option label="七成新" value="七成新"></el-option>
              <el-option label="及以下" value="及以下"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="价格区间">
            <el-input-number v-model="searchForm.min_price" placeholder="最低价" :min="0" style="width: 100px"></el-input-number>
            <span style="margin: 0 10px">-</span>
            <el-input-number v-model="searchForm.max_price" placeholder="最高价" :min="0" style="width: 100px"></el-input-number>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="search">筛选</el-button>
            <el-button @click="reset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
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
          <el-empty description="暂无搜索结果"></el-empty>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { Search } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const loading = ref(true)
const books = ref([])

const searchForm = ref({
  keyword: '',
  category: '',
  condition: '',
  min_price: 0,
  max_price: 999999
})

const search = async () => {
  loading.value = true
  try {
    const { data } = await axios.get('/api/books/search', {
      params: searchForm.value
    })
    if (data.code === 200) {
      books.value = data.data
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    ElMessage.error('搜索失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const reset = () => {
  searchForm.value = {
    keyword: '',
    category: '',
    condition: '',
    min_price: 0,
    max_price: 999999
  }
  search()
}

const goToDetail = (id) => {
  router.push(`/book/${id}`)
}

onMounted(() => {
  // 从路由参数中获取搜索关键词
  const keyword = route.query.keyword
  if (keyword) {
    searchForm.value.keyword = keyword
  }
  search()
})
</script>

<style scoped>
.search-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.search-card {
  margin-bottom: 20px;
}

.search-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-header h2 {
  margin: 0;
  color: #333;
}

.search-input {
  width: 300px;
}

.filter-container {
  margin: 20px 0;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
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