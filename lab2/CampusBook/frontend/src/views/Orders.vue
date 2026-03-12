<template>
  <div class="orders-container">
    <el-card class="orders-card">
      <template #header>
        <div class="orders-header">
          <h2>我的订单</h2>
        </div>
      </template>
      <div class="order-tabs">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="全部" name="all">
            <order-list :orders="orders" @view-detail="viewDetail" @cancel-order="cancelOrder" @confirm-receipt="confirmReceipt"></order-list>
          </el-tab-pane>
          <el-tab-pane label="待付款" name="0">
            <order-list :orders="filterOrders(0)" @view-detail="viewDetail" @cancel-order="cancelOrder" @confirm-receipt="confirmReceipt"></order-list>
          </el-tab-pane>
          <el-tab-pane label="待发货" name="1">
            <order-list :orders="filterOrders(1)" @view-detail="viewDetail" @cancel-order="cancelOrder" @confirm-receipt="confirmReceipt"></order-list>
          </el-tab-pane>
          <el-tab-pane label="待收货" name="2">
            <order-list :orders="filterOrders(2)" @view-detail="viewDetail" @cancel-order="cancelOrder" @confirm-receipt="confirmReceipt"></order-list>
          </el-tab-pane>
          <el-tab-pane label="已完成" name="3">
            <order-list :orders="filterOrders(3)" @view-detail="viewDetail" @cancel-order="cancelOrder" @confirm-receipt="confirmReceipt"></order-list>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const activeTab = ref('all')
const orders = ref([])

const getOrders = async () => {
  try {
    const { data } = await axios.get('/api/orders')
    if (data.code === 200) {
      orders.value = data.data
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    ElMessage.error('获取订单列表失败')
  }
}

const filterOrders = (status) => {
  return orders.value.filter(order => order.status === status)
}

const viewDetail = (id) => {
  router.push(`/order/${id}`)
}

const cancelOrder = async (id) => {
  try {
    const { data } = await axios.put(`/api/orders/${id}/cancel`)
    if (data.code === 200) {
      ElMessage.success('订单已取消')
      getOrders()
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    ElMessage.error('取消订单失败')
  }
}

const confirmReceipt = async (id) => {
  try {
    const { data } = await axios.put(`/api/orders/${id}/confirm`)
    if (data.code === 200) {
      ElMessage.success('确认收货成功')
      getOrders()
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    ElMessage.error('确认收货失败')
  }
}

onMounted(() => {
  getOrders()
})
</script>

<style scoped>
.orders-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.orders-card {
  margin-bottom: 20px;
}

.orders-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.orders-header h2 {
  margin: 0;
  color: #333;
}

.order-tabs {
  margin-top: 20px;
}
</style>

<!-- 订单列表组件 -->
<script setup>
const props = defineProps({
  orders: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['view-detail', 'cancel-order', 'confirm-receipt'])
</script>

<template>
  <div class="order-list">
    <div v-if="orders.length === 0" class="no-orders">
      <el-empty description="暂无订单"></el-empty>
    </div>
    <el-card v-for="order in orders" :key="order.id" class="order-card">
      <div class="order-header">
        <span class="order-no">订单号：{{ order.order_no }}</span>
        <span class="order-status" :class="`status-${order.status}`">{{ order.status_text }}</span>
      </div>
      <div class="order-content">
        <div class="order-book">
          <h3>{{ order.book_title }}</h3>
          <p class="order-price">¥{{ order.price }}</p>
        </div>
        <div class="order-address">
          <p>{{ order.address }}</p>
        </div>
      </div>
      <div class="order-footer">
        <span class="order-time">{{ order.created_at }}</span>
        <div class="order-actions">
          <el-button size="small" @click="$emit('view-detail', order.id)">查看详情</el-button>
          <el-button size="small" type="danger" v-if="order.status === 0" @click="$emit('cancel-order', order.id)">取消订单</el-button>
          <el-button size="small" type="primary" v-if="order.status === 2" @click="$emit('confirm-receipt', order.id)">确认收货</el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.order-list {
  margin-top: 20px;
}

.no-orders {
  text-align: center;
  padding: 100px 0;
}

.order-card {
  margin-bottom: 20px;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e4e7ed;
}

.order-no {
  font-size: 14px;
  color: #666;
}

.order-status {
  font-size: 14px;
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

.order-content {
  margin-bottom: 15px;
}

.order-book {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.order-book h3 {
  font-size: 16px;
  margin: 0;
  color: #333;
}

.order-price {
  font-size: 18px;
  font-weight: bold;
  color: #f56c6c;
  margin: 0;
}

.order-address {
  font-size: 14px;
  color: #666;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid #e4e7ed;
}

.order-time {
  font-size: 12px;
  color: #909399;
}

.order-actions {
  display: flex;
  gap: 10px;
}
</style>