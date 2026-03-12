<template>
  <div class="publish-container">
    <el-card class="publish-card">
      <h2>发布二手书籍</h2>
      <el-form :model="bookForm" :rules="rules" ref="bookFormRef" label-width="120px">
        <el-form-item label="书名" prop="title">
          <el-input v-model="bookForm.title" placeholder="请输入书名"></el-input>
        </el-form-item>
        <el-form-item label="作者" prop="author">
          <el-input v-model="bookForm.author" placeholder="请输入作者"></el-input>
        </el-form-item>
        <el-form-item label="ISBN" prop="isbn">
          <el-input v-model="bookForm.isbn" placeholder="请输入ISBN码"></el-input>
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="bookForm.category" placeholder="请选择分类">
            <el-option label="教材类" value="教材类"></el-option>
            <el-option label="考研资料" value="考研资料"></el-option>
            <el-option label="课外阅读" value="课外阅读"></el-option>
            <el-option label="其他" value="其他"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="成色" prop="condition">
          <el-select v-model="bookForm.condition" placeholder="请选择成色">
            <el-option label="全新" value="全新"></el-option>
            <el-option label="九成新" value="九成新"></el-option>
            <el-option label="八成新" value="八成新"></el-option>
            <el-option label="七成新" value="七成新"></el-option>
            <el-option label="及以下" value="及以下"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input v-model.number="bookForm.price" type="number" placeholder="请输入价格"></el-input>
        </el-form-item>
        <el-form-item label="库存" prop="stock">
          <el-input v-model.number="bookForm.stock" type="number" placeholder="请输入库存"></el-input>
        </el-form-item>
        <el-form-item label="交易方式" prop="delivery_type">
          <el-select v-model="bookForm.delivery_type" placeholder="请选择交易方式">
            <el-option label="仅自提" value="仅自提"></el-option>
            <el-option label="仅快递" value="仅快递"></el-option>
            <el-option label="自提+快递" value="自提+快递"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="书籍描述" prop="description">
          <el-input v-model="bookForm.description" type="textarea" rows="4" placeholder="请输入书籍描述"></el-input>
        </el-form-item>
        <el-form-item label="书籍图片" prop="images">
          <el-upload
            class="upload-demo"
            action="#"
            :on-change="handleImageChange"
            :multiple="true"
            :limit="3"
            :auto-upload="false"
          >
            <el-button type="primary">选择图片</el-button>
            <template #tip>
              <div class="el-upload__tip">
                最多上传3张图片
              </div>
            </template>
          </el-upload>
          <div class="image-list">
            <el-image 
              v-for="(image, index) in bookForm.images" 
              :key="index" 
              :src="image" 
              fit="cover"
              class="uploaded-image"
            >
              <template #error>
                <div class="image-error">图片加载失败</div>
              </template>
              <template #footer>
                <el-button size="small" type="danger" @click="removeImage(index)">删除</el-button>
              </template>
            </el-image>
          </div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="publish">发布</el-button>
          <el-button @click="reset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const bookFormRef = ref(null)

const bookForm = reactive({
  title: '',
  author: '',
  isbn: '',
  category: '',
  condition: '',
  price: 0,
  stock: 1,
  delivery_type: '',
  description: '',
  images: []
})

const rules = {
  title: [{ required: true, message: '请输入书名', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  condition: [{ required: true, message: '请选择成色', trigger: 'change' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  delivery_type: [{ required: true, message: '请选择交易方式', trigger: 'change' }]
}

const handleImageChange = (file) => {
  // 这里应该处理图片上传，暂时使用本地路径模拟
  bookForm.images.push(URL.createObjectURL(file.raw))
}

const removeImage = (index) => {
  bookForm.images.splice(index, 1)
}

const publish = async () => {
  if (!bookFormRef.value) return
  
  try {
    const { data } = await axios.post('/api/books', bookForm)
    if (data.code === 200) {
      ElMessage.success('发布成功')
      router.push('/')
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    ElMessage.error('发布失败，请稍后重试')
  }
}

const reset = () => {
  bookFormRef.value.resetFields()
  bookForm.images = []
}
</script>

<style scoped>
.publish-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.publish-card {
  margin-bottom: 20px;
}

.publish-card h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.image-list {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.uploaded-image {
  width: 100px;
  height: 100px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
}

.image-error {
  width: 100px;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
  color: #909399;
}
</style>