<template>
<div class='login-form-wrapper'>
	<div class='login-form-container grid'>
		<img src='@/assets/cross.png' class='close-form-icon' @click='toggleLogin'>
		<h1 class='main-header'>Log In</h1>
		<form class='login-form grid'>
			<div v-if='postResponse && !postResponse.success' class='denied-info-wrapper'>
				<p>{{postResponse.msg}}</p>
			</div>
			<div class='email-input-wrapper flex'>
				<label for='email_username'>e-mail /<br/>username</label>
				<input class='email-input' id='email_username' v-model='email_username'/>
			</div>
			<div class='password-input-wrapper flex'>
				<label for='password'>password</label>
				<input class='password-input' id='password' v-model='password' type='password'/>
			</div>
			<p class='forget-password-text'>Forget password?</p>
			<p class='signup-text'>Not Have an account? <router-link to='signup' @click='toggleLogin'>Sign up.</router-link></p>
			<button class='login-button button' @click='loginUser'>Log In</button>
		</form>
	</div>
</div>
</template>
<script>
import axios from 'axios'

export default {
	data() {
		return {
			email_username: '',
			password: '',
			postResponse: null,
		}
	},
	methods: {
		loginUser(e) {

			e.preventDefault();
			this.postResponse = null; // This makes user warning to go away (for a second if user makes a mistake again).

			let payload = {
				email_username: this.email_username,
				password: this.password
			}
			let config = {
				withCredentials: true
			}

			axios.post('http://localhost:5000/log-user', payload, config)
				.then((res) => {this.postResponse = res.data})
				.catch(err => console.log(err))

		}
	},
	props: ['toggleLogin', 'getUserInfo'],
	watch: {
		postResponse() {
			if (this.postResponse.success === true) {
				this.toggleLogin();
				this.getUserInfo();
			}
		}
	}
}
</script>
<style scoped>
.login-form-wrapper {
	width: 100vw; height: 100vh;
	position: absolute;
	top: 0; bottom: 0; left: 0; right: 0;
	z-index: 2;
	background-color: rgba(0, 0, 0, .5);
	display: flex;
	justify-content: center;
	align-items: center;	
}
.login-form-container {
	width: 17.5rem; height: 25rem;
	padding: 0 1rem 1rem;
	background-color: var(--bg-clr-primary);
	border-radius: 10px;
}

.close-form-icon {width: 2rem; justify-self: end; margin-top: 1rem; cursor: pointer;}

.main-header {text-align: center;}

.login-form {}

.denied-info-wrapper {
	background-color: rgba(243, 32, 19, .7);
	border: 2px rgba(243, 32, 19, 1) solid;
	border-radius: 5px;
}
.denied-info-wrapper p {margin: 0; margin-left: .3rem; margin-top: .05rem;}

.email-input-wrapper, .password-input-wrapper {align-items: center; margin-top: 1rem;}
.email-input-wrapper label, .password-input-wrapper label {width: 6rem;}
.email-input, .password-input {height: 1.2rem;}


.forget-password-text {text-align: end;}
.signup-text {color: var(--clr-other); text-align: center;}
.login-button {background-color: var(--bg-clr-tertiary); color: white;}


</style>
