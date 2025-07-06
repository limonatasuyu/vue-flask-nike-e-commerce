<template>
  <div class="home-container">
		<div class='product-main-context-container flex'>
			<div class='product-nav-container grid'>
				<p @click='changeProduct(0)' :class='[homePageProducts.indexOf(currentProduct) == 0 && "active-product-nav-item"]' class='product-nav-item grid'>01</p>
				<p @click='changeProduct(1)' :class='[homePageProducts.indexOf(currentProduct) == 1 && "active-product-nav-item"]' class='product-nav-item grid'>02</p>
				<p @click='changeProduct(2)' :class='[homePageProducts.indexOf(currentProduct) == 2 && "active-product-nav-item"]' class='product-nav-item grid'>03</p>
			</div>
			<div class='product-text'>
				<h1 class='product-header'><p>{{currentProduct.split(" ").slice(0, 2).join(" ")}}</p><p>{{currentProduct.split(" ").slice(2).join(" ")}}</p></h1>
				<img class='product-highlighted-image display-none' :src='`${baseUrl}/images/${currentProduct}-single.png`' />
				<p class='product-description'>Ex nesciunt pariatur voluptatem vitae voluptas quis placeat. Quasi laboriosam in tempora quia tenetur veritatis. Necessitatibus quia sint molestiae a quia eos sequi expedita.</p>
				<div class='product-price-wrapper flex'>
					<router-link class='add-to-bag-button button' :to="`/product-men-${currentProduct}`" >Add to Bag</router-link>
					<h2 class='product-price'>200${{currentProduct.price}}</h2>
				</div>
			</div>
			<img class='product-highlighted-image' :src='`${baseUrl}/images/${currentProduct}-single.png`'/>
		</div>
		<div class='product-images-container flex'>
			<div v-for="i, x in ['back', 'top', 'side']" :key='x' ><img :src='`${baseUrl}/images/${currentProduct}-${i}.png`'/></div>
		</div>
	</div>	
</template>
<script>

const homePageProducts = ['Nike Air Max Pre Day', 'Dunk Low Pro Parra', 'Nike Air Edge 270']

export default {
  name: 'homeView',
	data() {
		return {
			homePageProducts: homePageProducts,
			currentProduct: homePageProducts[0],
			baseUrl: process.env.VUE_APP_API_URL || 'http://localhost:5000',
		}
	},
	methods: {
		changeProduct(index) {this.currentProduct = this.homePageProducts[index]}
	},
	props: ['changeActiveNav'],
  created() {this.changeActiveNav('home')}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.home-container {margin-top: 7rem;}
.product-main-context-container {gap: 7rem;}
.product-nav-container {
	align-items: end;
	grid-gap: 2rem;
	width: 2rem;
	height: 13rem;
	border-left: 1.8px var(--clr-other) solid;
}
.product-nav-item {
	margin-left: -2px;
	height: 70%;
	align-items: center;
	padding-left: 3rem;
	font-size: .9rem;
	color: var(--clr-other);
	font-weight: 500;
	cursor: pointer;
}
.active-product-nav-item {
	border-left: 3px var(--bg-clr-tertiary) solid;
	font-size: 1.5rem;
	color: var(--text-clr-primary);
	padding-left: 2.2rem;
}
.product-text {
	margin-top: 0;
}
.product-header {
	margin-top: 0;
	margin-bottom: 0;
	font-size: 4.8rem;
	font-weight: 800;
	max-width: 35rem;
	color: var(--text-clr-primary);
}
.product-header p {margin: 0;}
.product-description {
	color: var(--clr-other);
	font-size: 1.1rem;
	max-width: 25rem;
}
.product-price-wrapper {
	align-items: center;
	gap: 1.5rem;
}
.add-to-bag-button {
	background-color: var(--text-clr-primary);
	font-size: 1rem; color: white;
	width: 12rem;
  text-align: center;
}
.product-price {
	color: var(--text-clr-primary);
  font-size: 2rem;
}
.product-highlighted-image {
	rotate: -48deg;
	height: 25.8vw;
	position: absolute;
	right: 8vw;
	margin-top: -3.5rem;
}
.product-images-container {
	background-color: var(--bg-clr-secondary);
	height: 12.5rem;
	position: absolute;
	z-index: -1;
	margin-left: -3.6%;
	width: 73.6%;
	gap: 1.6rem;
	align-items: center;
	margin-top: 4rem;
	border-radius: 0 0 25px 25px;
}
.product-images-container div {
	height: 74%; width: 10.2rem;
	background-color: var(--bg-clr-primary);
	display: flex; justify-content: center;
	border-radius: 10px;
}
.product-images-container div img {height: 100%}
.product-images-container div:first-child {margin-left: 4.3rem;}
@media screen and (max-width: 1830px) {.product-images-container {margin-left: 0;}}
@media screen and (max-width: 1400px) {
	.product-header {font-size: 5.5vw;}
	.product-highlighted-image {
		height: 25vw; right: 3vw;
		margin-top: -1rem;
	}
	.product-images-container {display: flex; justify-content: center;}
	.product-images-container div:first-child {margin-left: 0;}
}
@media screen and (max-width: 1000px) {
	.product-header {font-size: 3.5rem;}
	.product-highlighted-image {
		height: 19vw; right: 1.5vw;
		margin-top: 5rem;
	}
}
@media screen and (max-width: 820px) {
	.product-highlighted-image {display: none}
	.product-price-wrapper {margin-top: 5rem;}
	.product-description {display: none;}
	.product-text .product-highlighted-image {
		display: initial; position: initial;
		rotate: 0deg; height: 28vw;
		margin-left: 3rem;
	}
	.product-header {font-size: 3rem;}
	.product-header p {width: 100%; display: inline;}
	.product-header p:last-child {margin-left: .7rem}
	.product-images-container {width: 92%;}
}
@media screen and (max-width: 650px) {.product-images-container div:first-child {display: none;}}
@media screen and (max-width: 600px) {
	.product-main-context-container {gap: 3rem;}
	.product-nav-item {padding-left: 1rem;}
	.product-description {width: 17rem;}
}
@media screen and (max-width: 450px) {
	.product-images-container {width: 90vw;} 
	.product-price-wrapper {margin-left: -3rem;}
}
@media screen and (max-width: 400px) {.product-images-container {width: 105vw;}}
@media screen and (max-width: 350px) {.product-images-container {width: 140vw;}}

</style>
