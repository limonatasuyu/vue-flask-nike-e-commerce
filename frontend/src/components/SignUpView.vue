<template>
<div class='signup-page-container grid'>
	<div>
		<h1 class='main-header'>Sign Up</h1>
		<form class='signup-form grid'>
			<div class="email-input-wrapper flex">
				<label for='email-input' >email</label>
				<input type='email' class='email-input' id='email-input' v-model='email' />
			</div>
			<div v-if='postResponse && postResponse.data.cause == "email"' class='email-denied-info denied-info'>
				<p>{{postResponse.data.msg}}</p>
			</div>
			<div class="username-input-wrapper flex">
				<label for='username-input' >username</label>
				<input class='username-input' id='username-input' v-model='username' />
			</div>
			<div v-if='postResponse && postResponse.data.cause == "username"' class='username-denied-info denied-info'>
				<p>{{postResponse.data.msg}}</p>
			</div>
			<div class="password-input-wrapper flex">
				<label for='password-input' >password</label>
				<input type='password' class='password-input' id='password-input' v-model='password' />
			</div>
			<div class='verify-password-input-wrapper flex'>
				<label for="verify-password-input">verify password</label>
				<input type='password' class='verify-password-input' id='verify-password-input' v-model='verifyPassword'/>
			</div>
			<p class='form-text'>Already have an account? <span @click='toggleLogin'>Log In.</span></p>
			<button class='signup-button button' @click='signUpUser'>Sign Up</button>
		</form>
	</div>
</div>
</template>
<script>
import axios from 'axios'

export default {
	data() {
		return {
			email: '',
			username: '',
			password: '',
			verifyPassword: '',
			arePasswordsSame: true,
			postResponse: null,
		}
	},
	watch: {
		verifyPassword() {
			if (this.password !== this.verifyPassword) {this.arePasswordsSame = false}
			else {this.arePasswordsSame = true}
		},
		password() {
			if (this.password !== this.verifyPassword) {this.arePasswordsSame = false}
			else {this.arePasswordsSame = true}
		},
		postResponse() {
			if (this.postResponse.data.success === true) {this.$router.push('/')}
		}
	},
	methods: {
		signUpUser(e) {
			e.preventDefault();	
			
			if (!this.arePasswordsSame) {alert('passwords are not the same'); return}
			if (this.password.length <= 8) {alert('password needs to be longer then 8 characters'); return}
			if (this.username.length <= 6) {alert('username needs to be longer then 6 characters'); return}	
			if (!this.ValidateEmail(this.email))	{alert('email is invalid'); return}

			let payload = {
				email: this.email,
				username: this.username,
				password: this.password
			}
			
			axios.post(`${process.env.VUE_APP_API_URL ?? "http://localhost:5000"}/sign-user`, payload)
				.then(res => {this.postResponse = res; console.log(res.data)})
				.catch(err => console.log(err))

		}
	},
	props: ['toggleLogin', 'ValidateEmail']
}
</script>
<style scoped>
.signup-page-container {
	background-color: var(--bg-clr-secondary);
	justify-content: center; align-items: center;
	height: 70vh;
}

.main-header {text-align: center; }

.signup-form {gap: .5rem; margin-top: 2.5rem;}
.signup-form > div {height: 1.4rem;}
label {width: 8rem;}

.denied-info {
	background-color: rgba(243, 32, 19, .7);
	border: 2px rgba(243, 32, 19, 1) solid;
	border-radius: 5px;
}

.denied-info p {margin: 0; margin-left: .4rem;}



.form-text {text-align: center; color: var(--clr-other);}
.form-text span {color: var(--text-clr-primary); cursor: pointer;}

.signup-button {
	background-color: var(--bg-clr-tertiary);
	color: white;
}

@media screen and (max-width: 390px) {
	.signup-form > div {display: grid; margin-top: 1.8rem;}
	.signup-form input {margin-top: .2rem;}
}
</style>
