	<template>
<div v-if='userData' class='profile-page-container'>
	<h1 class='main-header'>Your Profile</h1>
	<div class='profile-pic-container'>
		<div style='width: 200px; height: 200px; border: 1px solid black;' />
		<button class='change-pic-button button'>change picture</button>	
	</div>
	<div class='user-info-container'>
		<div v-if='!isEmailChanging' class='email-info-wrapper info-wrapper flex'>	
			<p class='info-text'>email: <span>{{userData.email}}</span></p>
			<p class='change-info-text' @click='toggleEmailChange'>change email</p>
		</div>
		<div v-if='isEmailChanging' class='change-info-container flex info-wrapper'>
			<p class='info-text'>email: </p>
			<input class='new-info-input' v-model='email' />
			<div class='change-buttons-container flex'>
				<button class='change-info-button button' @click='changeInfo'>change</button>
				<button class='cancel-change-button button' @click='toggleEmailChange'>cancel</button>
			</div>
		</div>
		<div v-if='!isUsernameChanging' class='username-info-wrapper info-wrapper flex'>
			<p class='info-text'>username: <span>{{userData.username}}</span></p>
			<p class='change-info-text' @click='toggleUsernameChange'>change username</p>
		</div>
		<div v-if='isUsernameChanging' class='change-info-container flex info-wrapper'>
			<p class='info-text'>username: </p>
				<input class='new-info-input' v-model='username' />
				<div class='change-buttons-container flex'>
					<button class='change-info-button button' @click='changeInfo'>change</button>
					<button class='cancel-change-button button' @click='toggleUsernameChange'>cancel</button>
				</div>
		</div>
		<div v-if="!isAddressChanging" class='address-info-wrapper info-wrapper flex'>
			<p class='info-text'>address: {{userData.address ? userData.address : "not specified" }}</p>
			<p class='change-info-text' @click='toggleAddressChange'>change adress</p>
		</div>
		<div v-if='isAddressChanging' class='address-info-wrapper info-wrapper flex'>
			<p class='info-text'>address: </p>
			<input class='new-info-input' v-model='address' />
			<div class='change-buttons-container flex'>
				<button class='change-info-button button' @click='changeInfo'>change</button>
				<button class='cancel-change-button button' @click='toggleAddressChange'>cancel</button>
			</div>
		</div>
		<router-link to='/' class='history-link'>Go to shopping history.</router-link>
		<p class='change-password-text'>change password</p>
	</div>
</div>
</template>
<script>
import axios from 'axios'

export default {
	data() {	
		return {
			email: '',
			isEmailChanging: false,
			username: '',
			isUsernameChanging: false,
			address: '',
			isAddressChanging: false,
			changeResponse: null,
		}
	},
	methods: {
		toggleEmailChange() {this.isEmailChanging = !this.isEmailChanging},
		toggleUsernameChange() {this.isUsernameChanging = !this.isUsernameChanging},
		toggleAddressChange() {this.isAddressChanging = !this.isAddressChanging},
		changeInfo() {
			let sessionId = this.$cookies.get('sessionId')
			let payload;
			if (!this.ValidateEmail(this.email)) {alert('email is invalid'); return}
			
			payload = {
				sessionId: sessionId,
				email: this.email,
				username: this.username,
				address: this.address,
			}

			let config = {withCredentials: true}
			let url = 'http://localhost:5000/update-user'
			
			axios.put(url, payload, config)
				.then((res) => {
						console.log(res)
						this.changeResponse = res
						this.getUserInfo()
						this.isUsernameChanging = false; this.isEmailChanging = false; this.isAddressChanging = false;
				})
				.catch(err => console.log(err))
		},
	},
	props: ['changeActiveNav', 'userData', 'getUserInfo', 'ValidateEmail'],
	created() {
		this.changeActiveNav('profile')
		if (this.userData) {
			this.email = this.userData.email;
			this.username = this.userData.username;
			this.address = this.userData.address;
		}
	},
	watch: {
		userData() {
			if (this.userData) {
				this.email = this.userData.email;
				this.username = this.userData.username;
				this.address = this.userData.address;
			}	
		}
	}
}
</script>
<style scoped>
.profile-page-container {background-color: var(--bg-clr-secondary); padding: .5rem 0 1rem 0; margin-top: .5rem;}
.profile-page-container > * {margin-left: 1.5rem;}
.main-header {margin-top: .6rem;}

.change-pic-button {
	background-color: var(--bg-clr-tertiary);
	color: white;
	padding-bottom: .5rem; padding-top: .5rem;
	margin-top: .5rem;
	width: 200px; /*Picture's width, if it changes, change this too*/
}

.user-info-container {margin-top: 1.6rem; max-width: 81vw;}
.info-wrapper {justify-content: space-between; gap: .5rem; flex-wrap: wrap; max-width: 19.6rem; margin-top: 1rem;}
.info-wrapper p {margin: 0;}
.info-text {}
.info-text span {color: var(--clr-other);}
.change-info-text {text-decoration: underline; cursor: pointer;}

.history-link {display: block; margin-top: 3rem;}
.change-password-text {color: var(--clr-other);}
.history-link, .change-password-text {text-align: end; margin-right: 1.5em; text-decoration: underline;}

.change-info-container {
	justify-content: initial;
	max-width: 25rem !important;
}
.new-info-input {
	outline: none;
}
.change-buttons-container {
	margin-top: -.2rem;
	gap: .6rem;	
}
.change-info-button, .cancel-change-button {
	padding-top: .3rem; padding-bottom: .3rem;
}


@media screen and (min-width: 750px) {
	.profile-page-container {display: flex; gap: 10vw;}
	.main-header {position: absolute; left: 7vw;}
	.profile-pic-container {margin-top: 6rem;}
	.user-info-container {font-size: 1.1rem; margin-top: 6rem;}
	.info-wrapper {max-width: 22rem;}
	.history-link, .change-password-text {position: absolute; right: 5vw;}
}
@media screen and (min-width: 1000px) {.profile-page-container {gap: 25%;}}
@media screen and (min-width: 1830px) {
	.main-header {left: 14vw;}
	.history-link, .change-password-text {right: 15vw;}
}
</style>
