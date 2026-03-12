<template>
  <div class="address-container">
    <el-card class="address-card">
      <template #header>
        <div class="address-header">
          <h2>收货地址管理</h2>
          <el-button type="primary" @click="showAddDialog = true">新增地址</el-button>
        </div>
      </template>
      <div v-loading="loading" class="address-list">
        <div v-if="addresses.length === 0" class="no-addresses">
          <el-empty description="暂无地址"></el-empty>
        </div>
        <el-card v-for="address in addresses" :key="address.id" class="address-item">
          <div class="address-content">
            <div class="address-info">
              <h3>{{ address.receiver }} {{ address.phone }}</h3>
              <p>{{ address.address }}</p>
            </div>
            <div class="address-actions">
              <el-button size="small" @click="editAddress(address)">编辑</el-button>
              <el-button size="small" type="danger" @click="deleteAddress(address.id)">删除</el-button>
              <el-button size="small" v-if="!address.is_default" @click="setDefault(address.id)">设为默认</el-button>
              <el-tag v-else type="success" size="small">默认</el-tag>
            </div>
          </div>
        </el-card>
      </div>
    </el-card>

    <!-- 新增/编辑地址对话框 -->
    <el-dialog
      v-model="showAddDialog"
      :title="dialogTitle"
      width="500px"
    >
      <el-form :model="addressForm" :rules="rules" ref="addressFormRef" label-width="80px">
        <el-form-item label="收货人" prop="receiver">
          <el-input v-model="addressForm.receiver" placeholder="请输入收货人姓名"></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="addressForm.phone" placeholder="请输入手机号"></el-input>
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="addressForm.address" type="textarea" rows="3" placeholder="请输入详细地址"></el-input>
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="addressForm.is_default">设为默认地址</el-checkbox>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddDialog = false">取消</el-button>
          <el-button type="primary" @click="saveAddress">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(true)
const addresses = ref([])
const showAddDialog = ref(false)
const addressFormRef = ref(null)
const editingAddressId = ref(null)

const dialogTitle = ref('新增地址')

const addressForm = ref({
  receiver: '',
  phone: '',
  address: '',
  is_default: 0
})

const rules = {
  receiver: [{ required: true, message: '请输入收货人姓名', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
  address: [{ required: true, message: '请输入详细地址', trigger: 'blur' }]
}

const getAddresses = async () => {
  try {
    const { data } = await axios.get('/api/addresses')
    if (data.code === 200) {
      addresses.value = data.data
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    ElMessage.error('获取地址列表失败')
  } finally {
    loading.value = false
  }
}

const saveAddress = async () => {
  if (!addressFormRef.value) return
  
  try {
    let response
    if (editingAddressId.value) {
      // 更新地址
      response = await axios.put(`/api/addresses/${editingAddressId.value}`, addressForm.value)
    } else {
      // 新增地址
      response = await axios.post('/api/addresses', addressForm.value)
    }
    
    if (response.data.code === 200) {
      ElMessage.success(editingAddressId.value ? '地址更新成功' : '地址添加成功')
      showAddDialog.value = false
      getAddresses()
      resetForm()
    } else {
      ElMessage.error(response.data.message)
    }
  } catch (error) {
    ElMessage.error('保存地址失败，请稍后重试')
  }
}

const editAddress = (address) => {
  editingAddressId.value = address.id
  addressForm.value = {
    receiver: address.receiver,
    phone: address.phone,
    address: address.address,
    is_default: address.is_default
  }
  dialogTitle.value = '编辑地址'
  showAddDialog.value = true
}

const deleteAddress = async (id) => {
  try {
    const { data } = await axios.delete(`/api/addresses/${id}`)
    if (data.code === 200) {
      ElMessage.success('地址删除成功')
      getAddresses()
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    ElMessage.error('删除地址失败，请稍后重试')
  }
}

const setDefault = async (id) => {
  try {
    const { data } = await axios.put(`/api/addresses/${id}`, { is_default: 1 })
    if (data.code === 200) {
      ElMessage.success('设置默认地址成功')
      getAddresses()
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    ElMessage.error('设置默认地址失败，请稍后重试')
  }
}

const resetForm = () => {
  addressForm.value = {
    receiver: '',
    phone: '',
    address: '',
    is_default: 0
  }
  editingAddressId.value = null
  dialogTitle.value = '新增地址'
}

onMounted(() => {
  getAddresses()
})
</script>

<style scoped>
.address-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.address-card {
  margin-bottom: 20px;
}

.address-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.address-header h2 {
  margin: 0;
  color: #333;
}

.address-list {
  margin-top: 20px;
}

.no-addresses {
  text-align: center;
  padding: 100px 0;
}

.address-item {
  margin-bottom: 15px;
}

.address-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.address-info h3 {
  font-size: 16px;
  margin: 0 0 10px 0;
  color: #333;
}

.address-info p {
  font-size: 14px;
  color: #666;
  margin: 0;
  line-height: 1.5;
}

.address-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>