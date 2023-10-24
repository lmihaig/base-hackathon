<template>
  <div class="container">
    <div class="left">
      <h1>Create Dog</h1>
      <form @submit.prevent="createDog">
        <div>
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="newDog.name" required />
        </div>
        <div>
          <label for="age">Age:</label>
          <input type="number" id="age" v-model="newDog.age" required />
        </div>
        <div>
          <button type="submit">Create Dog</button>
        </div>
      </form>
    </div>
    <div class="right">
      <h1>Dog List</h1>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Age</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(dog, index) in dogs" :key="dog._id">
            <td>{{ index + 1 }}</td>
            <td>{{ dog.name }}</td>
            <td>{{ dog.age }} years old</td>
            <td>
              <button @click="openEditModal(dog)">Edit</button>
              <button @click="deleteDog(dog)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="modal" v-if="editingDog">
    <div class="modal-content">
      <h2>Edit Dog</h2>
      <form @submit.prevent="saveEditedDog">
        <div>
          <label for="editName">Name:</label>
          <input type="text" id="editName" v-model="editingDog.name" required />
        </div>
        <div>
          <label for="editAge">Age:</label>
          <input type="number" id="editAge" v-model="editingDog.age" required />
        </div>
        <div>
          <button type="submit">Save</button>
          <button @click="closeEditModal">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
const DOGS_API_URL = "http://localhost:8000";

import axios from "axios";

export default {
  data() {
    return {
      newDog: { name: "", age: null },
      dogs: [],
      editingDog: null,
    };
  },
  created() {
    this.fetchDogs();
  },
  methods: {
    async fetchDogs() {
      try {
        const response = await axios.get(`${DOGS_API_URL}/dogs`);
        this.dogs = response.data;
      } catch (error) {
        console.error("Error fetching dogs:", error);
      }
    },
    async createDog() {
      try {
        await axios.post(`${DOGS_API_URL}/dogs`, this.newDog);
        this.newDog = { name: "", age: null };
        this.fetchDogs();
      } catch (error) {
        console.error("Error creating dog:", error);
      }
    },
    editDog(dog) {
      this.editingDog = { ...dog };
    },
    openEditModal(dog) {
      this.editingDog = { ...dog };
    },
    closeEditModal() {
      this.editingDog = null;
    },
    async saveEditedDog() {
      try {
        await axios.put(`${DOGS_API_URL}/dogs/${this.editingDog._id}`, this.editingDog);
        this.closeEditModal();
        this.fetchDogs();
      } catch (error) {
        console.error("Error updating dog:", error);
      }
    },
    async deleteDog(dog) {
      try {
        await axios.delete(`${DOGS_API_URL}/dogs/${dog._id}`);
        this.fetchDogs();
      } catch (error) {
        console.error("Error deleting dog:", error);
      }
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
}

.left {
  flex: 1;
  padding: 20px;
}

.right {
  flex: 2;
  padding: 20px;
}


.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-content {
  background-color: #525151;
  padding: 20px;
  border-radius: 5px;
}
</style>
