<template>
  <div class="order-detail-container">
    <el-card v-loading="loading" class="order-detail-card">
      <template #header>
        <div class="order-detail-header">
          <h2>订单详情</h2>
        </div>
      </template>
      <div v-if="order" class="order-detail">
        <div class="order-info">
          <div class="order-basic">
            <p><span class="label">订单号：</span>{{ order.order_no }}</p>
            <p><span class="label">订单状态：</span><span class="status" :class="`status-${order.status}`">{{ order.status_text }}</span></p>
            <p><span class="label">创建时间：</span>{{ order.created_at }}</p>
            <p><span class="label">更新时间：</span>{{ order.updated_at }}</p>
          </div>
          <div class="order-price">
            <p><span class="label">订单总价：</span><span class="price">¥{{ order.total_price }}</span></p>
          </div>
        </div>
        <div class="order-book">
          <h3>书籍信息</h3>
          <el-card :body-style="{ padding: '0px' }">
            <div class="book-info">
              <img :src="order.book.images[0] || 'https://via.placeholder.com/100'" class="book-img" alt="book cover" />
              <div class="book-details">
                <h4>{{ order.book.title }}</h4>
                <p class="author">作者：{{ order.book.author }}</p>
                <p class="price">价格：¥{{ order.book.price }}</p>
              </div>
            </div>
          </el-card>
        </div>
        <div class="order-seller">
          <h3>卖家信息</h3>
          <el-card>
            <p><span class="label">昵称：</span>{{ order.seller.nickname }}</p>
            <p><span class="label">手机号：</span>{{ order.seller.phone }}</p>
          </el-card>
        </div>
        <div class="order-address">
          <h3>收货地址</h3>
          <el-card>
            <p><span class="label">收货人：</span>{{ order.address.receiver }}</p>
            <p><span class="label">手机号：</span>{{ order.address.phone }}</p>
            <p><span class="label">地址：</span>{{ order.address.address }}</p>
          </el-card>
        </div>
        <div class="order-actions">
          <el-button v-if="order.status === 0" type="danger" @click="cancelOrder">取消订单</el-button>
          <el-button v-if="order.status === 2" type="primary" @click="confirmReceipt">确认收货</el-button>
          <el-button @click="goBack">返回</el-button>
        </div>
      </div>
      <div v-else class="no-order">
        <el-empty description="订单不存在"></el-empty>
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
const order = ref(null)

const getOrderDetail = async () => {
  const id = route.params.id
  try {
    const { data } = await axios.get(`/api/orders/${id}`)
    if (data.code === 200) {
      order.value = data.data
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    ElMessage.error('获取订单详情失败')
  } finally {
    loading.value = false
  }
}

const cancelOrder = async () => {
  try {
    const { data } = await axios.put(`/api/orders/${order.value.id}/cancel`)
    if (data.code === 200) {
      ElMessage.success('订单已取消')
      getOrderDetail()
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    ElMessage.error('取消订单失败')
  }
}

const confirmReceipt = async () => {
  try {
    const { data } = await axios.put(`/api/orders/${order.value.id}/confirm`)
    if (data.code === 200) {
      ElMessage.success('确认收货成功')
      getOrderDetail()
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    ElMessage.error('确认收货失败')
  }
}

const goBack = () => {
  router.push('/orders')
}

onMounted(() => {
  getOrderDetail()
})
</script>

<style scoped>
.order-detail-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.order-detail-card {
  margin-bottom: 20px;
}

.order-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-detail-header h2 {
  margin: 0;
  color: #333;
}

.order-detail {
  margin-top: 20px;
}

.order-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.order-basic p {
  margin: 5px 0;
  font-size: 14px;
}

.order-price p {
  margin: 5px 0;
  font-size: 14px;
}

.label {
  font-weight: bold;
  color: #666;
}

.status {
  font-weight: bold;
}

.status-0 {
  color: #e6a23c;
}

.status-1 {
  color: #409eff;
}

.status-2 {
  color: #67c23a;
}

.status-3 {
  color: #909399;
}

.status-4 {
  color: #f56c6c;
}

.price {
  font-size: 18px;
  font-weight: bold;
  color: #f56c6c;
}

.order-book,
.order-seller,
.order-address {
  margin-bottom: 20px;
}

.order-book h3,
.order-seller h3,
.order-address h3 {
  font-size: 16px;
  margin: 0 0 10px 0;
  color: #333;
}

.book-info {
  display: flex;
  padding: 15px;
}

.book-img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  margin-right: 15px;
}

.book-details {
  flex: 1;
}

.book-details h4 {
  font-size: 16px;
  margin: 0 0 10px 0;
  color: #333;
}

.book-details p {
  margin: 5px 0;
  font-size: 14px;
  color: #666;
}

.order-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.no-order {
  text-align: center;
  padding: 100px 0;
}
</style>