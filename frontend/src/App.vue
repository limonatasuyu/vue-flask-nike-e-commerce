<template>
	<div class='app-container flex' :style="{isLoginViewAble:'overflow: hidden'}">
		<div>
			<nav class='main-nav flex'>
				<router-link class='nav-item' to='/'><img class='main-logo' src='@/assets/logo.png'></router-link>
				<img class='menu-icon display-none mobile-screen-display' @click='toggleNav' src='@/assets/menu-icon.png'/>
				<div :class='[isNavVisible ? "" : "mobile-screen-display-none"]' class='nav-item-container-wrapper'>
					<div :class='[isNavVisible ? "" : "mobile-screen-display-none"]' class='nav-item-container flex'>
						<div @click='toggleNav' class= 'menu-icon-wrapper display-none'>
							<img class='menu-icon' src='@/assets/menu-icon.png'/>
							<p class='nav-item'>Close Menu</p>
						</div>
						<router-link :class="isNavActive('home')" class='nav-item' to='/'>Home</router-link>
						<router-link :class="isNavActive('women')" class='nav-item' to='/browse-women'>Women</router-link>
						<router-link :class="isNavActive('men')" class='nav-item' to='/browse-men'>Men</router-link>
						<span v-if='userData === null' class='nav-item' style="cursor: pointer" @click="toggleLogin">Log In</span>
						<router-link v-if='userData' :class="isNavActive('profile')" class='profile-nav nav-item flex' to='/profile'>
							<span>Profile</span>
							<img class='nav-img' src='@/assets/user.png'/>
						</router-link>
						<router-link v-if='userData' :class="isNavActive('bag')" class='nav-item bag-nav flex' to='/bag'>
							<span>Bag</span>
							<img class='nav-img' src='@/assets/shopping-bag.png' />
							<span class="bag-number">{{bagNumber}}</span>
						</router-link>
					</div>
				</div>
			</nav>
			<router-view :increaseBagNumber='increaseBagNumber' :decreaseBagNumber='decreaseBagNumber' :ValidateEmail='ValidateEmail' :changeActiveNav="changeActiveNav" :toggleLogin='toggleLogin' :userData='userData' :getUserInfo='getUserInfo' />
			<LoginForm v-if='isLoginViewable' :toggleLogin='toggleLogin' :getUserInfo='getUserInfo'></LoginForm>
		</div>
	</div>
</template>

<script>
import LoginForm from './components/LoginForm.vue'
import axios from 'axios'

export default {
	name: 'App',
	data() {
		return {
			activeNavName: 'home',
			isNavVisible: false,
			isLoginViewable: false,
			userData: null,
			bagNumber: 0,
		}
	},
	methods: {
		isNavActive: function(navName) {if (navName == this.activeNavName) {return 'active-nav'} else {return ''}},
		toggleNav: function() {this.isNavVisible = !this.isNavVisible},
		changeActiveNav: function(newActive)	{this.activeNavName = newActive},
		toggleLogin: function() {
			this.isLoginViewable = !this.isLoginViewable
			document.querySelector('body').style.overflow = this.isLoginViewable ? 'hidden' : 'initial'
		},
		getUserInfo: function() {
			if (!this.$cookies.isKey('sessionId')) {console.log('cookie does not exists'); return}

			let payload = {sessionId: this.$cookies.get('sessionId')}
			
			let config = {withCredentials: true}
			axios.post(`${process.env.VUE_APP_API_URL ?? "http://localhost:5000"}/get-user-data`, payload, config)
				.then(res => this.userData = res.data.user_data)
				.catch(err => console.log(err))
		},
		ValidateEmail(mail) {
			if (/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(mail)) return true
			return false
		},
		getBagNumber() {
			if(!this.$cookies.isKey('sessionId')) return;
			
			let url = `${process.env.VUE_APP_API_URL ?? "http://localhost:5000"}/products-in-bag`,
			payload = {'sessionId': this.$cookies.get('sessionId')},
			config = {withCredentials: true}

			axios.post(url, payload, config)
				.then(res => this.bagNumber = res.data.product_data.length)
				.catch(err => console.log(err))
		},
		increaseBagNumber() {this.bagNumber += 1},
		decreaseBagNumber() {this.bagNumber -= 1}
	},
	components: {LoginForm},
	created() {
		this.getUserInfo();
		this.getBagNumber()
		document.addEventListener('beforeunload', () => alert('test'))
	},
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap');
html, body {margin: 0; padding: 0;}
:root {
	--bg-clr-primary: #f6f6f6;
	--bg-clr-secondary: #ffffff;
	--bg-clr-tertiary: #000000;
	--bg-clr-quaternary : #fcfcfc;
	--text-clr-primary: #2d2b2c; 
	--text-clr-secondary: #000000;
	--text-clr-tertiary: #333333;
	--clr-other: #877c78;
	--main-font: 'Inter', sans-serif;
}

.button {
	border: none; outline: none; cursor: pointer;
	padding: .9rem; border-radius: 8px;
}

a {color: black; text-decoration: none;}
body {background-color: var(--bg-clr-primary)}
.app-container {font-family: var(--main-font); height: fit-content;}
.app-container > div {width: 71vw; padding-bottom: 1rem;}

.bg-primary {background-color: var(--bg-clr-primary)}
.flex {display: flex;}
.grid {display: grid;}
.display-none {display: none;}
@media screen and (max-width: 1000px /*var(--mobile-screen-border)*/) {
	.mobile-screen-display-none {display: none;}
	.mobile-screen-display {display: initial;}
	.main-nav {justify-content: space-between;}
}

.main-nav {gap: 4vw; align-items: center; margin-top: 7rem;}
.main-logo {width: 5rem;}
.menu-icon {cursor: pointer; width: 1.4rem; height: 1.48rem;} /*it's look blury on 1.5rem*/
.nav-item-container {gap: 4vw;}
.nav-item:first-child {margin-left: 1.5rem}
.nav-item {
	text-decoration: none; 
	color: var(--text-clr-tertiary);
	font-size: 1.1rem;
}
.active-nav {
	color: var(--text-clr-primary);
	font-weight: bold;
	text-decoration: underline;
}
.profile-nav, .bag-nav {gap: .6rem; align-items: center;}
.nav-img {width: 1.5rem;}
.bag-number {
	font-size: .8rem;
	padding: .3rem .5rem;
	border-radius: 100px;
	background-color: orange;
	position: absolute;
	margin-left: 3.5rem; margin-bottom: 1rem;
}

@media screen and (max-width: 1000px /*var(--mobile-screen-border)*/) {
	.nav-item-container-wrapper {
		height: 100vh;
		background-color: var(--bg-clr-secondary);
		position: fixed;
		right: 0; top: 0; bottom: 0;
		animation: mount-anim .3s;
		z-index: 1;
	}
	.nav-item-container {display: grid; padding: 2rem; grid-gap: 2rem;}
	.menu-icon-wrapper {display: flex; align-items: center; gap: 1rem; }
	.menu-icon-wrapper img {display: block; margin-bottom: .2rem;}
	.nav-item-container .nav-item {margin-top: .8rem;}
	@keyframes mount-anim{
		from {transform: translateX(10rem)}
		to {transform: translateX(0)}
	}
}
@media screen and (max-width: 1830px) {.app-container > div {width: 90vw; margin-left: 5vw; margin-left: 5vw;}}
@media screen and (max-width: 1500px) {.main-nav {margin-top: 7vw;}}
@media screen and (min-width: 1000px) {.app-container {justify-content: center;}} 
</style>
