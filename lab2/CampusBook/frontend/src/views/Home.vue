<template>
  <div class="home">
    <h1>校园二手书交易平台</h1>
    <div class="book-list">
      <div v-for="book in books" :key="book.id" class="book-item">
        <h3>{{ book.title }}</h3>
        <p>作者: {{ book.author }}</p>
        <p>价格: ¥{{ book.price }}</p>
        <p>成色: {{ book.condition }}</p>
        <el-button type="primary" @click="goToDetail(book.id)">查看详情</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const books = ref([])

// 模拟数据
const mockBooks = [
  {
    id: 1,
    title: '大学英语四级词汇',
    author: '王长喜',
    price: 25.00,
    condition: '九成新',
    category: '教材类'
  },
  {
    id: 2,
    title: '高等数学',
    author: '同济大学数学系',
    price: 30.00,
    condition: '八成新',
    category: '教材类'
  },
  {
    id: 3,
    title: 'Python编程从入门到精通',
    author: '黑马程序员',
    price: 45.00,
    condition: '全新',
    category: '课外阅读'
  }
]

onMounted(() => {
  // 模拟API请求
  books.value = mockBooks
})

const goToDetail = (id) => {
  router.push(`/book/${id}`)
}
</script>

<style scoped>
.home {
  padding: 20px;
}

.book-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.book-item {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.book-item h3 {
  margin-bottom: 10px;
}

.book-item p {
  margin: 5px 0;
}
</style>