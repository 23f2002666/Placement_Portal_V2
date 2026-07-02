<template>
<div class="container d-flex justify-content-center align-items-center" style="height:80vh;">
    
    <!-- The Card Container from Code 2 -->
    <div class="card shadow p-4" style="width:350px; border-radius:12px;">
        
        <!-- Header with Emoji -->
        <h3 class="text-center mb-4">🔐 Login</h3>

        <!-- Keep Vue's @submit.prevent -->
        <form @submit.prevent="login">

            <!-- Email Input -->
            <div class="mb-3">
                <label class="form-label">Email address</label>
                <input 
                    type="email" 
                    class="form-control" 
                    placeholder="Enter email"
                    v-model="email" 
                    required
                >
            </div>

            <!-- Password Input with your validation logic -->
            <div class="mb-3">
                <label class="form-label">Password</label>
                <input 
                    type="password" 
                    class="form-control" 
                    placeholder="Enter password"
                    v-model="password" 
                    @input="validatePassword" 
                    required
                >
                <!-- Vue Validation Message -->
                <div v-if="passwordError" class="form-text text-danger" style="font-size: 0.8rem;">
                    {{ passwordError }}
                </div>
            </div>

            <!-- Full-width Button using d-grid -->
            <div class="d-grid">
                <button class="btn btn-primary" type="submit">Login</button>
            </div>

        </form>
        
        <!-- Optional: Link to Register since it's a Portal -->
        <div class="text-center mt-3">
            <small>Don't have an account? <router-link to="/register">Register</router-link></small>
        </div>

    </div>
</div>

</template>

<script setup>
import { ref } from 'vue';

const email = ref('');
const password = ref('');

const passwordError = ref('');

const validatePassword = () => {
    if (password.value.length < 8) {
        passwordError.value = 'Password must be at least 8 characters long.';
        return false;
    } else {
        passwordError.value = '';
        return true; 
    }
};



async function login() {
    if (!validatePassword()) {
        alert('Invalid password length.');
        return;
    }
    
    if (email.value === '' || password.value === '') {
        alert('Please fill in all fields.');
        return;
    }

    const response= await fetch('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email.value,
            password: password.value
        })
    });
    
    console.log(response);

    if (!response.ok) {
        const data = await response.json();
        console.error('Login failed:', data.message);
        alert('Login failed: ' + data.message);
    
    }else{
        const data = await response.json();
        console.log('Login successful:', data);

        localStorage.setItem('token', data.user.auth_token);
        alert(data.message);
        return;
    }
}

</script>