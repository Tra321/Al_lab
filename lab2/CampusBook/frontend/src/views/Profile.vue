<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="profile-header">
          <h2>个人中心</h2>
        </div>
      </template>
      <div v-loading="loading" class="profile-content">
        <div v-if="user" class="user-info">
          <div class="avatar-section">
            <el-avatar :size="100" :src="user.avatar || defaultAvatar" class="user-avatar"></el-avatar>
            <el-button type="primary" size="small" @click="uploadAvatar">更换头像</el-button>
          </div>
          <div class="user-details">
            <el-form :model="userForm" :rules="rules" ref="userFormRef" label-width="80px">
              <el-form-item label="昵称" prop="nickname">
                <el-input v-model="userForm.nickname"></el-input>
              </el-form-item>
              <el-form-item label="手机号" prop="phone">
                <el-input v-model="userForm.phone"></el-input>
              </el-form-item>
              <el-form-item label="邮箱" prop="email">
                <el-input v-model="userForm.email"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="updateProfile">保存修改</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
        <div v-else class="no-user">
          <el-empty description="请先登录"></el-empty>
          <el-button type="primary" @click="$router.push('/login')">去登录</el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(true)
const user = ref(null)
const userForm = ref({})
const userFormRef = ref(null)
const defaultAvatar = 'https://via.placeholder.com/100'

const rules = {
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }]
}

const getProfile = async () => {
  try {
    const { data } = await axios.get('/api/user/profile')
    if (data.code === 200) {
      user.value = data.data
      userForm.value = {
        nickname: user.value.nickname,
        phone: user.value.phone,
        email: user.value.email
      }
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    ElMessage.error('获取个人信息失败')
  } finally {
    loading.value = false
  }
}

const updateProfile = async () => {
  if (!userFormRef.value) return
  
  try {
    const { data } = await axios.put('/api/user/profile', userForm.value)
    if (data.code === 200) {
      ElMessage.success('更新成功')
      getProfile()
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    ElMessage.error('更新失败，请稍后重试')
  }
}

const uploadAvatar = () => {
  // 这里应该实现头像上传功能，暂时使用模拟
  ElMessage.info('头像上传功能待实现')
}

onMounted(() => {
  getProfile()
})
</script>

<style scoped>
.profile-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.profile-card {
  margin-bottom: 20px;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile-header h2 {
  margin: 0;
  color: #333;
}

.profile-content {
  margin-top: 20px;
}

.user-info {
  display: flex;
  gap: 30px;
}

.avatar-section {
  flex: 0 0 150px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  margin-bottom: 10px;
}

.user-details {
  flex: 1;
}

.no-user {
  text-align: center;
  padding: 100px 0;
}

.no-user .el-button {
  margin-top: 20px;
}
</style>